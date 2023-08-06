from .. import utils

class RedisHandler(utils.Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.send_dm.start()
        self.send_message.start()
        self.update_guild_cache.start()

    def cog_unload(self):
        self.send_dm.stop()
        self.send_message.stop()
        self.update_guild_cache.stop()

    @utils.redis_channel("SendDM")
    async def send_dm(self, payload):
        """
        Redis channel for dming a user
        """

        user_id = payload['user_id']
        content = payload['content']

        # Make sure we are using the correct bot
        bot_id = payload.get('bot_id', None)
        if bot_id is not None and bot_id != self.bot.user.id:
            return

        # Get the user
        user = self.bot.get_user(user_id) or await self.bot.fetch_user(user_id)
        if not user:
            return

        # Make sure we dont spam the user if there are multiple instances running
        if 0 not in (self.bot.shard_ids or [0]):
            return

        # Send the user a message
        try:
            await user.send(content=content)
            self.logger.debug(f"Sent dm to user {user}")
        except discord.Forbidden:
            self.logger.error(f"Failed sending a dm to {user}")
            pass

    @utils.redis_channel("SendMessage")
    async def send_message(self, payload):
        """
        Send a message
        """

        channel_id = payload['channel_id']
        content = payload['content']

        # Make sure we are using the correct bot
        bot_id = payload.get('bot_id', None)
        if bot_id is not None and bot_id != self.bot.user.id:
            return

        # Get the channel
        channel = self.bot.get_channel(channel_id) or await self.bot.fetch_channel(channe_id)
        if not channel:
            return

        # Make sure we dont spam the channel if there are multiple instances running
        if 0 not in (self.bot.shard_ids or [0]):
            return

        # Sent a message to the channel
        try:
            await channel.send(content)
            self.logger.debug(f"Sent a message to channel #{channel.name} ({channel_id})")
        except discord.Forbidden:
            self.logger.error(f"Failing sending a message to channel #{channel.name} ({channel_id})")

    @utils.redis_channel("UpdateGuildSettingsCache")
    async def update_guild_cache(self, payload):
        """
        Updates the bots guild_settings cache
        """

        guild_id = payload['guild_id']
        key = payload['key']
        value = payload['value']

        try:
            self.bot.guild_settings[guild_id][key] = value
            self.logger.debug(f"Updated guild settings cache for guild id {guild_id}")
        except Exception as e:
            self.logger.error(f"Failed updating guild settings cache for guild {guild_id} - {e}")


def setup(bot:utils.Bot):
    if not bot.redis_enabled:
        return

    x = RedisHandler(bot)
    bot.add_cog(x)