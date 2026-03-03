from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
import src.states.transaktion as st
from src.buttons.account_operations import get_category_kb, get_subcategory_kb, get_payment_accounts_kb
import src.db_service.transaktion as transaction_db

router = Router()
"""Пополнение"""
@router.callback_query(F.data == "depositing",)
async def get_all_account(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.answer("Выберите к какому счёту привязана операция",
                                  reply_markup=await get_payment_accounts_kb(callback.from_user.id),
                                  parse_mode="Markdown")

@router.callback_query(F.data.startswith("sum_accounts_get_"))
async def get_categories_kb(callback: CallbackQuery, state: FSMContext):
    payment_account_id = int(callback.data.replace("sum_accounts_get_", ""))
    await state.update_data(payment_account_id=payment_account_id)
    await callback.answer("")
    await callback.message.answer("Выберите категорию",
                                  reply_markup=await get_category_kb(),
                                  parse_mode="Markdown")

@router.callback_query(F.data.startswith("sum_select_categories_"))
async def select_subcategories_kb(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    category_id = int(callback.data.replace("sum_select_categories_", ""))
    await state.update_data(category_id=category_id)
    await callback.message.answer("Выберите подкатегорию",
                                  reply_markup=await get_subcategory_kb(category_id),
                                  parse_mode="Markdown")

@router.callback_query(F.data.startswith("sum_select_subcategories_"))
async def enter_amount_for_depositing(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    subcategory_id = int(callback.data.replace("sum_select_subcategories_", ""))
    await state.update_data(subcategory_id=subcategory_id)
    await callback.message.answer("Введите сумму пополнения",
                                  parse_mode="Markdown")
    await state.set_state(st.AdditionAccount.entering_the_top_up_amount)

@router.message(st.AdditionAccount.entering_the_top_up_amount)
async def depositing_account_ok(message: Message, state: FSMContext):
    amount = int(message.text)
    data = await state.get_data()
    payment_account_id = data.get('payment_account_id')
    await transaction_db.update_payment_account(
        tg_id=message.from_user.id,
        additional_amount=amount,
        payment_account_id=payment_account_id

    )
    await message.answer("Успешно!",parse_mode="Markdown")
    await state.clear()

"""Вычитание"""
@router.callback_query(F.data == "expense",)
async def get_all_account(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.answer("Выберите к какому счёту привязана операция",
                                  reply_markup=await get_payment_accounts_kb(callback.from_user.id),
                                  parse_mode="Markdown")

@router.callback_query(F.data.startswith("subtract_accounts_get_"))
async def get_categories_kb(callback: CallbackQuery, state: FSMContext):
    payment_account_id = int(callback.data.replace("subtract_accounts_get_", ""))
    await state.update_data(payment_account_id =payment_account_id)
    await callback.answer("")
    await callback.message.answer("Выберите категорию",
                                  reply_markup=await get_category_kb(),
                                  parse_mode="Markdown")

@router.callback_query(F.data.startswith("subtract_select_categories_"))
async def select_subcategories_kb(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    category_id = int(callback.data.replace("subtract_select_categories_", ""))
    await state.update_data(category_id=category_id)
    await callback.message.answer("Выберите подкатегорию",
                                  reply_markup=await get_subcategory_kb(category_id),
                                  parse_mode="Markdown")

@router.callback_query(F.data.startswith("subtract_select_subcategories_"))
async def select_sum_kb(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    subcategory_id = int(callback.data.replace("subtract_select_subcategories_", ""))
    await state.update_data(subcategory_id=subcategory_id)
    await callback.message.answer("Введите сумму вычета",
                                  parse_mode="Markdown")
    await state.set_state(st.SubtractAccount.entering_the_deduction_amount)

@router.message(st.SubtractAccount.entering_the_deduction_amount)
async def consumption_recorded_successfully(message: Message, state: FSMContext):
    amount = int(message.text)
    data = await state.get_data()
    payment_account_id = data.get('payment_account_id')
    await transaction_db.subtract_payment_account(
        tg_id=message.from_user.id,
        additional_amount=amount,
        payment_account_id=payment_account_id

    )
    await message.answer("Успешно!",parse_mode="Markdown")
    await state.clear()