import asyncio
import sys
import logging
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.models import async_main


async def main() -> None:
    await async_main()
    bot = Bot(token='7274769206:AAEcDxVPhbmChHLdZFuhrz40BRNQEd-pJzE')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')