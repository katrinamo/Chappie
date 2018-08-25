import asyncio
import os

import discord
from discord.ext import commands

from .utils.dataIO import dataIO

default_settings = {
    "audit-log_channel": None,
    "last_known_id": None
}


class Auditlog:
    """Audit-log commands."""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json("data/auditlog/settings.json")
        self.bg_task = self.bot.loop.create_task(self.auditlog_task())

    async def auditlog_task(self):

        await self.bot.wait_until_ready()
        while not self.bot.is_closed():

            for guild in self.bot.guilds:
                async for entry in guild.audit_logs(limit=1):
                    try:
                        last_known_id = self.settings[str(
                            guild.id)]['last_known_id']
                        auditlog_channel = self.settings[str(
                            guild.id)]['audit-log_channel']
                        channel = discord.utils.get(
                            guild.text_channels, name=auditlog_channel)

                        action = entry.action.name
                        user = str(entry.user)
                        entry_id = entry.id
                        target = str(entry.target)
                        extra = entry.extra
                        reason = entry.reason
                        created_at = entry.created_at
                        category = entry.category.name + 'd'

                        if entry_id == last_known_id:
                            continue

                        title = f"{user} {category} {target}"

                        em = discord.Embed(title=title,
                                           description=None,
                                           url=None,
                                           timestamp=created_at,
                                           color=discord.Color.gold())
                        em.add_field(name="Action", value=action)
                        em.add_field(name="Reason", value=reason)
                        em.add_field(name="Extra Information", value=extra)
                        await channel.send(embed=em)
                        self.settings[str(guild.id)
                                      ]['last_known_id'] = entry_id
                        self.save_settings()
                    except BaseException:
                        pass

                await asyncio.sleep(5)

    def add_server(self, guild):
        if str(guild.id) not in self.settings:
            self.settings[str(guild.id)] = default_settings
            self.save_settings()

    def save_settings(self):
        dataIO.save_json("data/auditlog/settings.json", self.settings)

    @commands.command()
    async def auditlog(self, ctx, channel: discord.TextChannel):
        """Sets the audit-log channel."""

        guild = ctx.guild

        self.add_server(guild)
        self.settings[str(guild.id)]['audit-log_channel'] = channel.name
        self.save_settings()

        await ctx.send(f"{channel.name} is the new audit-log channel.")


def check_folders():
    folders = ("data", "data/auditlog/")
    for folder in folders:
        if not os.path.exists(folder):
            print("Creating " + folder + " folder...")
            os.makedirs(folder)


def check_files():
    files = {
        "settings.json": {}
    }

    for filename, value in files.items():
        if not os.path.isfile("data/auditlog/{}".format(filename)):
            print("Creating empty {}".format(filename))
            dataIO.save_json("data/auditlog/{}".format(filename), value)


def setup(bot):
    check_folders()
    check_files()
    cog = Auditlog(bot)
    bot.add_cog(cog)
