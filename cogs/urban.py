import json

import discord
from discord.ext import commands


class Urban:
    """Urban Dictionary commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def urban(self, ctx, *, search_terms: str):
        """Urban Dictionary search."""

        search_terms = search_terms.replace(" ", "+")
        url = f"http://api.urbandictionary.com/v0/define?term={search_terms}"
        try:
            session = self.bot.session
            async with session.get(url) as r:
                t = await r.text()
                result = json.loads(t)

            if result["list"]:

                definitions = result['list']
                definition = definitions[0]['definition'][:2048]
                example = definitions[0]['example'][:2048]
                url = definitions[0]['permalink']
                word = definitions[0]['word']

                em = discord.Embed(title=f"{word}",
                                   description=definition,
                                   url=url,
                                   color=discord.Color.dark_blue())
                em.set_author(name="According to Urban Dictionary")
                em.set_footer(text=f"Example: {example}")

                await ctx.send(embed=em)
            else:
                await ctx.send("Your search terms gave no results.")
        except BaseException:
            await ctx.send("Error.")


def setup(bot):
    cog = Urban(bot)
    bot.add_cog(cog)
