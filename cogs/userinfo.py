import discord
from discord.ext import commands


class Userinfo:
    """User commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='user')
    async def _user(self, ctx):

        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @_user.command(name='info')
    async def _info(self, ctx, *, user: discord.Member = None):
        """Get user info."""

        if user is None:
            user = ctx.author

        voice_state = None if not user.voice else user.voice.channel

        activity = user.activity.name if user.activity is not None else "None"

        em = discord.Embed(
            title=None,
            description=None,
            url=None,
            timestamp=ctx.message.created_at,
            color=discord.Color.blue())
        em.add_field(name='User ID', value=user.id, inline=True)
        em.add_field(name='Nick', value=user.nick, inline=True)
        em.add_field(name='Status', value=user.status, inline=True)
        em.add_field(name='In Voice', value=voice_state, inline=True)
        em.add_field(name='Activity', value=activity, inline=True)
        em.add_field(name='Highest Role', value=user.top_role, inline=True)
        em.add_field(
            name='Account Created',
            value=user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
        em.add_field(
            name='Join Date',
            value=user.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
        em.set_thumbnail(url=user.avatar_url)
        em.set_author(
            name=user.display_name,
            icon_url=user.avatar_url)
        await ctx.send(embed=em)
        await ctx.message.delete()

    @_user.command(name='avi')
    async def _avi(self, ctx, *, user: discord.Member = None):
        """View bigger version of user's avatar."""

        if user is None:
            user = ctx.author

        em = discord.Embed(
            title=None,
            description=None,
            url=None,
            timestamp=ctx.message.created_at,
            color=discord.Color.blue())
        em.set_image(url=user.avatar_url)
        await ctx.send(embed=em)
        await ctx.message.delete()


def setup(bot):
    cog = Userinfo(bot)
    bot.add_cog(cog)
