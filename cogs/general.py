import base64
import datetime
import time
from random import choice, randint

import discord
from discord.ext import commands
import json


class General:

    def __init__(self, bot):
        self.bot = bot
        self.stopwatches = {}
        self.ball = [
            "As I see it, yes",
            "It is certain",
            "It is decidedly so",
            "Most likely",
            "Outlook good",
            "Signs point to yes",
            "Without a doubt",
            "Yes",
            "Yes – definitely",
            "You may rely on it",
            "Reply hazy, try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful"]

        self.regionals = {
            'a': '\N{REGIONAL INDICATOR SYMBOL LETTER A}',
            'b': '\N{REGIONAL INDICATOR SYMBOL LETTER B}',
            'c': '\N{REGIONAL INDICATOR SYMBOL LETTER C}',
            'd': '\N{REGIONAL INDICATOR SYMBOL LETTER D}',
            'e': '\N{REGIONAL INDICATOR SYMBOL LETTER E}',
            'f': '\N{REGIONAL INDICATOR SYMBOL LETTER F}',
            'g': '\N{REGIONAL INDICATOR SYMBOL LETTER G}',
            'h': '\N{REGIONAL INDICATOR SYMBOL LETTER H}',
            'i': '\N{REGIONAL INDICATOR SYMBOL LETTER I}',
            'j': '\N{REGIONAL INDICATOR SYMBOL LETTER J}',
            'k': '\N{REGIONAL INDICATOR SYMBOL LETTER K}',
            'l': '\N{REGIONAL INDICATOR SYMBOL LETTER L}',
            'm': '\N{REGIONAL INDICATOR SYMBOL LETTER M}',
            'n': '\N{REGIONAL INDICATOR SYMBOL LETTER N}',
            'o': '\N{REGIONAL INDICATOR SYMBOL LETTER O}',
            'p': '\N{REGIONAL INDICATOR SYMBOL LETTER P}',
            'q': '\N{REGIONAL INDICATOR SYMBOL LETTER Q}',
            'r': '\N{REGIONAL INDICATOR SYMBOL LETTER R}',
            's': '\N{REGIONAL INDICATOR SYMBOL LETTER S}',
            't': '\N{REGIONAL INDICATOR SYMBOL LETTER T}',
            'u': '\N{REGIONAL INDICATOR SYMBOL LETTER U}',
            'v': '\N{REGIONAL INDICATOR SYMBOL LETTER V}',
            'w': '\N{REGIONAL INDICATOR SYMBOL LETTER W}',
            'x': '\N{REGIONAL INDICATOR SYMBOL LETTER X}',
            'y': '\N{REGIONAL INDICATOR SYMBOL LETTER Y}',
            'z': '\N{REGIONAL INDICATOR SYMBOL LETTER Z}',
            '0': '0⃣',
            '1': '1⃣',
            '2': '2⃣',
            '3': '3⃣',
            '4': '4⃣',
            '5': '5⃣',
            '6': '6⃣',
            '7': '7⃣',
            '8': '8⃣',
            '9': '9⃣',
            '!': '\u2757',
            '?': '\u2753'}

    @commands.command()
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def ping(self, ctx):
        """Pong."""

        em = discord.Embed(title=None,
                           description='Pong',
                           url=None,
                           color=0xC0D3C5)

        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def choose(self, ctx, *, choices: str):
        """Chooses a random choice."""

        chosen = choice(choices.split("|"))

        em = discord.Embed(title=None,
                           description=chosen,
                           url=None,
                           color=0xC0D3C5)

        await ctx.send(embed=em)

    @commands.command(name="8ball")
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _8ball(self, ctx, *, question: str):
        """Let the 8ball decide your fate."""

        if not question.endswith('?'):
            return await ctx.send("This is not a question. Try adding a '?'")

        answer = choice(self.ball)

        em = discord.Embed(title=None,
                           description=answer,
                           url=None,
                           color=0xC0D3C5)

        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def react(self, ctx, *, message):
        """Replace letters with regional indicator emojis."""

        await ctx.message.delete()

        message = list(message)
        regional_list = [self.regionals[x.lower()] if x.isalnum() or x in [
            "!", "?"] else x for x in message]
        regional_output = '\u200b'.join(regional_list)

        em = discord.Embed(title=None,
                           description=regional_output,
                           url=None,
                           color=0xC0D3C5)

        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def space(self, ctx, *, message):
        """Add spaces between each letter."""

        await ctx.message.delete()

        if message.split(' ', 1)[0].isdigit():
            spaces = int(message.split(' ', 1)[0]) * ' '
            message = message.split(' ', 1)[1].strip()
            
        else:
            spaces = ' '

        spaced_message = spaces.join(list(message))

        em = discord.Embed(title=None,
                           description=spaced_message,
                           url=None,
                           color=0xC0D3C5)

        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def cookie(self, ctx, user: discord.Member):
        """Give a cookie to someone!"""

        sender = ctx.author.mention
        receiver = user.mention

        msg = f"**{receiver}**, you've been given a cookie by **{sender}**.:cookie:"

        em = discord.Embed(title=None,
                           description=msg,
                           url=None,
                           color=0xC0D3C5)

        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def lmgtfy(self, ctx, *, search_terms: str):
        """Creates a lmgtfy link."""

        search_terms = search_terms.replace(" ", "+")
        url = f"https://lmgtfy.com/?q={search_terms}"

        em = discord.Embed(title='Link',
                           description=search_terms,
                           url=url,
                           color=0xC0D3C5)

        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def stopwatch(self, ctx):
        """Starts/stops stopwatch."""

        author = ctx.author

        if author.id not in self.stopwatches:
            self.stopwatches[author.id] = int(time.perf_counter())
            msg = f"author.mention, your stopwatch started!"

        else:
            tmp = abs(self.stopwatches[author.id] - int(time.perf_counter()))
            tmp = str(datetime.timedelta(seconds=tmp))
            self.stopwatches.pop(author.id, None)
            msg = f"author.mention, your stopwatch stopped! Time: **{tmp}**"

        em = discord.Embed(title=None,
                           description=msg,
                           url=None,
                           color=0xC0D3C5)

        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def roll(self, ctx, number: int = 100):
        """Rolls random number between 1 and X. Defaults to 100."""

        if number > 1:
            n = randint(1, number)
            msg = f":game_die: {n} :game_die:"
            
        else:
            msg = f"Maybe try a number higher than 1?"

        em = discord.Embed(title=None,
                           description=msg,
                           url=None,
                           color=0xC0D3C5)

        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def discrim(self, ctx):
        """Find others who have the same discriminator as you."""

        count = 0
        match = []

        author = ctx.author
        users = self.bot.get_all_members()
        for user in users:
            if user.discriminator == author.discriminator:
                match.append(user)

        em = discord.Embed(
            title='Matching Discriminator Users',
            description=None,
            url=None,
            color=0xC0D3C5)

        for user in match:
            if count == 25:
                break
            em.add_field(name=user.name, value=user.discriminator)
            count += 1

        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def joke(self, ctx):
        """Sends a joke."""

        url = "https://icanhazdadjoke.com/"
        headers = {"Accept": "application/json"}

        await ctx.trigger_typing()
        session = self.bot.session
        async with session.get(url, headers=headers, ) as r:
            t = await r.json()

            em = discord.Embed(
                title=None,
                description=f"{t['joke']}",
                url=None,
                color=0xC0D3C5)

            await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 7, commands.BucketType.user)
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
                                   color=0xC0D3C5)
                em.set_author(name="According to Urban Dictionary")
                em.set_footer(text=f"Example: {example}")

                await ctx.send(embed=em)
                
            else:
                await ctx.send("Your search terms gave no results.")
                
        except BaseException:
            await ctx.send("Error.")


def setup(bot):
    cog = General(bot)
    bot.add_cog(cog)
