from keyboards import  fabric
from aiogram import  Router
from aiogram.filters import Command
from aiogram.types import Message
import db
from utilis.utilis import FormatedText
from config import TextsList

db = db.Database('DB.db')

router = Router()



@router.message(Command('start'))
async def send_welcome(message : Message):
    text = TextsList('start-text',
        {
            "username":message.from_user.username
        }
    )
    text = FormatedText.formatMarkdownV2(text)

    await message.answer(
        text =text,
        reply_markup=fabric.pagination(0,message.from_user.id,'menu'),
        parse_mode='MarkdownV2'
    )
