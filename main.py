# -*- coding: utf-8 -*-
import logging
import asyncio
from aiogram import Bot, Dispatcher
from callbacks import peganator
from handlers import bot_message
import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token='8019585796:AAFC5dWsCkXs19rP3gea_8xgy-e5OcZg6lA')

async def main():

    dp = Dispatcher()
    dp.include_routers(
    bot_message.router,
        peganator.router,
    )
    
    await  dp.start_polling(bot)
    
if __name__=='__main__':
    asyncio.run(main())