from discord.ext import commands

def has_permissions(**permissions):
    def predicate(ctx):
        setattr(ctx.command, 'requires_permissions', permissions)
        return commands.has_permissions(**permissions).predicate(ctx)
    return commands.check(predicate)

def bot_has_permissions(**permissions):
    def predicate(ctx):
        setattr(ctx.command, 'bot_requires_permissions', permissions)
        return commands.bot_has_permissions(**permissions).predicate(ctx)
    return commands.check(prediacte)

def has_role(role):
    def predicate(ctx):
        setattr(ctx.command, 'requires_role', role)
        return commands.has_role(role).predicate(ctx)
    return commands.check(predicate)

def has_any_role(*roles):
    def predicate(ctx):
        setattr(ctx.command, 'requires_any_role', roles)
        return commands.has_any_role(roles).predicate(ctx)
    return commands.check(predicate)

def bot_has_role(role):
    def predicate(ctx):
        setattr(ctx.command, 'bot_requires_role', role)
        return commands.bot_has_role(role).predicate(ctx)
    return commands.check(prediacte)

def bot_has_any_role(*roles):
    def predicate(ctx):
        setattr(ctx.command, 'bot_requires_any_role', roles)
        return commands.bot_has_any_role(roles).predicate(ctx)
    return commands.check(prediacte)

def has_guild_permissions(**permissions):
    def predicate(ctx):
        setattr(ctx.comamnd, 'requires_guild_permissions', permissions)
        return commands.has_guild_permissions(**permissions).predicate(ctx)
    return commands.check(predicate)

def bot_has_guild_permissions(**permissions):
    def predicate(ctx):
        setattr(ctx.command, 'bot_requires_guild_permissions', permissions)
        return commands.bot_has_guild_permissions(**permissions).predicate(ctx)
    return commands.check(predicate)

def dm_only():
    def predicate(ctx):
        setattr(ctx.command, 'requires_dm', True)
        return commands.dm_only().predicate(ctx)
    return commands.check(predicate)

def guild_only():
    def predicate(ctx):
        setattr(ctx.command, 'requires_guild', True)
        return commands.guild_only().predicate(ctx)
    return commands.check(predicate)

def is_owner():
    def predicate(ctx):
        setattr(ctx.command, 'requires_owner', True)
        return commands.is_owner().predicate(ctx)
    return commands.check(predicate)

def is_nsfw():
    def predicate(ctx):
        setattr(ctx.command, 'requires_nsfw', True)
        return commands.is_nsfw().predicate(ctx)
    return commands.check(predicate)