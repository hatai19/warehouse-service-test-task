from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis

from database import async_session
from repositories import InventoryRepository, MovementRepository
from services import MovementService


async def get_db() -> AsyncSession:
    async with async_session as session:
        yield session

def get_inventory_repo(session: AsyncSession = Depends(get_db)):
    return InventoryRepository(session)

def get_movement_repo(session: AsyncSession = Depends(get_db)):
    return MovementRepository(session)

def get_movement_service(
    inventory_repo: InventoryRepository = Depends(get_inventory_repo),
    movement_repo: MovementRepository = Depends(get_movement_repo)
) -> MovementService:
    return MovementService(inventory_repo, movement_repo)

redis_url = "redis://localhost:6379"
async def get_redis():
    client = redis.from_url(redis_url, decode_responses=True)
    try:
        yield client
    finally:
        await client.close()