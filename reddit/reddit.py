import asyncio
import os
import time

import discord
from discord.ext import commands

from cogs.utils.dataIO import dataIO

default_settings = {
    "subscriptions": []
}


class Reddit:
    """Reddit commands."""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json("data/reddit/settings.json")
        self.bg_task = self.bot.loop.create_task(self.stream())

    async def stream(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():

            row = await self.select_submission_row()

            if row is not None:
                sub_id = row['sub_id']
                subreddit = row['subreddit']
                author = row['author']
                title = row['title']
                body = row['body']
                url = row['url']
                created = row['created']

                description = body if len(body) < 2040 else body[:2040] + '...'
                date = time.strftime('Posted: %m-%d-%Y at %H:%M:%S', time.localtime(created))

                em = discord.Embed(
                    title=title,
                    description=description,
                    url=url,
                    color=discord.Color.red())
                em.set_footer(text=f"By {author} | r/{subreddit} | ID: {sub_id} | {date}")

                try:
                    channel_id_list = await self.find_all_channels_with_sub(subreddit)

                    for channel_id in channel_id_list:
                        channel = self.bot.get_channel(int(channel_id))
                        await channel.send(embed=em)
                    await self.update_submission_row(sub_id)

                except BaseException:
                    pass

            await asyncio.sleep(3)

    async def find_all_channels_with_sub(self, subreddit):
        master_list = []
        for channel_id, subscriptions in self.settings.items():
            for title, sub_list in subscriptions.items():
                if subreddit in sub_list:
                    master_list.append(channel_id)
        return master_list

    async def select_submission_row(self):

        query = '''
                SELECT * FROM submission
                WHERE read = 'no';
                '''

        row = await self.bot.db.chappie_execute(query=query, is_select=True, fetch_all=False)
        return row

    async def update_submission_row(self, sub_id):

        query = '''
                UPDATE submission
                SET read = 'yes'
                WHERE sub_id = $1;
                '''
        params = (sub_id,)

        await self.bot.db.chappie_execute(query=query, params=params)

    def add_channel(self, channel):
        if str(channel.id) not in self.settings:
            self.settings[str(channel.id)] = default_settings
            self.save_settings()

    def save_settings(self):
        dataIO.save_json("data/reddit/settings.json", self.settings)

    @commands.command()
    async def redditsub(self, ctx, subreddit):
        channel = ctx.channel

        self.add_channel(channel)
        self.settings[str(channel.id)]['subscriptions'].append(subreddit.lower())
        self.save_settings()

        await ctx.send(f"{channel.name}, `ID: {channel.id}` is now subscribed to {subreddit}.")

    @commands.command()
    async def redditunsub(self, ctx, subreddit):
        channel = ctx.channel

        self.add_channel(channel)
        try:
            self.settings[str(channel.id)]['subscriptions'].remove(subreddit.lower())
            self.save_settings()
            await ctx.send(f"{channel.name}, `ID: {channel.id}` is now unsubscribed to {subreddit}.")
        except BaseException:
            await channel.send("Error.")


def check_folders():
    folders = ("data", "data/reddit/")
    for folder in folders:
        if not os.path.exists(folder):
            print("Creating " + folder + " folder...")
            os.makedirs(folder)


def check_files():
    files = {
        "settings.json": {}
    }

    for filename, value in files.items():
        if not os.path.isfile("data/reddit/{}".format(filename)):
            print("Creating empty {}".format(filename))
            dataIO.save_json("data/reddit/{}".format(filename), value)


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Reddit(bot))
