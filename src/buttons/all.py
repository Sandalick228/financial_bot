from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_kb = InlineKeyboardMarkup(
    inline_keyboard=[
    [InlineKeyboardButton(text='Пополнение', callback_data='current_tasks'),
    InlineKeyboardButton(text='Расход', callback_data='completed_tasks')],
    [InlineKeyboardButton(text='Мои счета', callback_data='mark_completed_tasks'),
    InlineKeyboardButton(text='Статистика', callback_data='add_task')],
    [InlineKeyboardButton(text='Настройки', callback_data='delete_task'),
     InlineKeyboardButton(text='Премиум', callback_data='delete_task')]
    ]
)