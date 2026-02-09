from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class PaymentAccount(Base):
    __tablename__ = 'payment_accounts'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(16), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id", ondelete="CASCADE"))

class Currency(Base):
    __tablename__ = 'currencies'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(16), nullable=True)
