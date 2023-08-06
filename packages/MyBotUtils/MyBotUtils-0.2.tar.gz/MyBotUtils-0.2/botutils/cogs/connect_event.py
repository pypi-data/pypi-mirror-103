from .. import utils
import discord

class ConnectEvent(utils.Cog):
    
    async def send_to_webhook(self, event, message, username, log_message:bool):
        webhook = self.bot.get_event_webhook(event)
        if webhook is None:
            self.logger.debug(f"Ignoring {event} event due to config not being set")

        await webhook.send(discord.utils.escape_mentions(message), avatar_url=self.bot.user.avatar_url, username=username, wait=True)
        if log_message:
            self.logger.info(message)

    @utils.Cog.listener()
    async def on_ready(self):

        await self.send_to_webhook(
            event='bot_ready',
            message=f"Bot ready event just pinged for instance with shards `{len(self.bot.shards)}`",
            username=f"{self.bot.user.name} - Bot ready",
            log_message=False
        )

    @utils.Cog.listener()
    async def on_shard_ready(self, shard_id):

        await self.send_to_webhook(
            event='shard_update',
            message=f"Shard id {shard_id} just pinged for an on ready event.",
            username=f"{self.bot.user.name} - Shard ready",
            log_message=False
        )

    @utils.Cog.listener()
    async def on_shard_connect(self, shard_id):

        await self.send_to_webhook(
            event='shard_update',
            message=f"Shard id {shard_id} just pinged for an on connect event.",
            username=f"{self.bot.user.name} - Shard connect",
            log_message=True
        )


    @utils.Cog.listener()
    async def on_shard_disconnect(self, shard_id):

        await self.send_to_webhook(
            event='shard_update',
            message=f"Shard id {shard_id} just pinged for an on disconnect event.",
            username=f"{self.bot.user.name} - Shard disconnect",
            log_message=True
        )


    @utils.Cog.listener()
    async def on_guild_join(self, guild):

        await self.send_to_webhook(
            event='guild_update',
            message=f"Just joined guild `{guild.name}` with {len([i for i in guild.member if not i.bot])} members",
            username=f"{self.bot.user.name} - Guild join",
            log_message=False
        )


    @utils.Cog.listener()
    async def on_guild_remove(self, guild):

        await self.send_to_webhook(
            event='guild_update',
            message=f"Just left guild `{guild.name}` with {len([i for i in guild.member if not i.bot])} members",
            username=f"{self.bot.user.name} - Guild remove"
        )

def setup(bot:utils.Bot):
    x = ConnectEvent(bot)
    bot.add_cog(x)