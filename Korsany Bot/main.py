import asyncio

from aiogram import Bot, Dispatcher

import config
from handlers import user_commands, bot_messages


bot = Bot(config.tg_token, parse_mode='HTML')
dp = Dispatcher()

ml_admin = [5193123666, 6854009493, 6536683594]


async def main():
    dp.include_routers(
        user_commands.router,
        bot_messages.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
  asyncio.run(main())