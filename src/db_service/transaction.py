from sqlalchemy import select, update, Transaction
from sqlalchemy.orm import selectinload

from src.database import async_session
from src.models.categories import Category, Subcategory
from src.models.payments import PaymentAccount
from src.models.users import User


async def get_all_currencies():
    async with async_session() as session:
        return (await session.scalars(select(Subcategory))).all()

async def get_all_categories():
    async with async_session() as session:
        return (await session.scalars(select(Category))).all()

async def get_subcategories(category_id):
    async with (async_session() as session):
        result = await session.scalars(
            select(Subcategory)
        .where(Subcategory.category_id == category_id)
        .options(selectinload(Subcategory.category))
        )
        return result.all()

async def update_payment_account(tg_id: int, additional_amount: int,payment_account_id: int):
    async with async_session() as session:
        user_id = await session.scalar(select(User.id).where(User.tg_id == tg_id))
        await session.execute(
            update(PaymentAccount).where(PaymentAccount.user_id == user_id, PaymentAccount.id == payment_account_id).values(
                amount=PaymentAccount.amount + additional_amount))
        await session.commit()

async def subtract_payment_account(tg_id: int, additional_amount: int,payment_account_id: int, category_id: int, subcategory_id: int):
    async with async_session() as session:
        user_id = await session.scalar(select(User.id).where(User.tg_id == tg_id))
        await session.execute(
            update(Transaction).where(PaymentAccount.user_id == user_id, PaymentAccount.id == payment_account_id,
                                      category_id=category_id,subcategory_id=subcategory_id ).values(
                amount=PaymentAccount.amount - additional_amount))
        await session.commit()