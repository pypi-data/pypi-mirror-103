import discord
from discord.ext import commands
import toml
import logging
import glob
from datetime import datetime as dt
import asyncio
import aiohttp
import collections

from .database import Database
from .redis import Redis
from .custom_context import CustomContext as Context

def get_prefix(bot, message):
    """
    returns the proper prefix for the context of the message
    """

    if not message.guild:
        prefix = bot.config.get('prefix')
    else:
        try:
            prefix = bot.guild_settings[message.guild.id]['prefix'] 
        except Exception:
            prefix = bot.config.get('prefix')

    return commands.when_mentioned_or(prefix)(bot, message)

class CustomBot(commands.AutoShardedBot):
    def __init__(self, config_file:str="config/config.toml", logger:logging.Logger=None, *args, **kwargs):
        """
        Custom bot class to make things easier for me
        """

        # Store logger
        self.logger = logger or logging.getLogger('bot').setLevel("INFO")

        # Store config
        self.config_file = config_file
        self.config = None
        self.cache_config()

        # Store startup method/time
        self.startup_time = dt.now()
        self.startup_method = None

        # Store aiohttp session
        self.session = aiohttp.ClientSession(loop=asyncio.get_event_loop())

        # Store database and redis utils
        self.database = Database
        self.database.logger = self.logger.getChild('database')

        self.redis = Redis
        self.redis.logger = self.logger.getChild('Redis')

        # Get intents and allowed mentions
        if self.config['intents']:
            intents = discord.Intents(**self.config['intents'])
        else:
            intents = discord.Intents.default()
        
        if self.config['allowed_mentions']:
            allowed_mentions = discord.AllowedMentions(**self.config['allowed_mentions'])
        else:
            allowed_mentions = discord.AllowedMentions.all()
        
        # Run the original discord.py init method
        super().__init__(intents=intents, allowed_mentions=allowed_mentions, command_prefix=get_prefix, *args, **kwargs)

    @property
    def database_enabled(self):
        try:
            return self.config['database']['enabled']
        except Exception:
            return False

    @property
    def redis_enabled(self):
        try:
            return self.config['redis']['enabled']
        except Exception:
            return False

    @property
    def embediffy(self):
        try:
            return self.config['embed']['enabled']
        except Exception:
            return False
    
    @property
    def owner_ids(self):
        return self.config['owner_ids']

    @owner_ids.setter 
    def owner_ids(self, value):
        pass

    def cache_config(self):
        try:
            with open(self.config_file) as f:
                self.config = toml.load(f)
        except Exception as e:
            self.logger.critical(f"Could not read config file {self.config_file} - {e}")

    async def get_context(self, message, cls=Context):
        """
        Used to override d.py's default context with out new custom context
        """

        return await super().get_context(message, cls=cls)

    def get_all_extensions(self):
        ext = glob.glob('cogs/[!_]*.py')
        return [i.replace('\\', '.').replace('/', '.')[:-3] for i in ext]

    def load_all_extensions(self):

        self.logger.info("Loading all extensions")

        # Get all extensions
        for extension in self.get_all_extensions():
            try:
                # Unload them
                self.unload_extension(extension)
            except commands.ExtensionNotLoaded:
                pass
            except Exception as e:
                self.logger.error(f"Failed unloading extension {extension} - {e}")

            try:
                # Reload them
                self.load_extension(extension)
            except Exception as e:
                self.logger.error(f"Failed loading extension {extension} - {e}")

    async def set_default_presence(self, shard_id=None):

        self.logger.info("Setting default presence")
        presence_data = self.config['presence']

        # Check if we should include shard id or not
        if self.shard_count > 1 and presence_data['include_shard_id']:
            for shard in self.shard_ids:
                text = f"{presence_data['text'].format(bot=self)} (shard {shard})"
                status = getattr(discord.Status, presence_data['status'])
                activity = discord.Activity(name=text, type=getattr(discord.ActivityType, presence_data['activity'].lower()))

                await self.change_presence(activity=activity, status=status, shard_id=shard)
        else:
            text = presence_data['text'].format(bot=self)
            status = getattr(discord.Status, presence_data['status'])
            activity = discord.Activity(name=text, type=getattr(discord.ActivityType, presence_data['activity'].lower()))

            await self.change_presence(activity=activity, status=status)


    async def read_database_file(self, db):

        # Open the db file
        try:
            with open("config/database.sql") as a:
                data = a.read()
        except Exception as e:
            self.logger.error(f"Could not read database file config/database.sql - {e}")

        # Get the statements
        create_table_statements = []
        current_line = ''
        for line in data.split('\n'):
            if line.lstrip().startswith('--'):
                continue
            current_line += line + '\n'
            if line.endswith(';') and not line.startswith(' '):
                create_table_statements.append(current_line.strip())
                current_line = ''

        for i in create_table_statements:
            if i and i.strip():
                await db(i.strip())

    def get_event_webhook(self, event_name):
        webhook_url = self.config['event_webhooks'][event_name]
        if webhook_url is None:
            return None
        
        return discord.Webhook.from_url(webhook_url, adapter=discord.AsyncWebhookAdapter(self.session))

    async def cache_table(self, db, table, primary_key, variable_name=None):
        """
        Aysnc function to cache a database table
        """   

        self.logger.debug(f"Caching database table {table} with primary key {primary_key}")
        variable_name = variable_name or table

        # Make sure the variable doesnt already exist
        try:
            variable_check = getattr(self, variable_name)
        except AttributeError:
            variable_check = None

        if variable_check:
            self.logger.critical(f"Failed caching database table {table} - The variable {variable_name} already exists in the bot class")
            exit(1)

        cache = collections.defaultdict(lambda: {})
        data = await db("SELECT * FROM {table} WHERE {primary_key} IS NOT NULL".format(table=table, primary_key=primary_key))

        for row in data:
            for key, value in row.items():
                cache[row[primary_key]][key] = value

        setattr(self, variable_name, cache)

    async def _startup_method(self):
        """
        Caches database tables set in config
        """
        if self.database_enabled:
            async with self.database() as db:
                await self.read_database_file(db)

                database_cache = self.config['database_cache']
                if database_cache['enabled']:
                    for database in database_cache['databases']:
                        await self.cache_table(db, **database)

    async def start(self):
        """
        Runs the bots startup then connects to discord
        """

        self.logger.info("Running startup...")

        # Store startup method for a later check
        self.startup_method = await self._startup_method()

        # Login to discord
        await super().start(self.config['token'])

