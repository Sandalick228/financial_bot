from sqlalchemy import select, update
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
        .options(selectinload(Subcategory.sb_category))
        )
        return result.all()

async def update_payment_account(tg_id: int, additional_amount: int,payment_account_id: int):
    async with async_session() as session:
        user_id = await session.scalar(select(User.id).where(User.tg_id == tg_id))
        account_id = await session.scalar(select(PaymentAccount.id).where(PaymentAccount.id == payment_account_id))
        payment_account = await session.scalar(
            select(PaymentAccount).where(PaymentAccount.user_id == user_id, account_id)
        )
        payment_account.amount += additional_amount
        update (await session.execute(
            update(PaymentAccount).where(PaymentAccount.user_id == user_id, PaymentAccount.id == account_id).values(
                amount=PaymentAccount.amount - additional_amount)))
        await session.commit()

async def subtract_payment_account(tg_id: int, additional_amount: int,payment_account_id: int):
    async with async_session() as session:
        user_id = await session.scalar(select(User.id).where(User.tg_id == tg_id))
        account_id = await session.scalar(select(PaymentAccount.id).where(PaymentAccount.id == payment_account_id))
        payment_account = await session.scalar(
            select(PaymentAccount).where(PaymentAccount.user_id == user_id, PaymentAccount.id == account_id)
        )
        payment_account.amount -= additional_amount
        update(await session.execute(
            update(PaymentAccount).where(PaymentAccount.user_id == user_id, PaymentAccount.id == account_id).values(
                amount=PaymentAccount.amount - additional_amount)))
        await session.commit()