# app/services/movement.py
import json
from uuid import UUID
from datetime import datetime

import redis
from fastapi import HTTPException, Depends

from dependencies import get_redis
from schemas import MovementEventType, MovementResponse, InventoryResponse
from repositories import InventoryRepository, MovementRepository


class MovementService:
    def __init__(
            self,
            inventory_repo: InventoryRepository,
            movement_repo: MovementRepository,
            redis_client: redis.Redis = Depends(get_redis),
    ):
        self.inventory_repo = inventory_repo
        self.movement_repo = movement_repo
        self.redis_client = redis_client

    async def process_movement(
            self,
            movement_id: UUID,
            event_type: MovementEventType,
            warehouse_code: str,
            product_id: UUID,
            quantity: int,
            timestamp: datetime
    ):
        if event_type == MovementEventType.DEPARTURE:
            await self._process_departure(warehouse_code, product_id, quantity)
        else:
            await self._process_arrival(warehouse_code, product_id, quantity)

        await self.movement_repo.create_movement({
            "movement_id": movement_id,
            "event_type": event_type,
            "warehouse_code": warehouse_code,
            "product_id": product_id,
            "quantity": quantity,
            "timestamp": timestamp
        })

    async def _process_departure(self, warehouse_code, product_id, quantity):
        inventory = await self.inventory_repo.get_inventory(warehouse_code, product_id)

        if not inventory or inventory.quantity < quantity:
            raise ValueError(f"Insufficient stock for product {product_id}")

        await self.inventory_repo.update_quantity(inventory, -quantity)

    async def _process_arrival(self, warehouse_code, product_id, quantity):
        inventory = await self.inventory_repo.get_inventory(warehouse_code, product_id)

        if not inventory:
            await self.inventory_repo.create_inventory(warehouse_code, product_id, quantity)
        else:
            await self.inventory_repo.update_quantity(inventory, quantity)


    async def get_movement_info(self, movement_id: UUID) -> MovementResponse:
        movements = await self.movement_repo.get_movement_details(movement_id)

        if not movements:
            raise HTTPException(status_code=404, detail="Movement not found")

        departure = next((m for m in movements if m.event_type == "departure"), None)
        arrival = next((m for m in movements if m.event_type == "arrival"), None)

        return MovementResponse(
            movement_id=movement_id,
            product_id=movements[0].product_id,
            departure=departure,
            arrival=arrival,
            time_elapsed=str(arrival.timestamp - departure.timestamp) if (departure and arrival) else None,
            quantity_diff=(arrival.quantity - departure.quantity) if (departure and arrival) else None
        )

    async def get_inventory_info(self, warehouse_id: UUID, product_id: UUID) -> InventoryResponse:
        cache_key = f"inventory:{warehouse_id}:{product_id}"

        cached_data = await self.redis_client.get(cache_key)
        if cached_data:
            return json.loads(cached_data)

        data = await self.inventory_repo.get_inventory_state(warehouse_id, product_id)
        if not data:
            raise HTTPException(status_code=404)

        await self.redis_client.set(
            cache_key,
            json.dumps(data),
            ex=60
        )
        return data