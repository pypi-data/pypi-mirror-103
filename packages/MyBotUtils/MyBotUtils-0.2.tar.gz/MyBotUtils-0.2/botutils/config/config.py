config = """
token = ""
owner_ids = []
prefix = ""

[event_webhooks]
    enabled = false
    default_event_webhook = "" # Will be used if the event webhook is true, but a webhook url is not given
    [webhooks]
        # All of these can either be a bool (enabled or disabled) or a str (webhook url)
        guild_updates = "" #  Used for on_guild_join and on_guild_remove events 
        shard_updates = "" # Used for on_shard_connect, on_shard_disconnect and on_shard_ready events
        bot_ready = "" # Used for on_ready events
        unhandled_errors = "" # Used to log errors that are not handled in the bots error handler

[intents]
    guilds = true  # Guilds - Used for guild join/remove, channel create/delete/update, Bot.get_channel, Bot.guilds, Bot.get_guild.
    members = false  # Members (privileged intent) - Used for member join/remove/update, Member.roles, Member.nick, User.name, Bot.get_user, Guild.get_member etc.
    bans = true  # Bans - Used for member ban/unban.
    emojis = true  # Emojis - Used for guild emojis update, Bot.get_emoji, Guild.emojis.
    integrations = true  # Integrations - Used for guild integrations update.
    webhooks = true  # Webhooks - Used for guild webhooks update.
    invites = true  # Invites - Used for invite create/delete.
    voice_states = true  # Voice states - Used for voice state update, VoiceChannel.members, Member.voice.
    presences = false  # Presences (privileged intent) - Used for member update (for activities and status), Member.status.
    guild_messages = true  # Guild messages - Used for message events in guilds.
    dm_messages = true  # DM messages - Used for message events in DMs.
    guild_reactions = true  # Guild reactions - Used for [raw] reaction add/remove/clear events in guilds.
    dm_reactions = true  # DM reactions - Used for [raw] reaction add/remove/clear events in DMs.
    guild_typing = false  # Guild typing - Used for the typing event in guilds.
    dm_typing = false  # DM typing - Used for the typing event in Dms.

[allowed_mentions]
    everyone = true
    users = true
    roles = true

[embed]
    enabled = true
    footers = []

[presence]
    text = "Testing"
    status = "online"
    activity = "playing"
    include_shard_id = true

[database]
    enabled = false
    user = "database_username"
    password = "database_password"
    database = "database_name"
    host = "127.0.0.1"
    port = 5432

[database_cache]
    enabled = true

    [[database_cache.databases]]
        table = "guild_settings"
        primary_key = "guild_id"
        variable_name = "guild_settings"

    [[database_cache.databases]]
        table = "user_settings"
        primary_key = "guild_id"
        variable_name = "user_settings"

[redis]
    enabled = false
    host = "127.0.0.1"
    port = 6379
    db = 0
"""