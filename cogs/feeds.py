import os

import discord
from discord.ext import commands

from .utils.dataIO import dataIO

default_settings = {
    "default": None,
    "mod-log": None,
}


class Feeds:
    """Channel feed commands."""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json("data/feeds/settings.json")

    async def on_member_remove(self, member):

        guild = member.guild

        await self.modlog_remove(guild, member)

    async def on_member_join(self, member):

        guild = member.guild

        await self.welcome_message(guild, member)
        await self.modlog_join(guild, member)

    async def welcome_message(self, guild, member):

        try:
            default_channel = self.settings[str(guild.id)]['default']
            channel = discord.utils.get(
                guild.text_channels, name=default_channel)
            msg = f"Welcome to {guild.name}, {member.mention}! " \
                  f"Please read our rules before participating in discussion and introduce yourself! " \
                  f"Last but not least, enjoy yourself!"
            await channel.send(msg)

        except BaseException:
            pass

    async def modlog_join(self, guild, member):

        try:
            modlog_channel = self.settings[str(guild.id)]['mod-log']
            channel = discord.utils.get(
                guild.text_channels, name=modlog_channel)
            msg = f"{member.mention} joined the server!"
            await channel.send(msg)

        except BaseException:
            pass

    async def modlog_remove(self, guild, member):

        try:
            modlog_channel = self.settings[str(guild.id)]['mod-log']
            channel = discord.utils.get(
                guild.text_channels, name=modlog_channel)
            msg = f"{member.name} left the server!"
            await channel.send(msg)

        except BaseException:
            pass

    def add_server(self, guild):
        if str(guild.id) not in self.settings:
            self.settings[str(guild.id)] = default_settings
            self.save_settings()

    def save_settings(self):
        dataIO.save_json("data/feeds/settings.json", self.settings)

    @commands.group()
    @commands.has_permissions(manage_channels=True)
    async def feeds(self, ctx):
        """Set channel feeds."""

        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @feeds.command()
    async def default(self, ctx, channel: discord.TextChannel):
        """Sets default feed channel."""

        guild = ctx.guild

        self.add_server(guild)
        self.settings[str(guild.id)]['default'] = channel.name
        self.save_settings()

        await ctx.send(f"{channel.name} is the new default channel.")

    @feeds.command()
    async def modlog(self, ctx, channel: discord.TextChannel):
        """Sets the mod-log feed channel."""

        guild = ctx.guild

        self.add_server(guild)
        self.settings[str(guild.id)]['mod-log'] = channel.name
        self.save_settings()

        await ctx.send(f"{channel.name} is the new modlog channel.")


def check_folders():
    folders = ("data", "data/feeds/")
    for folder in folders:
        if not os.path.exists(folder):
            print("Creating " + folder + " folder...")
            os.makedirs(folder)


def check_files():
    files = {
        "settings.json": {}
    }

    for filename, value in files.items():
        if not os.path.isfile("data/feeds/{}".format(filename)):
            print("Creating empty {}".format(filename))
            dataIO.save_json("data/feeds/{}".format(filename), value)


def setup(bot):
    check_folders()
    check_files()
    cog = Feeds(bot)
    bot.add_cog(cog)
