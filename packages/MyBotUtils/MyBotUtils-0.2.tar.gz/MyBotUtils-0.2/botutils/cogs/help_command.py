from .. import utils
from discord.ext import commands

class HelpCommand(commands.MinimalHelpCommand):

	filtered_errors = (commands.DisabledCommand, commands.NotOwner)

	async def get_runnable_commands(self, ctx):
		"""
		returns a list of the commands the user can run
		"""

		if await ctx.bot.is_owner(ctx.author):
			return [i for i in ctx.bot.commands if i.name != 'help']

		all_commands = [i for i in ctx.bot.commands if i.enabled is True and i.hidden is False and i.name != 'help']

		valid_commands = {}

		for command in all_commands:
			try:
				command.can_run(ctx)
			except commands.CommandError as error:
				if isinstance(error, self.filtered_errors):
					continue
				try:
					valid_commands[command.cog].append(command)
				except Exception:
					valid_commands[command.cog] = [command]

		return valid_commands

	def get_command_info(self, command):
		"""
		returns a dict of information for a command
		"""

		payload = {}

		payload['description'] = command.short_doc
		if command.requires_permissions:
			payload['permissions'] = command.requires_permissions

		if command.requires_guild_permissions:
			try:
				payload['permissions'].append(command.requires_guild_permissions)
			except Exception:
				payload['permissions'] = command.requires_guild_permissions

		if command.requires_role:
			payload['role'] = comamnd.requires_role

		if command.requires_any_role:
			payload['roles'] = command.requires_role

		if command.requires_dm:
			payload['dm_only'] = True

		if command.requires_guild:
			payload['guild_only'] = True

		if command.requires_nsfw:
			payload['nsfw_only'] = True


