import discord
from discord.ext import commands


class Mod:
    """Mod commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason: str = None):
        """Kicks user."""

        author = ctx.author
        guild = ctx.guild

        if author == user:
            await ctx.send("I cannot let you do that. Self-harm is bad \N{PENSIVE FACE}")
            return

        await guild.kick(user=user, reason=reason)
        await ctx.send("Done. That felt good.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, days_to_delete: int = 0, *, reason: str = None):
        """Bans user."""

        author = ctx.author
        guild = ctx.guild

        if author == user:
            await ctx.send("I cannot let you do that. Self-harm is bad \N{PENSIVE FACE}")
            return

        await guild.ban(user=user, delete_message_days=days_to_delete, reason=reason)
        await ctx.send("Done. That felt good.")

    @commands.group()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx):
        """Mutes user in the channel/server."""

        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @mute.command(name="channel")
    async def mute_channel(self, ctx, user: discord.Member, channel: discord.TextChannel = None):
        """Mutes user in a channel."""

        guild = ctx.guild

        if channel is None:
            channel = ctx.channel

        await channel.set_permissions(user, send_messages=False)
        await ctx.send(f"User has been muted in {channel.name}")
        await user.send(f"Hello, you have been **muted** in {channel.name} by the mods of {guild.name}. If you have "
                        f"questions as to the reason why, please contact the mods. Thank you.")

    @mute.command(name="server")
    async def mute_server(self, ctx, user: discord.Member):
        """Mutes user in the server."""

        guild = ctx.guild

        for channel in guild.text_channels:
            await channel.set_permissions(user, send_messages=False)
        await ctx.send("User has been muted in all channels.")
        await user.send(f"Hello, you have been **muted** in all channels by the mods of {guild.name}. If you have "
                        f"questions as to the reason why, please contact the mods. Thank you.")

    @commands.group()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx):
        """Unmutes user in the channel/server."""

        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @unmute.command(name="channel")
    async def unmute_channel(self, ctx, user: discord.Member, channel: discord.TextChannel = None):
        """Unmutes user in a channel."""

        guild = ctx.guild

        if channel is None:
            channel = ctx.channel

        overwrite_perm = discord.PermissionOverwrite(send_messages=None)
        await channel.set_permissions(user, overwrite=overwrite_perm)
        await ctx.send("User has been unmuted in this channel.")
        await user.send(f"Hello again, it looks like you have been **unmuted** in {channel.name} by the mods of "
                        f"{guild.name}. Feel free to come and chat.")

    @unmute.command(name="server")
    async def unmute_server(self, ctx, user: discord.Member):
        """Unmutes user in the server."""

        guild = ctx.guild

        overwrite_perm = discord.PermissionOverwrite(send_messages=None)
        for channel in guild.text_channels:
            await channel.set_permissions(user, overwrite=overwrite_perm)
        await ctx.send("User has been unmuted in all applicable channels.")
        await user.send(f"Hello again, it looks like you have been **unmuted** in all channels by the mods of "
                        f"{guild.name}. Feel free to come and chat.")

    @commands.command()
    @commands.has_permissions(manage_messages=True, read_message_history=True)
    async def purge(self, ctx, amount: int = 100, channel: discord.TextChannel = None):
        """Purge X amount of messages from channel. Defaults to 100"""

        if channel is None:
            channel = ctx.channel

        await ctx.message.delete()
        await channel.purge(limit=amount)

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(self, ctx, user: discord.Member, *, nickname):

        await user.edit(nick=nickname)

        if user.nick is None:
            await ctx.send(f"{user.mention} is back to their default nickname.")
        else:
            await ctx.send(f"{user.mention} is now known as `{user.nick}`.")


def setup(bot):
    cog = Mod(bot)
    bot.add_cog(cog)
