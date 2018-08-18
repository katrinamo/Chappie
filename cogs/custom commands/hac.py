import discord
from discord.ext import commands

from ..utils import checks


class HAC:
    """Health Anxiety Community commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.in_guilds(351371821138051093, 342082813790781440)
    async def panic(self, ctx):
        """Alerts others of a panic attack."""

        guild = ctx.guild
        author = ctx.author
        support_channel = discord.utils.get(
            guild.text_channels, name="support-panic-attacks")
        everyone = guild.roles[0]

        channel_msg = f"Hello {author.mention}, I see you're having a panic attack. Please move to the " \
                      f"{support_channel.mention} where we can better assist you."
        support_msg = f"Is there anyone @here who can assist {author.mention}?"

        await ctx.send(channel_msg)
        await support_channel.send(support_msg)
        await support_channel.set_permissions(everyone, send_messages=True)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @checks.in_guilds(351371821138051093, 342082813790781440)
    @checks.in_channels("support-panic-attacks")
    async def solved(self, ctx):
        """Purges the panic attack channel."""

        channel = ctx.channel
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name="@everyone")
        msg = "To use this chat room please type in **!panic** in a different chat room first. " \
              "This will alert anyone online to help you. This room is for **panic attacks**, " \
              "if you're looking for support please use our support chat rooms for that."

        await channel.purge(limit=999)
        await channel.set_permissions(role, send_messages=False)
        await channel.send(msg)


def setup(bot):
    cog = HAC(bot)
    bot.add_cog(cog)
