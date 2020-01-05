import asyncio
import sys

import asyncpg
from collections import namedtuple
import discord
import logging
import json
import os
import traceback

from mandrake import database, errors
from mandrake.config import Config
from mandrake.bot import commands

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")

def connect_to_database(uri: str) -> asyncpg.pool.Pool:
    return asyncio.get_event_loop().run_until_complete(database.connect(uri))


def run(config: Config):

    print("Welcome to Mandrake!")

    print("Connecting to database...")
    pool = connect_to_database(config.database_uri)
    print("Connected to database!")

    async def create_tables():
        async with pool.acquire() as conn:
            await database.create_tables(conn)

    asyncio.get_event_loop().run_until_complete(create_tables())

    client = discord.AutoShardedClient()
    
    @client.event
    async def on_ready():
        print("Connected to Discord!\n")
        print(f"Connected as: {str(client.user)} ({str(client.user.id)})")
        print()
        await client.change_presence(activity=discord.Game(name="mn;help \u2014 in {} servers".format(len(client.guilds))))

    @client.event
    async def on_message(message: discord.Message):
        if message.author.bot:
            return

        # Grab a database connection from the pool
        async with pool.acquire() as conn:
            did_run_command = await commands.command_dispatch(client, message, conn, config)
            if did_run_command:
                return

    @client.event
    async def on_error(event_name, *args, **kwargs):
        if not config.log_channel:
            return
        log_channel = client.get_channel(int(config.log_channel))

        traceback_str = "```python\n{}```".format(traceback.format_exc())
        if len(traceback.format_exc()) >= (2000 - len("```python\n```")):
            traceback_str = "```python\n...{}```".format(traceback.format_exc()[- (2000 - len("```python\n...```")):])
        await log_channel.send(content=traceback_str)

    print("Connecting to Discord. Please wait...")
    client.run(config.token)
