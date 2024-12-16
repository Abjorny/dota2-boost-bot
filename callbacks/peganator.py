# -*- coding: utf-8 -*-

from aiogram import Router,types
from aiogram.utils.keyboard import CallbackData
from aiogram.fsm.context import  FSMContext
from aiogram.types import CallbackQuery
from aiogram.fsm.state import  State,StatesGroup

from utilis.utilis import FormatedText
from keyboards import fabric
from main import Bot
from config import TextsList
import cryptobot
import db


class FormOrder(StatesGroup):
    current =State()
    desired = State()
    account = State()
    comments =State()


router = Router()
db = db.Database('DB.db')

class Pagination(CallbackData, prefix='pag'):
    action: str
    page: int
    last : str
    data : str




@router.callback_query(Pagination.filter())
async def pagination_handler(call: CallbackQuery, callback_data: Pagination,state: FSMContext,bot:Bot):
    user_data = {
        "user_id":call.message.chat.id,
        "username":call.message.chat.username,
        "firstName":call.message.chat.first_name
    }
    action = callback_data.action
    text = ""
    page = 0
    last = ''
    date = []
    if action == "menu":
        text = TextsList('start-text',user_data)
        page = 0
        last ="menu"
        await state.clear()
        

    elif action == "order":
        text = "*To start the process, please provide the following information:\nYour current MMR?(Enter just a number)*"
        await state.set_state(FormOrder.current)   
        last = "menu"    
        page = 0


    text = FormatedText.formatMarkdownV2(text)
    try:
        mes=  await call.message.edit_text(text,reply_markup=fabric.pagination(page,user_data.get("user_id",1),last,date),parse_mode='MarkdownV2')
        await state.update_data(lastid = mes.message_id)
    except:
        pass

async def edit_message_opros(bot,text,message,date,last = "menu",page = 1):
    await bot.edit_message_text(text,reply_markup=fabric.pagination(page,message.from_user.id,last,[]),parse_mode='MarkdownV2',message_id=date['lastid'],chat_id=message.chat.id)


@router.message(FormOrder.current)
async def send_welcome(message : types.Message,state: FSMContext,bot:Bot):
    await message.delete()
    date = await state.get_data()
    if message.text.isdigit():
        text = "*Your desired MMR?(Enter just a number)*"
        await state.set_state(FormOrder.desired)
        await state.update_data(current = message.text)
    else:
        text = "*Error: you entered the wrong number!\nYour current MMR?(Enter just a number)*"
    text = FormatedText.formatMarkdownV2(text)
    await edit_message_opros(bot,text,message,date)

@router.message(FormOrder.desired)
async def send_welcome(message : types.Message,state: FSMContext,bot:Bot):
    await message.delete()
    date = await state.get_data()
    if message.text.isdigit():
        if int(date['current']) > int(message.text):
            text = "*Your Steam account login and password (required only for boosting, your data is safe with us)?*"
            await state.set_state(FormOrder.account)
            await state.update_data(desired = message.text)
        else:
            text = "*Error: your current MMR is larger than the desired MMR\nYour desired MMR?(Enter just a number)*"
    else:
        text = "*Error: you entered the wrong number!\nYour desired MMR?(Enter just a number)*"

    text = FormatedText.formatMarkdownV2(text)
    
    await edit_message_opros(bot,text,message,date)

@router.message(FormOrder.account)
async def send_welcome(message : types.Message,state: FSMContext,bot:Bot):
    await message.delete()
    date = await state.get_data()
    text = "*Any additional preferences or comments (e.g., specific heroes to play)?*"
    text = FormatedText.formatMarkdownV2(text)
    await state.set_state(FormOrder.comments)
    await state.update_data(account = message.text)
    await edit_message_opros(bot,text,message,date)

@router.message(FormOrder.comments)
async def send_welcome(message : types.Message,state: FSMContext,bot:Bot):
    await message.delete()
    date = await state.get_data()
    current = date['current']
    desired = date['desired']
    delta_mmr = desired - current
    price = delta_mmr // 25 * 4
    await cryptobot.create_payment()
    text = "*will contact you to confirm the details and start the process?*"
    text = FormatedText.formatMarkdownV2(text)
    await state.update_data(comments = message.text)
    await edit_message_opros(bot,text,message,date)