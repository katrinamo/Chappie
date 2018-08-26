import datetime

import discord
from discord.ext import commands


class Owner:
    """Owner commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, cog_name: str):
        """Loads a cog."""

        cog = cog_name.strip()
        if "cogs." not in cog:
            cog = "cogs." + cog

        try:
            self.bot.load_extension(cog)
            await ctx.send(f"Loaded {cog}")

        except ModuleNotFoundError:
            await ctx.send(f"No module named '{cog}' was found.")
            return

    @commands.group()
    @commands.is_owner()
    async def unload(self, ctx, ):
        """Unloading cog commands."""

        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @unload.command(name="cog")
    @commands.is_owner()
    async def unload_cog(self, ctx, *, cog_name: str):
        """Unloads a cog."""

        cog = cog_name.strip()
        if "cogs." not in cog:
            cog = "cogs." + cog

        if cog == "cogs.owner":
            await ctx.send("Owner not allowed to be unloaded.")
            return

        self.bot.unload_extension(cog)
        await ctx.send(f"Unloaded {cog}")

    @unload.command(name="all")
    @commands.is_owner()
    async def unload_all(self, ctx):
        """Unloads all cogs."""

        for cog in self.bot.initial_extensions:
            if cog == "cogs.owner":
                continue
            self.bot.unload_extension(cog)

        await ctx.send("All cogs, except owner, have been unloaded.")

    @commands.command(name="reload")
    @commands.is_owner()
    async def _reload(self, ctx, *, cog_name: str):
        """Reloads a cog."""

        cog = cog_name.strip()
        if "cogs." not in cog:
            cog = "cogs." + cog

        if cog == "cogs.owner":
            await ctx.send("Owner not allowed to be unloaded.")
            return

        self.bot.unload_extension(cog)
        self.bot.load_extension(cog)
        await ctx.send(f"Reloaded {cog}")

    @commands.group()
    @commands.is_owner()
    async def set(self, ctx):
        """Set commands."""

        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @set.command()
    @commands.is_owner()
    async def nickname(self, ctx, *, nickname: str):
        """Sets Chappie's nickname."""

        await ctx.guild.me.edit(nick=nickname)
        await ctx.send("Done.")

    @set.command()
    @commands.is_owner()
    async def playing(self, ctx, *, name: str):
        """Sets Chappie's playing status."""

        type = discord.ActivityType.playing
        activity = discord.Activity(name=name, type=type)
        await self.bot.change_presence(activity=activity)
        await ctx.send("Done.")

    @set.command()
    @commands.is_owner()
    async def watching(self, ctx, *, name: str):
        """Sets Chappie's watching status."""

        type = discord.ActivityType.watching
        activity = discord.Activity(name=name, type=type)
        await self.bot.change_presence(activity=activity)
        await ctx.send("Done.")

    @set.command()
    @commands.is_owner()
    async def streaming(self, ctx, *, name: str):
        """Sets Chappie's streaming status."""

        type = discord.ActivityType.streaming
        activity = discord.Activity(
            name=name, url='https://www.twitch.tv/philzeey/', type=type)
        await self.bot.change_presence(activity=activity)
        await ctx.send("Done.")

    @set.command()
    @commands.is_owner()
    async def listening(self, ctx, *, name: str):
        """Sets Chappie's listening status."""

        type = discord.ActivityType.listening
        activity = discord.Activity(name=name, type=type)
        await self.bot.change_presence(activity=activity)
        await ctx.send("Done.")

    @set.command()
    @commands.is_owner()
    async def status(self, ctx, status=None):
        """Sets Chappie's status."""

        statuses = {
            "online": discord.Status.online,
            "idle": discord.Status.idle,
            "dnd": discord.Status.dnd,
            "offline": discord.Status.offline,
            "invisible": discord.Status.invisible
        }

        status = statuses.get(status.lower(), None)

        await self.bot.change_presence(status=status)
        await ctx.send("Done.")

    @set.command()
    @commands.is_owner()
    async def avatar(self, ctx, url):
        """Sets Chappie's avatar."""

        session = self.bot.session
        async with session.get(url) as r:
            data = await r.read()
        await self.bot.user.edit(password=self.bot.config["BOT_ACCOUNT_PASSWORD"], avatar=data)
        await ctx.send("Done.")

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shuts down Chappie."""

        wave = "\N{WAVING HAND SIGN}"
        skin = "\N{EMOJI MODIFIER FITZPATRICK TYPE-3}"

        await ctx.send("Shutting down... " + wave + skin)
        await self.bot.logout()


def setup(bot):
    cog = Owner(bot)
    bot.add_cog(cog)
