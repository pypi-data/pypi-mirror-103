import asyncio
import logging

from fastapi import FastAPI

from timewheel import TimeWheel
from timewheel.schedule import Schedule

logging.basicConfig(level=logging.INFO)


app = FastAPI()


async def mf():
    print("OLAR")
    await asyncio.sleep(10)


@app.on_event('startup')
async def setup():
    tw = TimeWheel([
        Schedule('my-s', '* * * * *', mf)
    ])
    asyncio.create_task(tw.run())

