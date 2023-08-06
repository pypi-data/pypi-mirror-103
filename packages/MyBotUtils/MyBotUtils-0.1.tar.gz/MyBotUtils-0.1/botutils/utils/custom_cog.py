from discord.ext import commands
import logging
from cogs import utils

class CustomCog(commands.Cog):
    def __init__(self, bot:utils.Bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        bot_logger = bot.logger
        self.logger = bot_logger.getChild('.'.join(['cog', self.__cog_name__.replace(' ', '')]))

        # Add cog item to all redis channels in our cog
        #self.logger.debug("Adding cog item to all redis channels")
        for attr in dir(self):
            try:
                item = getattr(self, attr)
            except AttributeError:
                continue
            if isinstance(item, utils.RedisChannel):
                item.cog = self