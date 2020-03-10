import sys
if sys.platform != "nt":
    # uvloop doesn't work on Windows, therefore an optional dependency
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

import mandrake

print("Starting Bot.")
mandrake.run("/app/mandrake.conf")
