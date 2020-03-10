import asyncpg
from mandrake import errors

async def connect(uri):
    while True:
        try:
            return await asyncpg.create_pool(uri)
        except (ConnectionError, asyncpg.exceptions.CannotConnectNowError):
            print("Failed to connect to database, retrying in 5 seconds...")
            time.sleep(5)

async def create_tables(conn):
    await conn.execute("""create table if not exists embyusers (
        discordid bigint,
        embyuser text,
        primary key (discordid, embyuser)
    )
    """)

async def add_emby_user(ctx, embyuser):
    try:
        row = await ctx.conn.execute("insert into embyusers (discordid, embyuser) values ($1, $2)", ctx.message.author.id, embyuser)
        return True
    except Exception as e:
        await errors.send_error(ctx, e)

async def check_emby_user(ctx):
    if await ctx.conn.fetchrow("select from embyusers where discordid = $1", ctx.message.author.id) is not None:
        return True
