import asyncio
import logging
from functools import partial

from timewheel import TimeWheel
from timewheel.schedule import Schedule

logging.basicConfig(level=logging.INFO)


async def hello():
    print("Hello!")
    await asyncio.sleep(10)


async def bonoro():
    await asyncio.sleep(80)


async def main():
    tm = TimeWheel([Schedule('Bonoro-runner',
                             '* * * * *',
                             bonoro)])
    await tm.run()


asyncio.get_event_loop().run_until_complete(main())
