import copy
import datetime
import discord
from contextlib import redirect_stdout
from discord.ext import commands
from io import StringIO
from textwrap import indent
from traceback import format_exc
from ..utils import *

class CogConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str) -> commands.Cog:
        cog = ctx.bot.get_cog(argument)
        if cog is None:
            raise commands.ExtensionNotFound(argument)
        return cog


class AnyChannel(commands.Converter):
    """
    Attempts to convert any Discord ID to a valid Discord Text Channel, Voice Channel, etc

    Taken from the `GlobalChannel` converter from https://github.com/Rapptz/RoboDanny/blob/644e588851bccca24f220b74f0ef091c48299757/cogs/admin.py
    """

    async def convert(self, ctx: commands.Context, argument: str):
        try:
            return await commands.TextChannelConverter().convert(argument)
        except commands.BadArgument:
            try:
                channel_id = int(argument, base=10)
            except ValueError:
                # couldn't convert argument to channel id
                raise commands.BadArgument(f"Couldn't convert {argument!r} to a global channel ID")
            else:
                channel = ctx.bot.get_channel(channel_id)
                if channel is not None:
                    raise commands.BadArgument(f"No channel with ID {argument!r} found")



class Meta(commands.Cog):
    """
    Default commands and listeners and stuffs
    """

    def __init__(self, bot):
        self.bot = bot
    
    @staticmethod
    def _cleanup_code(content: str) -> str:
        """Automatically removes code blocks from the code.

        This is just used for the `execute` command at this time
        
        Parameters
        ----------
        content : str
            The content to remove code blocks from
        
        Returns
        -------
        The cleaned content as a string
        """

        # remove \`\`\`py\n\`\`\`
        if content.startswith('```') and content.endswith('```'):
            if content[-4] == '\n':
                return '\n'.join(content.split('\n')[1:-1])
            return '\n'.join(content.split('\n')[1:]).rstrip('`')

        # remove `foo`
        return content.strip('` \n')

    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True)
    @commands.command()
    async def execute(self, ctx: commands.Context, *, content: str):
        """
        Evaluates some python code
        Gracefully stolen from Rapptz ->
        https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/admin.py#L72-L117
        """

        # make the environment
        # this allows you to reference particular
        # variables in your block of code in discord
        # if you want to get technical, this is an
        # implementation of a Symbol Table
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'self': self
        }
        env.update(globals())

        # make code and output string
        content = self._cleanup_code(content)
        stdout = StringIO()
        to_compile = f'async def func():\n{indent(content, "  ")}'

        # create the function to be ran
        try:
            exec(to_compile, env)
        except Exception as e:
            # compilation error
            # send the error in a code block
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        # execute the function we just made
        func = env["func"]
        try:
            # force stdout into StringIO
            with redirect_stdout(stdout):
                # run our function
                ret = await func()
        except Exception:
            # runtime error
            # output the error in a code block
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{format_exc()}\n```')
        else:
            # hey we didn't goof up

            # react with a white check mark to show that it ran
            try:
                await ctx.message.add_reaction("\u2705")
            except Exception:
                pass

            # if nothing was returned, it might have printed something
            value = stdout.getvalue()
            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                text = f'```py\n{value}{ret}\n```'

                # character limits are a thing
                if len(text) > 2000:
                    # over max limit
                    # send output in a file
                    return await ctx.send(
                        file=discord.File(StringIO('\n'.join(text.split('\n')[1:-1])),
                                          filename='ev.txt')
                    )
                await ctx.send(text)
    
    @commands.is_owner()
    @commands.command(name="sudo")
    async def sudo_command(self, ctx: commands.Context, channel: Optional[AnyChannel], user: Union[discord.Member, discord.User], *, command: str):
        """
        Executes a command as another user, in another channel

        The `channel` parameter is optional and defaults to the current channel if not supplied, and does not have to be a channel from the current guild
        """

        message = copy.copy(ctx.message)
        channel = channel or ctx.channel
        
        # reconstruct message so that it points in the other channel
        message.channel = channel
        message.author = user
        message.content = ctx.prefix + command
        context = await self.bot.get_context(message, cls=type(ctx))
        await self.bot.invoke(context)

    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True)
    @commands.group(name="cog")
    async def _cog_group(self, ctx: commands.Context):
        """
        Cog related commands and utilities
        """

        import copy

        pass

    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True)
    @_cog_group.command(name="list")
    async def _cog_list_command(self, ctx: commands.Context):
        """
        Lists all cogs currently running on the bot
        """

        await paginate(
            ctx,
            embed_title="Cog List",
            line="`{0}`",
            sequence=list(self.bot.cogs.keys()),
            max_page_size=1024,
            sequence_type_name="cogs",
            author_name=str(self.bot.user),
            author_icon_url=self.bot.user.avatar_url
        )

    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True)
    @_cog_group.command(name="info")
    async def _cog_info_command(self, ctx: commands.Context, cog: CogConverter):
        """
        Returns info about a given cog
        """

        embed = discord.Embed(
            title=f"Cog Info - {cog.qualified_name}",
            description=cog.description if cog.description != "" else "(No Description Provided)",
            color=self.bot.color,
            timestamp=datetime.datetime.utcnow()
        )

        embed.set_author(
            name=str(ctx.bot.user),
            icon_url=ctx.bot.user.avatar_url
        )

        listeners = cog.get_listeners()
        fmt = ', '.join(sorted([f'`{listener[0]}`' for listener in listeners])) if len(listeners) != 0 else "None"

        embed.add_field(
            name=f"Listeners[{len(listeners)}]",
            value=fmt,
            inline=False
        )

        commands = cog.get_commands()
        fmt = ', '.join(sorted([f'`{cmd.name}`' for cmd in commands])) if len(commands) != 0 else "None"
        embed.add_field(
            name=f"Commands[{len(commands)}]",
            value=fmt
        )

        await ctx.send(embed=embed)
    
    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True)
    @_cog_group.command(name="load")
    async def _cog_load_command(self, ctx: commands.Context, cog: str):
        """
        Loads a particular cog
        """

        self.bot.load_extension(cog)
        await self.bot.send_success_embed(ctx, f"Cog `{cog}` was loaded!")
    
    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True)
    @_cog_group.command(name="unload")
    async def _cog_unload_command(self, ctx: commands.Context, cog: str):
        """
        Unloads a particular cog
        """

        self.bot.unload_extension(cog)
        await self.bot.send_success_embed(ctx, f"Cog `{cog}` was unloaded!")
    
    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True)
    @_cog_group.command(name="reload")
    async def _cog_reload_command(self, ctx: commands.Context, cog: str):
        self.bot.unload_extension(cog)
        self.bot.load_extension(cog)
        await self.bot.send_success_embed(ctx, f"Cog `{cog}` was reloaded!")

    @_cog_info_command.error
    async def on_cog_commands_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.ExtensionNotFound):
            await self.bot.send_fail_embed(ctx, f"Cog `{error.name}` was not found")
        elif isinstance(error, commands.ExtensionAlreadyLoaded):
            await self.bot.send_fail_embed(ctx, f"Cog `{error.name}` is already loaded")
        elif isinstance(error, commands.ExtensionNotLoaded):
            await self.bot.send_fail_embed(ctx, f"Cog `{error.name}` is already unloaded")
        elif isinstance(error, commands.NoEntryPointError):
            await self.bot.send_fail_embed(ctx, f"Cog `{error.name}` is missing `setup` entrypoint")
        elif isinstance(error, commands.ExtensionFailed):
            await self.bot.send_fail_embed(ctx, f"Cog {error.name} initiation failed: `{error.original.__class__.__name__}`")
        
        print(error, error.__class__.__name__)

    @_cog_load_command.error
    async def on_cog_load_command_error(self, ctx: commands.Context, error):
        await self.on_cog_commands_error(ctx, error)
    
    @_cog_unload_command.error
    async def on_cog_unload_command_error(self, ctx: commands.Context, error):
        await self.on_cog_commands_error(ctx, error)
