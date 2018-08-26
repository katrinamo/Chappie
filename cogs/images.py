import json
from random import randint

from discord.ext import commands


class Images:
    """Images commands."""

    def __init__(self, bot):
        self.bot = bot
        self.CLIENT_ID = self.bot.config["IMGUR_CLIENT_ID"]
        self.CLIENT_SECRET = self.bot.config["IMGUR_CLIENT_SECRET"]
        self.GIPHY_API_KEY = self.bot.config["GIPHY_API_KEY"]

    @commands.group()
    async def imgur(self, ctx):
        """Imgur commands."""

        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @imgur.command()
    async def top(self, ctx, search_terms: str):
        """Retrieves the first picture from imgur."""

        search_terms = search_terms.replace(" ", "+")
        querystring = {"q": f"{search_terms}", "mature": "true"}
        headers = {"Authorization": f"Client-ID {self.CLIENT_ID}"}
        url = f"https://api.imgur.com/3/gallery/search/viral/all/0"

        try:
            session = self.bot.session
            async with session.get(url, headers=headers, params=querystring) as r:
                t = await r.text()
                result = json.loads(t)

            if result["data"]:
                await ctx.send(result["data"][0]["link"])

            else:
                await ctx.send("Your search terms gave no results.")

        except BaseException:
            await ctx.send("Error.")

    @imgur.command()
    async def random(self, ctx, *, search_terms: str):
        """Retrieves a random image from Imgur."""

        search_terms = search_terms.replace(" ", "+")
        querystring = {"q": f"{search_terms}", "mature": "true"}
        headers = {"Authorization": f"Client-ID {self.CLIENT_ID}"}
        url = f"https://api.imgur.com/3/gallery/search/time/all/0"

        try:
            session = self.bot.session
            async with session.get(url, headers=headers, params=querystring) as r:
                t = await r.text()
                result = json.loads(t)

            if result["data"]:
                random = randint(0, len(result["data"]))
                await ctx.send(result["data"][random]["link"])

            else:
                await ctx.send("Your search terms gave no results.")

        except BaseException:
            await ctx.send("Error.")

    @commands.group()
    async def gif(self, ctx):
        """Gif commands."""

        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @gif.command()
    async def top(self, ctx, *, search_terms: str):
        """Retrieves the first gif from giphy."""

        search_terms = search_terms.replace(" ", "+")
        url = f"http://api.giphy.com/v1/gifs/search?&api_key={self.GIPHY_API_KEY}&q={search_terms}"

        try:
            session = self.bot.session
            async with session.get(url) as r:
                t = await r.text()
                result = json.loads(t)

            if result["data"]:
                await ctx.send(result["data"][0]["url"])

            else:
                await ctx.send("Your search terms gave no results.")

        except BaseException:
            await ctx.send("Error.")

    @gif.command()
    async def random(self, ctx, search_terms: str):
        """Retrieves a random gif from giphy."""

        search_terms = search_terms.replace(" ", "+")
        url = f"http://api.giphy.com/v1/gifs/search?&api_key={self.GIPHY_API_KEY}&q={search_terms}"

        try:
            session = self.bot.session
            async with session.get(url) as r:
                t = await r.text()
                result = json.loads(t)

            if result["data"]:
                random = randint(0, len(result["data"]))
                await ctx.send(result["data"][random]["url"])

            else:
                await ctx.send("Your search terms gave no results.")

        except BaseException:
            await ctx.send("Error.")


def setup(bot):
    cog = Images(bot)
    bot.add_cog(cog)
