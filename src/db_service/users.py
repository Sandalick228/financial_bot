from sqlalchemy import select, insert

from src.database import async_session
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

async def add_transaction_with_user(tg_id: int,name: str, amount: int, ):
    async with async_session() as session:
        user_id = await session.scalar(select(User.id).where(User.tg_id == tg_id))
        await session.execute(insert(Transaction).values(user_id=user_id,name=name,amount=amount))
        await session.commit()