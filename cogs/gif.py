import json
from random import randint

from discord.ext import commands


class Gif:
    """Gif commands"""

    def __init__(self, bot):
        self.bot = bot
        self.GIPHY_API_KEY = self.bot.config["GIPHY_API_KEY"]

    @commands.group()
    async def gif(self, ctx):
        """Gif commands."""

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
    cog = Gif(bot)
    bot.add_cog(cog)
