from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=True)
    subcategory: Mapped[List["Subcategory"]] = relationship(back_populates="category", cascade='all, delete')

class Subcategory(Base):
    __tablename__ = 'subcategories'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"))
    category: Mapped["Category"] = relationship(back_populates="subcategory")