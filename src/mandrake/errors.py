"""error handling"""
# import discord unused import
import time

async def send_error(ctx, error):
    """sends error to log channel when encountered"""
    if not ctx.config.log_channel:
        return

    log_channel = ctx.client.get_channel(int(ctx.config.log_channel))

    if len(error) >= (2000):
        eid = int(time.time()) #id is a function in python.....
        print(f"Error ID {eid}:")
        print(error)

    await log_channel.send("Error too long, please check your console for error ID {id}.")
