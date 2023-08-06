from .. import utils
from discord.ext import commands
import discord

import aiohttp
import traceback
import io

error_responses = (
    (
        commands.MissingRequiredArgument,
        lambda ctx, error: f"You are missing the `{error.param.name}` argument that is required for this command to run - see `{ctx.clean_prefix}help {ctx.invoked_with}`."
    ),
    (
        commands.BadArgument,
        lambda ctx, error: str(error).format(ctx=ctx, error=error)
    ),
    (
        commands.TooManyArguments,
        lambda ctx, error: f"You gave too many arguments to this command - see `{ctx.clean_prefix}help {ctx.invoked_with}`."
    ),
    (
        commands.CommandOnCooldown,
        lambda ctx, error: f"This command is on cooldown. Try again later."
    ),
    #(
    #   utils.errors.bot_not_ready,
    #   lambda ctx, error: "I am not ready to start processing commands yet, please wait."
    #),
    (
        commands.NSFWChannelRequired,
        lambda ctx, error: "This command can only be ran in NSFW channels."
    ),
    (
        commands.DisabledCommand,
        lambda ctx, error: "This command is disbaled, sorry for any inconvenience."
    ),
    (
        commands.NoPrivateMessage,
        lambda ctx, error: "This command can not be ran in DMs."
    ),
    (
        commands.PrivateMessageOnly,
        lambda ctx, error: "This command can only be ran in DMs."
    ),
    (
        commands.NotOwner,
        lambda ctx, error: "You have to be registered as a bot owner to run this command."
    ),
    (
        commands.MissingAnyRole,
        lambda ctx, error: f"You have to have one of the {', '.join(['`' + role + '`' for role in error.missing_roles])} roles to be able to run this command."
    ),
    (
        commands.BotMissingAnyRole,
        lambda ctx, error: f"I need to have one of the {', '.join(['`' + role + '`' for role in error.missing_roles])} roles for you to be able to run this command."
    ),
    (
        commands.MissingRole,
        lambda ctx, error: f"You need to have the `{error.missing_role}` role to be able to run this command."
    ),
    (
        commands.BotMissingRole,
        lambda ctx, error: f"I need to have the `{error.missing_role}` role for you to be able to run this command."
    ),
    (
        commands.MissingPermissions,
        lambda ctx, error: f"You need the `{error.missing_perms[0]}` permission to be able to run this command."
    ),
    (
        commands.BotMissingPermissions,
        lambda ctx, error: f"I need to have the `{error.missing_perms[0]}` permission for me to be able to run this command."
    ),
    (
        discord.NotFound,
        lambda ctx, error: str(error).format(ctx=ctx, error=error)
    ),
    (
        commands.CheckFailure,
        lambda ctx, error: str(error).format(ctx=ctx, error=error)
    ),
    (
        discord.Forbidden,
        lambda ctx, error: "Discord is saying I'm unable to perform that action."
    ),
    (
        (discord.HTTPException, aiohttp.ClientOSError),
        lambda ctx, error: "Either I or Discord messed up running this command. Please try again later."
    ),
)

class ErrorHandler(utils.Cog):

    async def send_error(self, ctx, message):
        try:
            await ctx.send(message, allowed_mentions=discord.AllowedMentions.none())
        except discord.Forbidden:
            try:
                await ctx.author.send(message)
            except discord.Forbidden:
                pass

    @utils.Cog.listener()
    async def on_command_error(self, ctx, error):

        ignored_errors = (commands.CommandNotFound)
        if isinstance(error, ignored_errors):
            return

        owner_reinvoke_errors = (
            commands.MissingRole, commands.MissingAnyRole, commands.MissingPermissions,
            commands.CommandOnCooldown, commands.DisabledCommand, commands.CheckFailure,
        )
        if isinstance(error, owner_reinvoke_errors) and await self.bot.is_owner(ctx.author):
            await ctx.reinvoke()

        if hasattr(ctx.command, "on_error"):
            return

        found_error = False
        output = None 
        for error_type, func in error_responses:
            if isinstance(error, error_type):
                output = func(ctx, error)
                found_error = True
                break

        if output:
            await self.send_error(ctx, output)

        if found_error:
            return

        try:
            await ctx.send(f"`{str(error)}`", allowed_mentions=discord.AllowedMentions.none())
        except discord.Forbidden:
            pass

        # Send the error to the webhook
        webhook = self.bot.get_event_webhook("unhandled_error")
        file_bytes = io.BytesIO(traceback.format_exception(None, error, error.__traceback__))
        error_text = f"""Error `{error}` encountered\n
            Guild: {ctx.guild.name} ({ctx.guild.id})\n
            Channel: {ctx.channel.name} ({ctx.channel.id})\n
            User: {ctx.author} ({ctx.author.id})
            """

        try:
            await webhook.send(
                content=error_text,
                file=discord.File(file_bytes, filename="errorlog.py"),
                username=f"{self.bot.user.name} - Error log",
                avatar_url=self.bot.user.avatar_url,
                allowed_mentions=discord.AllowedMentions.none()
                )
        except Exception as e:
            raise e

        ctx.cog.logger.error(error_text.replace('\n', ' '))

def setup(bot:utils.Bot):
    x = ErrorHandler(bot)
    bot.add_cog(x)