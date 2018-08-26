import discord
from discord.ext import commands

from .dataIO import dataIO


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


def has_mod_role_or_heirachy():
    settings = dataIO.load_json("data/mod/settings.json")

    def predicate(ctx):
        result = False

        guild = ctx.guild
        author = ctx.author
        author_roles = author.roles
        moderator_roles = find_mod_roles(settings, guild)

        for role in author_roles:
            if role.name in moderator_roles:
                result = True

        roles = []
        for role in moderator_roles:
            r = discord.utils.get(guild.roles, name=role)
            if r is not None:
                roles.append(r)

        for role in roles:
            if author.top_role.position >= role.position:
                result = True
            else:
                result = False

        return result

    return commands.check(predicate)


def find_mod_roles(settings, guild):
    try:
        guild_settings = settings.get(str(guild.id))
        mod_roles = guild_settings.get('moderator_roles')
        return mod_roles
    except BaseException:
        return []
