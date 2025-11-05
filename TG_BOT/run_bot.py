import asyncio
from create_bot import bot, dp
from handlers.start import start_router
from handlers import inline_router
from db_handlers import db_router


async def main():
    dp.include_routers(
        start_router,
        inline_router,
        db_router
    )
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())