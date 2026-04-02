from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart
import src.states.users as st
import src.db_service.users as user_db
from src.buttons.account_operations import add_account, select_currency_kb, get_payment_accounts_for_all_statistics_kb, \
    menu_statistic, get_payment_accounts_for_consumption_statistics_kb, get_payment_accounts_for_income_statistics_kb
from src.buttons.profile import main_kb, back_to_main_kb

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
    await callback.message.edit_text("Введите название счёта", parse_mode="Markdown")
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
    await callback.message.edit_text("Введите сумму счёта")
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

"""Статистика"""
@router.callback_query(F.data == "statistics",)
async def menu_statistics(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.edit_text("Выберите какую статистику вы хотите получить",
                                  reply_markup=menu_statistic,
                                  parse_mode="Markdown")

@router.callback_query(F.data == "general_statistics",)
async def my_accounts_for_statistics(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.edit_text("Выберите по какому счёту хотите узнать статистику",
                                  reply_markup=await get_payment_accounts_for_all_statistics_kb(callback.from_user.id),
                                  parse_mode="Markdown")

@router.callback_query(F.data.startswith("get_payment_accounts_for_statist"))
async def get_categories_kb(callback: CallbackQuery):
    payment_account_id = int(callback.data.replace("get_payment_accounts_for_statist_", ""))
    await callback.answer("")
    accounts = await user_db.get_statistics(callback.from_user.id, payment_account_id)
    formatted_transactions = []
    for amount, operation_type, subcategory_name, date in accounts:
        operation_text = " Пополнение" if operation_type else " Расход"
        formatted_amount = f"+{amount} ₽" if operation_type else f"-{amount} ₽"
        formatted_transactions.append(
            f" {date} | {operation_text} : {formatted_amount} ({subcategory_name})"
        )
    account_text = "\n".join(formatted_transactions) if accounts else "Пока что не происходило операций на данном счёте"
    await callback.message.edit_text(
        text=f"📋 *Статистика:*\n\n{account_text}",
        reply_markup=back_to_main_kb,
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "consumption_statistics",)
async def my_accounts_for_statistics(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.edit_text("Выберите по какому счёту хотите узнать статистику",
                                  reply_markup=await get_payment_accounts_for_consumption_statistics_kb(callback.from_user.id),
                                  parse_mode="Markdown")

@router.callback_query(F.data.startswith("get_payment_accounts_for_consumption_statistics"))
async def get_categories_kb(callback: CallbackQuery):
    payment_account_id = int(callback.data.replace("get_payment_accounts_for_consumption_statistics_", ""))
    await callback.answer("")
    accounts = await user_db.get_statistics_consumption(callback.from_user.id, payment_account_id)
    formatted_transactions = []
    for amount, operation_type, subcategory_name in accounts:
        operation_text = "Расход"
        formatted_amount = f"-{amount} ₽"
        formatted_transactions.append(
            f"{operation_text} | {subcategory_name}: {formatted_amount}"
        )
    account_text = "\n".join(formatted_transactions) if accounts else "Пока что не происходило расходов на данном счёте"
    await callback.message.edit_text(
        text=f"📋 *Статистика:*\n\n{account_text}",
        reply_markup=back_to_main_kb,
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "income_statistics",)
async def my_accounts_for_statistics(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.edit_text("Выберите по какому счёту хотите узнать статистику",
                                  reply_markup=await get_payment_accounts_for_income_statistics_kb(callback.from_user.id),
                                  parse_mode="Markdown")

@router.callback_query(F.data.startswith("get_payment_accounts_for_income_statistics"))
async def get_categories_kb(callback: CallbackQuery):
    payment_account_id = int(callback.data.replace("get_payment_accounts_for_income_statistics_", ""))
    await callback.answer("")
    accounts = await user_db.get_statistics_income(callback.from_user.id, payment_account_id)
    formatted_transactions = []
    for amount, operation_type, subcategory_name in accounts:
        operation_text = "Доход"
        formatted_amount = f"+{amount} ₽"
        formatted_transactions.append(
            f"{operation_text} | {subcategory_name}: {formatted_amount}"
        )
    account_text = "\n".join(formatted_transactions) if accounts else "Пока что не происходило пополнений на данном счёте"
    await callback.message.edit_text(
        text=f"📋 *Статистика:*\n\n{account_text}",
        reply_markup=back_to_main_kb,
        parse_mode="Markdown"
    )