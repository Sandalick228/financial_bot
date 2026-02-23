import asyncio
from aiogram import Bot, Dispatcher
from src.config import TOKEN
from src.database import async_main
from src.routers.users import router as users_router
from src.routers.transaktion import router as transaction_router

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    await async_main()
    dp.include_routers(users_router, transaction_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())