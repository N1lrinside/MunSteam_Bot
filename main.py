import asyncio
import os
import sys
import logging
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.models import async_main


async def main() -> None:
    await async_main()
    bot = Bot(token=os.environ.get('TG_TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')