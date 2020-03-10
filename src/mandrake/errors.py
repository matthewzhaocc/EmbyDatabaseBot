import discord
import time

async def send_error(ctx, error):
    if not ctx.config.log_channel:
        return

    log_channel = ctx.client.get_channel(int(ctx.config.log_channel))

    if len(error) >= (2000):
        id = int(time.time())
        print(f"Error ID {id}:")
        print(error)

    await log_channel.send("Error too long, please check your console for error ID {id}.")
