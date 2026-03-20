from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from src.database import async_session
from src.models.categories import Category, Subcategory
from src.models.payments import PaymentAccount
from src.models.transactions import Transaction
from src.models.users import User


async def get_all_currencies():
    async with async_session() as session:
        return (await session.scalars(select(PaymentAccount))).all()

async def get_all_categories():
    async with async_session() as session:
        return (await session.scalars(select(Category))).all()

async def get_subcategories(category_id):
    async with async_session() as session:
        result = await session.scalars(
            select(Subcategory)
        .where(Subcategory.category_id == category_id)
        .options(selectinload(Subcategory.category))
        )
        return result.all()

async def add_top_up_transaction(tg_id: int, additional_amount: int,payment_account_id: int,subcategory_id: int):
    async with async_session() as session:
        user_id = await session.scalar(select(User.id).where(User.tg_id == tg_id))
        await session.execute(
            update(PaymentAccount).where(PaymentAccount.user_id == user_id, PaymentAccount.id == payment_account_id).values(
                amount=PaymentAccount.amount + additional_amount))
        new_transaction = Transaction(
            user_id = user_id,
            subcategory_id = subcategory_id,
            amount = additional_amount,
            operation_type = True
        )
        session.add(new_transaction)
        await session.commit()

async def add_subtract_transaction(tg_id: int, subtract_amount: int,payment_account_id: int, subcategory_id: int):
    async with async_session() as session:
        user_id = await session.scalar(select(User.id).where(User.tg_id == tg_id))
        await session.execute(
            update(PaymentAccount).where(PaymentAccount.user_id == user_id,
                                         PaymentAccount.id == payment_account_id).values(
                amount=PaymentAccount.amount - subtract_amount))
        new_transaction = Transaction(
            user_id = user_id,
            subcategory_id = subcategory_id,
            amount = subtract_amount,
            operation_type = False
        )
        session.add(new_transaction)
        await session.commit()