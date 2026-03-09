from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart
import src.states.users as st
import src.db_service.users as user_db
from src.buttons.account_operations import add_account, select_currency_kb
from src.buttons.profile import main_kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await user_db.set_user(message.from_user.id)
    await message.answer(
        "🌟*Добро пожаловать в Финансового бота!!!*🌟",
        reply_markup=main_kb,
        parse_mode="Markdown",
    )

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "🌟*Добро пожаловать в Финансового бота!!!*🌟",
        reply_markup=main_kb,
        parse_mode="Markdown",
    )

@router.callback_query(F.data == "my_accounts")
async def my_accounts(callback: CallbackQuery):
    await callback.answer("")
    accounts = await user_db.get_accounts(callback.from_user.id)
    account_text = "\n".join(
        f"{account.name}|{account.amount}{account.currency.name}\n\n" for account in accounts) if accounts else "Нет счетов"
    await callback.message.edit_text(text=f"📋 *Мои счета:*\n\n{account_text}",
                                     reply_markup=add_account)


"""Создание счёта"""
@router.callback_query(F.data == "add_an_invoice")
async def entry_account_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await callback.message.answer("Введите название счёта", parse_mode="Markdown")
    await state.set_state(st.EntryAccountInKB.entry_account_name)


@router.message(st.EntryAccountInKB.entry_account_name)
async def entry_account_currency(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer("Выберите валюту", reply_markup=await select_currency_kb())


@router.callback_query(F.data.startswith("select_currency_"))
async def entry_account_amount(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    currency_id = int(callback.data.split("_")[-1])
    await state.update_data(currency_id=currency_id)
    await callback.message.answer("Введите сумму счёта")
    await state.set_state(st.EntryAccountInKB.entry_account_amount)


@router.message(st.EntryAccountInKB.entry_account_amount)
async def entry_account_ok(message: Message, state: FSMContext):
    amount = int(message.text)
    data = await state.get_data()
    name = data.get("name")
    currency_id = data.get("currency_id")
    await user_db.add_payment_account(
        tg_id=message.from_user.id,
        name=name,
        amount=amount,
        currency_id=currency_id,
    )
    accounts = await user_db.get_accounts(message.from_user.id)
    account_text = "\n".join(
        f"{account.name}|{account.amount}{account.currency.name}\n\n" for account in accounts) if accounts else "Нет счетов"
    await message.answer(text=f"✅Счёт успешно добавлен!\n\n📋 *Мои счета:*\n\n{account_text}",
                                     reply_markup=add_account)
    await state.clear()


