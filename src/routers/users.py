from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("🌟_*Добро пожаловать в TaskMaster!*_🌟",
                         parse_mode="Markdown")