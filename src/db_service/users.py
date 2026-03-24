from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload

from src.database import async_session
from src.models.categories import Subcategory
from src.models.payments import PaymentAccount, CurrencyDB
from src.models.transactions import Transaction
from src.models.users import User



async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            user = User(
                tg_id=tg_id
            )
            session.add(user)
            await session.commit()
        return user

async def add_payment_account(tg_id: int,name: str, amount: int, currency_id: int):
    async with async_session() as session:
        user_id = await session.scalar(select(User.id).where(User.tg_id == tg_id))
        await session.execute(insert(PaymentAccount).values(user_id=user_id,name=name,amount=amount, currency_id=currency_id))
        await session.commit()

async def get_all_currencies():
    async with async_session() as session:
        return (await session.scalars(select(CurrencyDB))).all()

async def get_accounts(tg_id: int):
    async with async_session() as session:
        user_result = await session.scalar(
            select(User.id).where(User.tg_id == tg_id)
        )
        account_result = await session.scalars(
        select(PaymentAccount)
        .where(PaymentAccount.user_id == user_result)
        .options(selectinload(PaymentAccount.currency))
        )
        return account_result.all()


async def get_statistics(tg_id: int, payment_account_id: int):
    async with async_session() as session:
        user_result = await session.scalar(
            select(User.id).where(User.tg_id == tg_id)
        )
        result = await session.execute(
            select(
                Transaction.amount,
                Transaction.operation_type,
                Subcategory.name.label('subcategory_name')
            ).join(
                Subcategory, Transaction.subcategory_id == Subcategory.id
            ).where(
                Transaction.user_id == user_result,
                Transaction.payment_accounts_id == payment_account_id
            )
        )
        return result.all()
# async def get_statistics(tg_id: int, payment_account_id: int):
#     async with async_session() as session:
#         user_result = await session.scalar(
#             select(User.id).where(User.tg_id == tg_id)
#         )
#         account_result = await session.scalars(
#         select(Transaction).where(Transaction.user_id == user_result,
#                                   Transaction.payment_accounts_id == payment_account_id)
#         )
#         return account_result.all()





