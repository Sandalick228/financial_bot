from aiogram.types import Message

from aiogram.dispatcher import router
from aiogram.filters import CommandStart


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("🌟_*Добро пожаловать в TaskMaster!*_🌟",
                         parse_mode="Markdown")