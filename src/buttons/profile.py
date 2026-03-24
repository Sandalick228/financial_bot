from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



main_kb = InlineKeyboardMarkup(
    inline_keyboard=[
    [InlineKeyboardButton(text='Пополнение', callback_data='depositing'),
    InlineKeyboardButton(text='Расход', callback_data='expense')],
    [InlineKeyboardButton(text='Мои счета', callback_data='my_accounts'),
    InlineKeyboardButton(text='Статистика', callback_data='statistics')]
    ]
)

back_to_main_kb = InlineKeyboardMarkup(
    inline_keyboard=[
    [InlineKeyboardButton(text='◀️ Назад', callback_data='back_to_main')]
    ]
)
