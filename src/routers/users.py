from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from src.buttons.all import main_kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("🌟*Добро пожаловать в Финансового бота!!!*🌟",
                         reply_markup=main_kb,
                         parse_mode="Markdown")