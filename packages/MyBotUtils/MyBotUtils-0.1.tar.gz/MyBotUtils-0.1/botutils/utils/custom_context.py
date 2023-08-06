from discord.ext import commands

class CustomContext(commands.Context):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_slash_command = False

    @property
    def clean_prefix(self):
        return self.prefix.replace(f'<@{self.bot.user.id}>', f"@{self.bot.user.name}").replace(f'<@!{self.bot.user.id}>', f'@{self.bot.user.name}')
    

    async def send(self, content=None, embed=None, file=None, embeddify=None, ignore_error=False, *args, **kwargs):

        if embeddify is None:
            embeddify = self.bot.config['embed']['enabled']

        try:
            await super().send(content=content, embed=embed, file=file, *args, **kwargs)
        except Exception as e:
            if ignore_error:
                return
            raise e

    async def okay(self, ignore_error=False):
        try:
            await self.message.add_reaction("\N{OK HAND SIGN}")
        except Exception as e:
            if ignore_error:
                return
            raise e
