from discord.ext import commands


def in_guilds(*ids):
    def predicate(ctx):
        for guild_id in ids:
            if guild_id == ctx.guild.id:
                return True
        return False
    return commands.check(predicate)


def in_channels(*channel_names):
    def predicate(ctx):
        for channel_name in channel_names:
            if channel_name == ctx.message.channel.name:
                return True
        return False
    return commands.check(predicate)
