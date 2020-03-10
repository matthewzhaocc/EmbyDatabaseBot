"""initialization stuff"""
import time
import asyncpg
from mandrake import errors

async def connect(uri):
    """connects to db"""
    while True:
        try:
            return await asyncpg.create_pool(uri)
        except (ConnectionError, asyncpg.exceptions.CannotConnectNowError):
            print("Failed to connect to database, retrying in 5 seconds...")
            time.sleep(5)

async def create_tables(conn):
    """initialize db"""
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS embyusers (
        discordid BIGINT,
        embyuser TEXT,
        primary key (discordid, embyuser)
    )
    """) #suggestion, use sqlalchemy

async def add_emby_user(ctx, embyuser):
    """create new user"""
    try:
        row = await ctx.conn.execute("INSERT INTO embyusers (discordid, embyuser) VALUES ($1, $2)", ctx.message.author.id, embyuser)
        return True
    except Exception as e:
        await errors.send_error(ctx, e)

async def check_emby_user(ctx):
    """check if emvy user exists"""
    return await ctx.conn.fetchrow("select from embyusers where discordid = $1", ctx.message.author.id) is not None
