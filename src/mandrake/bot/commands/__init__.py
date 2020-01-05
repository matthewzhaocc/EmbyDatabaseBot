# TODO: imports
from typing import Tuple, Optional, Union
import discord
import re
from mandrake import errors, config

# Thanks to xSke/PluralKit's legacy branch

def find_with_predicate(s: str, pred) -> int:
    for i, v in enumerate(s):
        if pred(v):
            return i
    return -1

def next_arg(arg_string: str) -> Tuple[str, Optional[str]]:
    # A basic quoted-arg parser

    for quote in "“‟”":
        arg_string = arg_string.replace(quote, "\"")

    if arg_string.startswith("\""):
        end_quote = arg_string[1:].find("\"") + 1
        if end_quote > 0:
            return arg_string[1:end_quote], arg_string[end_quote + 1:].strip()
        else:
            return arg_string[1:], None

    next_space = find_with_predicate(arg_string, lambda ch: ch.isspace())
    if next_space >= 0:
        return arg_string[:next_space].strip(), arg_string[next_space:].strip()
    else:
        return arg_string.strip(), None

class CommandContext:
    client: discord.Client
    message: discord.Message
    config: config.Config

    def __init__(self, client: discord.Client, message: discord.Message, conn, config, args: str): # , conn
        self.client = client
        self.message = message
        self.conn = conn
        self.config = config
        self.args = args

    # Argument parser
    def pop_str(self) -> Optional[str]: #  error: CommandError = None
        if not self.args:
            #if error:
                #raise error
            return None

        popped, self.args = next_arg(self.args)
        return popped

    def peek_str(self) -> Optional[str]:
        if not self.args:
            return None
        popped, _ = next_arg(self.args)
        return popped

    def match(self, next) -> bool:
        peeked = self.peek_str()
        if peeked and peeked.lower() == next.lower():
            self.pop_str()
            return True
        return False
    
    def remaining(self):
        return self.args

    # react with ok/error

    async def ok_react(self):
        await self.message.add_reaction("\u2705")
    async def error_react(self):
        await self.message.add_reaction("\u274c")

    # define methods that would be submethods of the message object

    async def send(self, content = None, embed = None):
        return await self.message.channel.send(content = content, embed = embed)
    
    async def dm(self, content = None, embed = None):
        return await self.message.author.send(content = content, embed = embed)


# import all de commands

import mandrake.bot.commands.help_commands
import mandrake.bot.commands.misc_commands

async def command_root(ctx: CommandContext):

    # command groups
    if ctx.match("help"):
        await help_commands.command_root(ctx)

    # misc commands
    elif ctx.match("emby"):
        await misc_commands.emby(ctx)
    elif ctx.match("ping"):
        await misc_commands.ping(ctx)
    
    else:
        await ctx.reply("This command does not exist. Maybe try `mn;help`?")

async def run_command(ctx: CommandContext, func):
    try:
        await func(ctx)
    except Exception as e:
        await errors.send_error(ctx, e)


async def command_dispatch(client: discord.Client, message: discord.Message, conn, config) -> bool: # , conn
    prefix = "^(mn(;|!)|<@{}> )".format(client.user.id)
    regex = re.compile(prefix, re.IGNORECASE)

    cmd = message.content
    match = regex.match(cmd)
    if match:
        remaining_string = cmd[match.span()[1]:].strip()
        ctx = CommandContext(
            client=client,
            message=message,
            conn=conn,
            config=config,
            args=remaining_string,
        )
        await run_command(ctx, command_root)
        return True
    return False
