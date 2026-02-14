from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
