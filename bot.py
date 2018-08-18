import datetime
import sys
import traceback

import aiohttp
import discord
from discord.ext import commands

from cogs.utils.dataIO import dataIO

description = """
"Philzeey's creation - Chappie"
"""

initial_extensions = [
    'cogs.general',
    'cogs.gif',
    'cogs.imgur',
    'cogs.mod',
    'cogs.owner',
    'cogs.player',
    'cogs.serverinfo',
    'cogs.urban',
    'cogs.userinfo'
]


class Chappie(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix="!",
                         description=description,
                         pm_help=None,
                         shard_id=0,
                         status=discord.Status.dnd,
                         activity=discord.Game(name="with humans"),
                         fetch_offline_members=False,
                         help_attrs=dict(hidden=True))

        self.uptime = datetime.datetime.utcnow()
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.config = dataIO.load_json("data/chappie/config.json")

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(
                    f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()

    async def send_cmd_help(self, ctx):
        if ctx.invoked_subcommand:
            pages = await self.formatter.format_help_for(ctx, ctx.invoked_subcommand)
            for page in pages:
                await ctx.send(page)
        else:
            pages = await self.formatter.format_help_for(ctx, ctx.command)
            for page in pages:
                await ctx.send(page)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.send_cmd_help(ctx)
        elif isinstance(error, commands.BadArgument):
            await self.send_cmd_help(ctx)
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'Command on cool down. Retry after {int(error.retry_after)} seconds.')
        elif isinstance(error, commands.MissingPermissions):
            msg = ',\n'.join(error.args)
            await ctx.author.send(msg)
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Sorry. This command is disabled and cannot be used.')
        elif isinstance(error, commands.CommandInvokeError):
            print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
            traceback.print_tb(error.original.__traceback__)
            print(
                f'{error.original.__class__.__name__}: {error.original}',
                file=sys.stderr)

    async def on_ready(self):
        users = len(set(self.get_all_members()))
        guilds = len(self.guilds)
        channels = len([c for c in self.get_all_channels()])

        login_time = datetime.datetime.utcnow() - self.uptime
        login_time = login_time.seconds + login_time.microseconds / 1E6

        print(f"Login successful. ({login_time} ms)\n")
        print("---------------------")
        print("Chappie - Discord Bot")
        print("---------------------")
        print(str(self.user))
        print("\nConnected to:")
        print("{} servers".format(guilds))
        print("{} channels".format(channels))
        print("{} users\n".format(users))
        print("{} active cogs with {} commands".format(
            len(self.cogs), len(self.commands)))

    async def on_resumed(self):
        print('resumed...')

    async def close(self):
        await super().close()
        await self.session.close()

    def run(self):
        super().run(self.config["BOT_TEST_TOKEN"], reconnect=True)
