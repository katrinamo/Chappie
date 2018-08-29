import asyncio
import os

import discord
from discord.ext import commands

from cogs.utils.dataIO import dataIO

from cogs.utils import checks

default_settings = {
    "moderator_roles": [],
    "logging_channel": None,
    "join_message": "{member.name} joined the server!",
    "leave_message": "{member.mention} left the server!"
}


class Mod:
    """Mod commands."""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json("data/mod/settings.json")

    @commands.command()
    @checks.has_mod_role_or_heirachy()
    async def ban(self, ctx, user: discord.Member, *, reason: str = 'Unspecified'):
        """Bans user."""

        author = ctx.author
        guild = ctx.guild

        if author == user:
            await ctx.send("I cannot let you do that. Self-harm is bad \N{PENSIVE FACE}")
            return
        if author.top_role.position <= user.top_role.position:
            await ctx.send("Your role is equal or below the user you are trying to moderate. Sorry.")
            return

        await ctx.send(f"{user.mention} did '**{reason}**' and got the ban hammer!")
        await user.send(f"Hey, sorry about this but... you have been banned from **{guild.name}** by {author} for "
                        f"'**{reason}**'.")
        await guild.ban(user=user, reason=reason)

    @commands.command()
    @checks.has_mod_role_or_heirachy()
    async def tempban(self, ctx, user: discord.Member, minutes: int, *, reason: str = 'Unspecified'):
        """Temporarily bans user."""

        author = ctx.author
        guild = ctx.guild

        if author == user:
            await ctx.send("I cannot let you do that. Self-harm is bad \N{PENSIVE FACE}")
            return
        if author.top_role.position <= user.top_role.position:
            await ctx.send("Your role is equal or below the user you are trying to moderate. Sorry.")
            return

        await ctx.send(f"{user.mention} did '**{reason}**' and got the ban hammer for {minutes} minutes!")
        await user.send(f"Hey, sorry about this but... you have been temporarily banned from **{guild.name}** by "
                        f"{author} for '**{reason}**' and duration of {minutes} minutes.")
        await guild.ban(user=user, reason=reason)

        await asyncio.sleep(minutes * 60)
        await guild.unban(user=user, reason="Temporary ban lifted.")

    @commands.command()
    @checks.has_mod_role_or_heirachy()
    async def kick(self, ctx, user: discord.Member, *, reason: str = None):
        """Kicks user."""

        author = ctx.author
        guild = ctx.guild

        if author == user:
            await ctx.send("I cannot let you do that. Self-harm is bad \N{PENSIVE FACE}")
            return
        if author.top_role.position <= user.top_role.position:
            await ctx.send("Your role is equal or below the user you are trying to moderate. Sorry.")
            return

        await ctx.send(f"{user.mention} has been kicked for '**{reason}**'!")
        await guild.kick(user=user, reason=reason)

    @commands.command()
    @checks.has_mod_role_or_heirachy()
    async def clear(self, ctx, amount: int, channel: discord.TextChannel = None):
        """Clear X amount of messages from channel."""

        if channel is None:
            channel = ctx.channel

        await ctx.message.delete()
        await channel.purge(limit=amount)

        msg = await ctx.send(f"I have cleared `{amount} messages` for ya!")
        await asyncio.sleep(5)
        await msg.delete()

    @commands.command()
    @checks.has_mod_role_or_heirachy()
    async def mute(self, ctx, user: discord.Member, *, reason: str = 'Unspecified'):
        """Mutes user."""

        guild = ctx.guild
        author = ctx.author
        mute_role = discord.utils.get(guild.roles, name='Muted')

        if author.top_role.position <= user.top_role.position:
            await ctx.send("Your role is equal or below the user you are trying to moderate. Sorry.")
            return

        if mute_role is None:
            mute_role = await guild.create_role(name='Muted', color=discord.Color.dark_grey())

        await user.add_roles(mute_role)
        await ctx.send(f"{user.mention} ({user.id}) is now muted for '**{reason}**', alright?")

    @commands.command()
    @checks.has_mod_role_or_heirachy()
    async def tempmute(self, ctx, user: discord.Member, minutes: int, reason: str = 'Unspecified'):
        """Temporarily mutes user."""

        guild = ctx.guild
        author = ctx.author
        mute_role = discord.utils.get(guild.roles, name='Muted')

        if author.top_role.position <= user.top_role.position:
            await ctx.send("Your role is equal or below the user you are trying to moderate. Sorry.")
            return

        if mute_role is None:
            mute_role = await guild.create_role(name='Muted', color=discord.Color.dark_grey())

        await user.add_roles(mute_role)
        await ctx.send(f"{user.mention} ({user.id}) is now muted for '**{reason}**' for a duration of {minutes} "
                       f"minutes, alright?")

        await asyncio.sleep(minutes * 60)
        await ctx.send(f"{user.mention} is now unmuted.")
        await user.remove_roles(mute_role)

    @commands.command()
    @checks.has_mod_role_or_heirachy()
    async def unmute(self, ctx, user: discord.Member):
        """Unmutes user."""

        guild = ctx.guild
        author = ctx.author
        mute_role = discord.utils.get(guild.roles, name='Muted')

        if author.top_role.position <= user.top_role.position:
            await ctx.send("Your role is equal or below the user you are trying to moderate. Sorry.")
            return

        if mute_role is None:
            mute_role = await guild.create_role(name='Muted', color=discord.Color.dark_grey())

        await user.remove_roles(mute_role)
        await ctx.send(f"{user.mention} is now unmuted.")

    @commands.command()
    @checks.has_mod_role_or_heirachy()
    async def nickname(self, ctx, user: discord.Member, *, nickname):
        """Changes nickname of user."""

        author = ctx.author
        await user.edit(nick=nickname)

        if author.top_role.position <= user.top_role.position:
            await ctx.send("Your role is equal or below the user you are trying to moderate. Sorry.")
            return

        if user.nick is None:
            await ctx.send(f"{user.mention} is back to their default nickname.")
        else:
            await ctx.send(f"{user.mention} is now known as `{user.nick}`.")

    @commands.command()
    async def modrole(self, ctx, role: discord.Role):
        """Sets a role as a server's moderation role."""

        guild = ctx.guild

        self.add_server(guild)
        if role.name not in self.settings[str(guild.id)]['moderator_roles']:
            self.settings[str(guild.id)]['moderator_roles'].append(role.name)
            self.save_settings()
            await ctx.send(f"`{role.name}` is now a moderator's role for this server.")
        else:
            await ctx.send(f"`{role.name}` is already a moderator's role for this server.")

    @commands.command()
    async def logging(self, ctx, channel: discord.TextChannel):
        """Sets a channel as the server's logging channel."""

        guild = ctx.guild

        self.add_server(guild)
        self.settings[str(guild.id)]['logging_channel'] = channel.name
        self.save_settings()

        await ctx.send(f"`{channel.name}` is now your server's logging channel.")

    def add_server(self, guild):
        if str(guild.id) not in self.settings:
            self.settings[str(guild.id)] = default_settings
            self.save_settings()

    def save_settings(self):
        dataIO.save_json("data/mod/settings.json", self.settings)


def check_folders():
    folders = ("data", "data/mod/")
    for folder in folders:
        if not os.path.exists(folder):
            print("Creating " + folder + " folder...")
            os.makedirs(folder)


def check_files():
    files = {
        "settings.json": {}
    }

    for filename, value in files.items():
        if not os.path.isfile("data/mod/{}".format(filename)):
            print("Creating empty {}".format(filename))
            dataIO.save_json("data/mod/{}".format(filename), value)


def setup(bot):
    check_folders()
    check_files()
    cog = Mod(bot)
    bot.add_cog(cog)
