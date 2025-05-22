import enum
from typing import Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy import Column, ForeignKey, String, Enum, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Inventory(Base):
    __tablename__ = "inventory"
    __table_args__ = (
        CheckConstraint('quantity >= 0', name='quantity_non_negative'),
        UniqueConstraint('warehouse_id', 'product_id', name='uq_warehouse_product')
    )

    id: Mapped[UUID] = mapped_column(primary_key=True)
    warehouse_id: Mapped[UUID] = mapped_column(ForeignKey("warehouses.id"))
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(default=0)

    warehouse: Mapped["Warehouse"] = relationship(back_populates="inventory")
    product: Mapped["Product"] = relationship(back_populates="inventory")


class Warehouse(Base):
    __tablename__ = "warehouses"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(10), unique=True)

    inventory: Mapped[list["Inventory"]] = relationship(back_populates="warehouse")
    movements: Mapped[list["Movement"]] = relationship(back_populates="warehouse")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    inventory: Mapped[list["Inventory"]] = relationship(back_populates="product")


class Movement(Base):
    __tablename__ = "movements"

    class EventType(str, enum.Enum):
        ARRIVAL = "arrival"
        DEPARTURE = "departure"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    movement_id: Mapped[UUID] = mapped_column(index=True)
    event_type: Mapped[EventType] = mapped_column(Enum(EventType))


    warehouse_id: Mapped[UUID] = mapped_column(ForeignKey("warehouses.id"))
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column()

    related_warehouse: Mapped[Optional[UUID]] = mapped_column()
    warehouse: Mapped["Warehouse"] = relationship(back_populates="movements")
    product: Mapped["Product"] = relationship()