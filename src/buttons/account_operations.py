from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import src.db_service.users as user_db
import src.db_service.transaction as transaction_db

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

async def  get_category_kb():
    categories = await transaction_db.get_all_categories()
    keyboard = InlineKeyboardBuilder()
    for category in categories:
        keyboard.row(InlineKeyboardButton(text=category.name, callback_data=f' get_category_{category.id}'))
    keyboard.row(InlineKeyboardButton(text='◀️ Назад', callback_data='back_to_main'))
    return keyboard.as_markup()

async def  get_subcategory_kb(category_id):
    subcategories = await transaction_db.get_subcategories(category_id)
    keyboard = InlineKeyboardBuilder()
    for subcategory in subcategories:
        keyboard.row(InlineKeyboardButton(text=subcategory.name, callback_data=f' get_subcategory_{subcategory.id}'))
    keyboard.row(InlineKeyboardButton(text='◀️ Назад', callback_data='back_to_main'))
    return keyboard.as_markup()

async def get_payment_accounts_kb(tg_id):
    payment_accounts = await user_db.get_accounts(tg_id)
    items = InlineKeyboardBuilder()
    for payment_account in payment_accounts:
        items.row(InlineKeyboardButton(text=payment_account.name, callback_data=f'get_payment_accounts_{payment_account.id}'))
    items.row(InlineKeyboardButton(text='◀️ Назад', callback_data='back_to_main'))
    return items.as_markup()

