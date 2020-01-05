from mandrake.bot.commands import CommandContext
from mandrake import errors, database

async def ping(ctx: CommandContext):
    await ctx.send(f":ping_pong: Pong! \nPing time: {int(ctx.client.latency*1000)} ms")

async def emby(ctx: CommandContext):
    if ctx.remaining() == None:
        await ctx.error_react()
        return
    try:
        if not await database.check_emby_user(ctx):
            await database.add_emby_user(ctx, ctx.remaining())
            await ctx.ok_react()
        else:
            await ctx.error_react()
            await ctx.dm("You already have an Emby username registered with the bot!")
    except Exception as e:
        await errors.send_error(ctx, e)
        await ctx.error_react()
