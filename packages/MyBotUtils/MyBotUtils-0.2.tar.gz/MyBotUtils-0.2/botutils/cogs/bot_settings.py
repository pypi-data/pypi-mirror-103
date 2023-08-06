from .. import utils
from discord.ext import commands
import discord

class BotSettings(utils.Cog):

    @utils.command()
    @commands.has_permissions(manage_channels=True)
    async def prefix(self, ctx, *, prefix):
        """
        Set the prefix for your server
        """

        if len(prefix) > 30:
            return await ctx.send("The maximum length a prefix can be is 30 characters.")

        self.bot.guild_settings[ctx.guild.id]['prefix'] = prefix
        async with self.bot.database() as db:
            await db("INSERT INTO guild_settings (guild_id, prefix) values ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET prefix=$2", ctx.guild.id, prefix)

        await ctx.send(f"Set your servers prefix to `{prefix}`", allowed_mentions=discord.AllowedMentions.none())

def setup(bot:utils.Bot):
    x = BotSettings(bot)
    bot.add_cog(x)