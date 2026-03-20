from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
import src.states.transaction as st
from src.buttons.account_operations import get_category_kb, get_subcategory_kb, get_payment_accounts_kb
import src.db_service.transaction as transaction_db
import src.db_service.users as user_db

router = Router()
"""Пополнение"""
@router.callback_query(F.data == "depositing",)
async def get_all_account(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await state.update_data(is_depositing=True)
    await callback.message.edit_text("Выберите к какому счёту привязана операция",
                                  reply_markup=await get_payment_accounts_kb(callback.from_user.id),
                                  parse_mode="Markdown")

@router.callback_query(F.data.startswith("get_payment_accounts_"))
async def get_categories_kb(callback: CallbackQuery, state: FSMContext):
    payment_account_id = int(callback.data.replace("get_payment_accounts_", ""))
    await state.update_data(payment_account_id=payment_account_id)
    await callback.answer("")
    await callback.message.edit_text("Выберите категорию",
                                  reply_markup=await get_category_kb(),
                                  parse_mode="Markdown")

@router.callback_query(F.data.startswith("get_category_"))
async def select_subcategories_kb(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    category_id = int(callback.data.replace("get_category_", ""))
    await state.update_data(category_id=category_id)
    await callback.message.edit_text("Выберите подкатегорию",
                                  reply_markup=await get_subcategory_kb(category_id),
                                  parse_mode="Markdown")

@router.callback_query(F.data.startswith("get_subcategory_"))
async def enter_amount(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    subcategory_id = int(callback.data.replace("get_subcategory_", ""))
    await state.update_data(subcategory_id=subcategory_id)
    await callback.message.edit_text("Введите сумму пополнения",
                                  parse_mode="Markdown")
    await state.set_state(st.AdditionAccount.entering_the_top_up_amount)

@router.message(st.AdditionAccount.entering_the_top_up_amount)
async def account_operation_ok(message: Message, state: FSMContext):
    amount = int(message.text)
    data = await state.get_data()
    is_depositing = data.get("is_depositing")
    payment_account_id = data.get('payment_account_id')
    subcategory_id = data.get("subcategory_id")
    if is_depositing:
        await transaction_db.add_top_up_transaction(
            tg_id=message.from_user.id,
            additional_amount=amount,
            payment_account_id=payment_account_id,
            subcategory_id = subcategory_id,
        )
    else:
        await transaction_db.add_subtract_transaction(
            tg_id=message.from_user.id,
            subtract_amount=amount,
            payment_account_id=payment_account_id,
            subcategory_id=subcategory_id,
        )
    accounts = await user_db.get_accounts(message.from_user.id)
    account_text = "\n".join(
        f"{account.name}|{account.amount}{account.currency.name}\n\n" for account in accounts)
    await message.edit_text(text=f"✅Транзакция успешно завершена!\n\n📋 *Мои счета:*\n\n{account_text}",parse_mode="Markdown")
    await state.clear()

"""Вычитание"""
@router.callback_query(F.data == "expense")
async def get_all_account(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await state.update_data(is_depositing=False)
    await callback.message.edit_text("Выберите к какому счёту привязана операция",
                                  reply_markup=await get_payment_accounts_kb(callback.from_user.id),
                                  parse_mode="Markdown")
