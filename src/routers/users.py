from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
import src.states.all as st
from src.buttons.all import main_kb, add_account
import src.db_service.users as user_db


router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await user_db.set_user(message.from_user.id)
    await message.answer("🌟*Добро пожаловать в Финансового бота!!!*🌟",
                         reply_markup=main_kb,
                         parse_mode="Markdown")

@router.callback_query(F.data=="back_to_main")
async def back_to_main(callback: CallbackQuery):
    await callback.answer()
    await callback.answer("🌟*Добро пожаловать в Финансового бота!!!*🌟",
                         reply_markup=main_kb,
                         parse_mode="Markdown")
@router.callback_query(F.data=="my_accounts")
async def my_accounts(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Мои счета',
                                  reply_markup=add_account)

@router.callback_query(F.data == 'add_an_invoice')
async def entry_account(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer('Введите название счёта',parse_mode="Markdown")
    await state.set_state(st.EntryAccountInKB.add_an_invoice)

@router.message(st.EntryAccountInKB.add_an_invoice)
async def entry_account_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer('Введите сумму счёта')
    await state.set_state(st.EntryAccountInKB.entry_account)

@router.message(st.EntryAccountInKB.entry_account)
async def entry_account_ok(message: Message, state: FSMContext):
    amount = int(message.text)
    data = await state.get_data()
    name = data.get('name')
    tg_id = message.from_user.id
    await user_db.add_transaction_with_user(tg_id,name,amount)
    await message.answer("✅ Счёт успешно добавлен!", parse_mode="Markdown")
    await state.clear()























