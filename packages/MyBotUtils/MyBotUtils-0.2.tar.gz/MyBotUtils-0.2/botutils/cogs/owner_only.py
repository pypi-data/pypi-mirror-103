from .. import utils
from discord.ext import commands
import discord

import textwrap
import io
import contextlib
import traceback
import json
import asyncio

class OwnerOnly(utils.Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.test.start()

    def cog_unload(self):
        self.test.stop()

    def _cleanup_code(self, content):
        """Automatically removes code blocks from the code."""

        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            if content[-4] == '\n':
                return '\n'.join(content.split('\n')[1:-1])
            return '\n'.join(content.split('\n')[1:]).rstrip('`')

        # remove `foo`
        return content.strip('` \n')

    @utils.command(aliases=['evall', 'eval'])
    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True)
    async def ev(self, ctx, *, content:str):
        """Evaluates some Python code
        Gracefully stolen from Rapptz ->
        https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/admin.py#L72-L117"""

        # Make the environment
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'self': self,
        }
        env.update(globals())

        # Make code and output string
        content = self._cleanup_code(content)
        code = f'async def func():\n{textwrap.indent(content, "  ")}'

        # Make the function into existence
        stdout = io.StringIO()
        try:
            exec(code, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        # Grab the function we just made and run it
        func = env['func']
        try:
            # Shove stdout into StringIO
            with contextlib.redirect_stdout(stdout):
                ret = await func()
        except Exception:
            # Oh no it caused an error
            stdout_value = stdout.getvalue() or None
            await ctx.send(f'```py\n{stdout_value}\n{traceback.format_exc()}\n```')
        else:
            # Oh no it didn't cause an error
            stdout_value = stdout.getvalue() or None

            # Give reaction just to show that it ran
            await ctx.message.add_reaction("\N{OK HAND SIGN}")

            # If the function returned nothing
            if ret is None:
                # It might have printed something
                if stdout_value is not None:
                    await ctx.send(f'```py\n{stdout_value}\n```')
                return

            # If the function did return a value
            result_raw = stdout_value or ret  # What's returned from the function
            result = str(result_raw)  # The result as a string
            if result_raw is None:
                return
            text = f'```py\n{result}\n```'
            if type(result_raw) == dict:
                try:
                    result = json.dumps(result_raw, indent=4)
                except Exception:
                    pass
                else:
                    text = f'```json\n{result}\n```'
            if len(text) > 2000:
                await ctx.send(file=discord.File(io.StringIO(result), filename='ev.txt'))
            else:
                await ctx.send(text)

    @utils.command(aliases=['su'])
    @utils.checks.is_owner()
    async def sudo(self, ctx, user, message):
        """
        Run a command as another user
        """

        msg = message.copy()

        try:
            msg.author = ctx.guild.get_member(user.id) or await ctx.guild.fetch_member(user.id)
        except Exception:
            msg.author = user

        msg.content = ctx.prefix + message
        new_ctx = await self.bot.get_context(message)
        await new_ctx.invoke()
        await ctx.okay()

    @utils.group()
    @utils.checks.is_owner()
    async def botuser(self, ctx):
        """
        Parent command for botuser command
        """

        pass

    @botuser.command(aliases=['av', 'pfp', 'picture', 'image'])
    @utils.checks.is_owner()
    async def avatar(self, ctx, image=None):
        """
        Changes the current bot users avatar
        """

        if not image:
            try:
                image = ctx.message.attachments[0].url
            except Exception:
                await ctx.send("You need to provide an image.")

        image_data = await self.bot.session.get(image)
        image_bytes = await image_data.read()

        await self.bot.edit(avatar=image_bytes)
        await ctx.okay()

    @botuser.command(aliases=['name'])
    @utils.checks.is_owner()
    async def username(self, ctx:utils.Context, name):
        """
        Changes the current bot users name
        """

        if len(name) > 32:
            return await ctx.send("The maximum length a username can be is 32 characters.")

        await self.bot.user.edit(username=name)       
        await ctx.okay()

    @botuser.command(aliases=['game'])
    @utils.checks.is_owner()
    async def activity(self, ctx, activity, name=None):
        """
        Changes the current bot users activity
        """ 

        
        activity = discord.Activity(name=name, type=getattr(discord.ActivityType, activity.lower()))
        await self.bot.change_presence(activity=activity)
        await ctx.okay()

    @botuser.command()
    @utils.checks.is_owner()
    async def status(self, ctx, status):
        """
        Changes the current bot users status
        """

        await self.bot.change_presence(activity=self.bot.guilds[0].me.activity,status=getattr(discord.Status, status.lower()))
        await ctx.okay()

    @utils.command(aliases=['rld', 'rl'])
    @utils.checks.is_owner()
    async def reload(self, ctx, *cogs):
        """
        Reloads an extension
        """

        messages = []
        extensions = [f"cogs.{'_'.join(cog)}" for cog in cogs]
        for cog in extensions:
            try:
                # Unload them
                self.bot.unload_extension(cog)
            except commands.ExtensionNotLoaded:
                pass
            except Exception as e:
                messages.append(f"Failed unloading extension {cog} - {e}")

            try:
                # Reload them
                self.bot.load_extension(cog)
            except Exception as e:
                messages.append(f"Failed loading extension {cog} - {e}")
            messages.append(f"Successfully reloaded extension {cog}")

        #await ctx.send(f"```{'\n'.join(messages)}```", embeddify=False)

    @utils.command(aliases=['sh'])
    @utils.checks.is_owner()
    async def shell(self, ctx, *, command):
        """
        Runs a shell command
        """

        # Run the command
        command_process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

        command_data = f"$ {command}\n"
        m = await ctx.send(f"```{command_data}```", embeddify=False)

        async def get_data(stdout, stderr):
            return (await stdout.read()).decode() + (await stderr.read()).decode()

        # Get data until the command finishes
        while command_process.returncode is None:
            data = await get_data(command_process.stdout, command_process.stderr)
            if data:
                command_data += f"{data} \n"
                await m.edit(content=f"```\n{command_data[-1900:]}```")
            await asyncio.sleep(0.5)

        data = await get_data(command_process.stdout, command_process.stderr)
        if data:
            command_data += f"{data} \n"
        command_data += f"\n{command_process.returncode}"
        await m.edit(content=f"```{command_data[-1900:]}```")
        await ctx.okay(True)

    @utils.redis_channel("test")
    async def test(self, payload:dict):
        channel = self.bot.get_channel(765242901889810443)
        await channel.send(payload)

def setup(bot:utils.Bot):
    x = OwnerOnly(bot)
    bot.add_cog(x)