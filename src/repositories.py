from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Inventory, Movement


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


class InventoryRepository(BaseRepository):
    async def get_inventory(self, warehouse_id, product_id):
        result = await self.session.execute(
            select(Inventory)
            .where(Inventory.warehouse_id == warehouse_id)
            .where(Inventory.product_id == product_id)
        )
        return result.scalar_one_or_none()

    async def update_quantity(self, inventory, quantity_delta):
        inventory.quantity += quantity_delta
        self.session.add(inventory)
        await self.session.flush()
        return inventory

    async def create_inventory(self, warehouse_id, product_id, quantity):
        inventory = Inventory(
            warehouse_id=warehouse_id,
            product_id=product_id,
            quantity=quantity
        )
        self.session.add(inventory)
        await self.session.flush()
        return inventory

    async def get_inventory_state(self, warehouse_id: UUID, product_id: UUID):
        result = await self.session.execute(
            select(Inventory)
            .where(Inventory.warehouse_id == warehouse_id)
            .where(Inventory.product_id == product_id)
        )
        return result.scalar_one_or_none()


class MovementRepository(BaseRepository):
    async def create_movement(self, movement_data):
        movement = Movement(**movement_data)
        self.session.add(movement)
        await self.session.flush()
        return movement

    async def get_movement_details(self, movement_id: UUID):
        result = await self.session.execute(
            select(Movement)
            .where(Movement.movement_id == movement_id)
            .order_by(Movement.timestamp)
        )
        return result.scalars().all()

