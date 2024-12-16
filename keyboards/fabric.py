

from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import tarifs



def pagination(page: int=0,id: int=1,last:str='',elem: list=None):
    
    from callbacks.peganator import Pagination
    build = InlineKeyboardBuilder()

    if page == 0:

        build.button(
            text = "New Order",
            callback_data=Pagination(action="order", page=page, last=last, data='')
        )
        build.button(
            text = "List of orders",
            callback_data=Pagination(action="list-orders", page=page, last=last, data='')
        )

        build.button(
            text = "Support",
            url="https://t.me/zencodeuz"
        )
        build.adjust(2,1)
    elif page == 1:
        build.button(
            text="◀ Back",
            callback_data=Pagination(action=last, page=page, last=last, data='')
        )
        build.adjust(1) 

    return build.as_markup(resize_keyboard=True)