import discord
from discord.ext import commands


class Info:

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def server(self, ctx):
        """Serverinfo commands."""

        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @server.command(name='info')
    async def server_info(self, ctx):
        """Get various info about the server."""

        await ctx.message.delete()

        guild = ctx.message.guild

        online = 0
        for i in guild.members:
            if str(
                    i.status) == 'online' or str(
                    i.status) == 'idle' or str(
                    i.status) == 'dnd':
                online += 1

        channels = guild.channels
        text_channels = guild.text_channels
        voice_channels = guild.voice_channels
        categories = guild.categories

        role_count = len(guild.roles)
        emoji_count = len(guild.emojis)

        em = discord.Embed(title=None,
                           description=None,
                           url=None,
                           timestamp=ctx.message.created_at,
                           color=discord.Color.red())
        em.add_field(name='Name', value=guild.name)
        em.add_field(name='Owner', value=guild.owner, inline=False)
        em.add_field(name='Region', value=guild.region, inline=False)
        em.add_field(name='Highest role',
                     value=guild.role_hierarchy[0], inline=False)
        em.add_field(name='Members', value=guild.member_count)
        em.add_field(name='Currently Online', value=online)
        em.add_field(name='Text Channels', value=str(len(text_channels)))
        em.add_field(name='Voice Channels', value=str(len(voice_channels)))
        em.add_field(name='Categories', value=str(len(categories)))
        em.add_field(name='All Channels', value=str(len(channels)))
        em.add_field(
            name='Verification Level', value=str(
                guild.verification_level))
        em.add_field(
            name='Explicit Content Filter', value=str(
                guild.explicit_content_filter))

        em.add_field(name='Number of roles', value=str(role_count))
        em.add_field(name='Number of emotes', value=str(emoji_count))
        em.add_field(name='Created At', value=guild.created_at.__format__(
            '%A, %d. %B %Y @ %H:%M:%S'), inline=False)
        em.set_thumbnail(url=guild.icon_url)
        em.set_author(name='Server Info',
                      icon_url=guild.icon_url)
        em.set_footer(text=f'Server ID: {guild.id}')

        await ctx.send(embed=em)

    @server.command(name='emojis')
    async def server_emojis(self, ctx):
        """List all emojis in the server."""

        await ctx.message.delete()

        guild = ctx.message.guild
        emojis = (str(x) for x in guild.emojis)

        await ctx.send("".join(emojis))

    @server.command(name='avi')
    async def server_avi(self, ctx):
        """View a bigger version of server's avatar."""

        await ctx.message.delete()

        guild = ctx.message.guild

        em = discord.Embed(title=None,
                           description=None,
                           url=None,
                           color=0xC0D3C5)
        em.set_image(url=guild.icon_url)

        await ctx.send(embed=em)

    @commands.group(name='user')
    async def user(self, ctx):
        """Userinfo commands."""

        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @user.command(name='info')
    async def user_info(self, ctx, *, user: discord.Member = None):
        """Get various info about a user."""

        await ctx.message.delete()

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

    @user.command(name='avi')
    async def user_avi(self, ctx, *, user: discord.Member = None):
        """View a bigger version of a user's avatar."""

        await ctx.message.delete()

        if user is None:
            user = ctx.author

        em = discord.Embed(title=None,
                           description=None,
                           url=None,
                           color=0xC0D3C5)
        em.set_image(url=user.avatar_url)

        await ctx.send(embed=em)


def setup(bot):
    cog = Info(bot)
    bot.add_cog(cog)
