try:
    # uvloop doesn't work on Windows, therefore an optional dependency
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

import mandrake

print("Starting Bot.")
mandrake.run("/app/mandrake.conf")