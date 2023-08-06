from cogs import utils
import logging
import argparse
import sys
import asyncio
import discord

parser = argparse.ArgumentParser()
parser.add_argument("--config_file", type=str, default="config/config.toml", help="Config file for the bot")
parser.add_argument("--loglevel", type=str, default="debug", help="Global log level.")
parser.add_argument("--shardcount", type=int,default=None, help="The number of shards to run the bot with.")
parser.add_argument("--min", type=int, default=None, help="The minimum shard ID that the bot will run with.")
parser.add_argument("--max", type=int, default=None, help="The maximum shard ID that the bot will run with.")
args = parser.parse_args()

def set_log_level(logger, level):
    if isinstance(logger, str):
        logger = logging.getLogger(logger)

    try:
        level = getattr(logging, level.upper())
    except AttributeError:
        raise ValueError(f"Could not find log level {level.upper()} in the logging module.")
    
    logger.setLevel(level)

logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s: %(message)s', stream=sys.stdout)
logger = logging.getLogger('bot')

set_log_level(logger, args.loglevel)
set_log_level("discord", "info")

def get_shard_ids(min, max, shardcount):
    if shardcount is None:
        return None

    if not min:
        min = 0
    if not max:
        max = shardcount - 1
        
    shard_ids = list(range(min, max + 1))
    return shard_ids

bot = utils.Bot(
    activity=discord.Game("Connecting..."),
    status=discord.Status.dnd,
    config_file=args.config_file,
    shard_count=args.shardcount,
    shard_ids=get_shard_ids(args.min, args.max, args.shardcount),
    logger=logger,
    case_insensitive=True
)

@bot.event 
async def on_ready():
    logger.info(f"Connected to discord as {bot.user} // {bot.user.id}")
    await bot.set_default_presence()

if __name__ == '__main__':
    loop = bot.loop

    if bot.database_enabled:
        logger.info("Running postgresql database startup")
        try:
            db_task = loop.create_task(bot.database.create_pool(bot.config['database']))
            loop.run_until_complete(db_task)
        except ConnectionRefusedError:
            logger.error("Database connection refused - Did you set the right information in the config?")
        except Exception as e:
            raise e

    if bot.redis_enabled:
        try:
            logger.info("Running redis startup")
            redis_task = loop.create_task(bot.redis.create_pool(bot.config['redis']))
            loop.run_until_complete(redis_task)
        except ConnectionRefusedError:
            logger.error("Redis connection refused - Did you set the right information in the config?")
        except Exception as e:
            raise e

    bot.load_all_extensions()
    try:
        logger.info("Running bot")
        loop.run_until_complete(bot.start())
    except KeyboardInterrupt:
        logger.info("Closing bot")
        loop.run_until_complete(bot.close())

    if bot.database_enabled:
        logger.info("Closing database pool")
        loop.run_until_complete(bot.database.pool.close())
    if bot.redis_enabled:
        logger.info("Closing redis pool")
        loop.run_until_complete(bot.redis.pool.close())
    logger.info("Closing asyncio loop")
    loop.close()