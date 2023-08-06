from .custom_bot import CustomBot as Bot
from .redis import Redis, RedisChannel
from .database import Database#, DatabaseChannel, postgresql_channel
from .custom_context import CustomContext as Context
from .custom_cog import CustomCog as Cog  
from . import checks

from discord.ext import commands as _dpy

def redis_channel(channel_name):
    def wrapper(func):
        return RedisChannel(channel_name, func)
    return wrapper

# Add command and group to utils so
# 1. I wont have to change all the decorators if i make a child class of `commands.command`
# 2. I wont have to import discord.ext.commands for every cog

def command(*args, **kwargs):
	return _dpy.command(*args, **kwargs)

def group(*args, **kwargs):
	return _dpy.group(*args, **kwargs)