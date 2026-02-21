from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class PaymentAccount(Base):
    __tablename__ = 'payment_accounts'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(16), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id", ondelete="CASCADE"))
    amount: Mapped[int]
    currency: Mapped["CurrencyDB"] = relationship(back_populates="payment_accounts")

class CurrencyDB(Base):
    __tablename__ = 'currencies'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(16), nullable=True)
    payment_accounts: Mapped[List["PaymentAccount"]] = relationship(back_populates="currency", cascade='all, delete')
