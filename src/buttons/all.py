from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import src.db_service.users as user_db

main_kb = InlineKeyboardMarkup(
    inline_keyboard=[
    [InlineKeyboardButton(text='Пополнение', callback_data='depositing'),
    InlineKeyboardButton(text='Расход', callback_data='expense')],
    [InlineKeyboardButton(text='Мои счета', callback_data='my_accounts'),
    InlineKeyboardButton(text='Статистика', callback_data='statistics')]
    ]
)

back_to_main = InlineKeyboardMarkup(
    inline_keyboard=[
    [InlineKeyboardButton(text='назад', callback_data='back_to_main')]
    ]
)

add_account = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Добавить счёт', callback_data='add_an_invoice')]]
)


async def select_currency_kb():
    currencies = await user_db.get_all_currencies()
    keyboard = InlineKeyboardBuilder()
    for currency in currencies:
        keyboard.row(InlineKeyboardButton(text=currency.name, callback_data=f'select_currency_{currency.id}'))
    keyboard.row(InlineKeyboardButton(text='◀️ Назад', callback_data='back_to_main'))
    return keyboard.as_markup()
