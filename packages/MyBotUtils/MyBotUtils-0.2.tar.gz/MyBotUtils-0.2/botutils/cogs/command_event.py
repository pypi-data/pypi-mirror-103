from .. import utils
class CommandEvent(utils.Cog):

	content_limit = 75

	@utils.Cog.listener()
	async def on_command(self, ctx):
		"""
		Sends a logger message on every command run
		"""

		logger = getattr(ctx.cog, logger)
		message_content = ctx.message.content[:self.content_limit]
		if len(ctx.message.content) > self.content_limit:
			message_content += '...'
		logger.debug(f"Command invoked ({ctx.invoked_with}) ~ {"G" + ctx.guild.id + ' ' if ctx.guild else ''}C{ctx.cahnnel.id} U{ctx.author.id}) :: {message_content}")

def setup(bot:utils.Bot):
	x = CommandEvent(bot)
	bot.add_cog(x)