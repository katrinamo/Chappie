import os

import discord

from .utils.dataIO import dataIO

default_settings = {
    "mod-log_channel": None,
}


class Modlog:
    """Welcome settings"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json("data/mod/settings.json")

    async def on_member_remove(self, member):

        guild = member.guild

        try:
            modlog_channel = self.settings[str(guild.id)]['logging_channel']
            channel = discord.utils.get(
                guild.text_channels, name=modlog_channel)
            msg = f"{member.name} left the server!"
            await channel.send(msg)

        except BaseException:
            pass

    async def on_member_join(self, member):

        guild = member.guild

        try:
            modlog_channel = self.settings[str(guild.id)]['logging_channel']
            channel = discord.utils.get(
                guild.text_channels, name=modlog_channel)
            msg = f"{member.mention} joined the server!"
            await channel.send(msg)

        except BaseException:
            pass


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
    cog = Modlog(bot)
    bot.add_cog(cog)
