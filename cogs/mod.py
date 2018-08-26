import asyncio

import discord
from discord.ext import commands


class Mod:
    """Mod commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason: str = 'Unspecified'):
        """Bans user."""

        author = ctx.author
        guild = ctx.guild

        if author == user:
            await ctx.send("I cannot let you do that. Self-harm is bad \N{PENSIVE FACE}")
            return

        await ctx.send(f"{user.mention} did '**{reason}**' and got the ban hammer!")
        await user.send(f"Hey, sorry about this but... you have been banned from **{guild.name}** by {author} for "
                        f"'**{reason}**'.")
        await guild.ban(user=user, reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def tempban(self, ctx, user: discord.Member, minutes: int, *, reason: str = 'Unspecified'):
        """Temporarily bans user."""

        author = ctx.author
        guild = ctx.guild

        if author == user:
            await ctx.send("I cannot let you do that. Self-harm is bad \N{PENSIVE FACE}")
            return

        await ctx.send(f"{user.mention} did '**{reason}**' and got the ban hammer for {minutes} minutes!")
        await user.send(f"Hey, sorry about this but... you have been temporarily banned from **{guild.name}** by "
                        f"{author} for '**{reason}**' and duration of {minutes} minutes.")
        await guild.ban(user=user, reason=reason)

        await asyncio.sleep(minutes * 60)
        await guild.unban(user=user, reason="Temporary ban lifted.")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason: str = None):
        """Kicks user."""

        author = ctx.author
        guild = ctx.guild

        if author == user:
            await ctx.send("I cannot let you do that. Self-harm is bad \N{PENSIVE FACE}")
            return

        await ctx.send(f"{user.mention} has been kicked for '**{reason}**'!")
        await guild.kick(user=user, reason=reason)

    @commands.command()
    @commands.has_permissions(manage_messages=True, read_message_history=True)
    async def clear(self, ctx, amount: int, channel: discord.TextChannel = None):
        """Clear X amount of messages from channel."""

        if channel is None:
            channel = ctx.channel

        await ctx.message.delete()
        await channel.purge(limit=amount)

        msg = await ctx.send(f"I have cleared `{amount} messages` for ya!")
        await asyncio.sleep(5)
        await msg.delete()

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, user: discord.Member):
        """Mutes user."""

        guild = ctx.guild
        mute_role = discord.utils.get(guild.roles, name='Muted')

        if mute_role is None:
            mute_role = await guild.create_role(name='Muted', color=discord.Color.dark_grey())

        await user.add_roles(mute_role)
        await ctx.send(f"{user.mention} is now muted!")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def tempmute(self, ctx, user: discord.Member, minutes: int):
        """Termporarily mutes user."""

        guild = ctx.guild
        mute_role = discord.utils.get(guild.roles, name='Muted')

        if mute_role is None:
            mute_role = await guild.create_role(name='Muted', color=discord.Color.dark_grey())

        await user.add_roles(mute_role)
        await ctx.send(f"{user.mention} is now muted for {minutes} minutes!")

        await asyncio.sleep(minutes * 60)
        await ctx.send(f"{user.mention} is now unmuted.")
        await user.remove_roles(mute_role)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, user: discord.Member):
        """Unmutes user."""

        guild = ctx.guild
        mute_role = discord.utils.get(guild.roles, name='Muted')

        if mute_role is None:
            mute_role = await guild.create_role(name='Muted', color=discord.Color.dark_grey())

        await user.remove_roles(mute_role)
        await ctx.send(f"{user.mention} is now unmuted.")

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(self, ctx, user: discord.Member, *, nickname):
        """Changes nickname of user."""

        await user.edit(nick=nickname)

        if user.nick is None:
            await ctx.send(f"{user.mention} is back to their default nickname.")
        else:
            await ctx.send(f"{user.mention} is now known as `{user.nick}`.")


def setup(bot):
    cog = Mod(bot)
    bot.add_cog(cog)
