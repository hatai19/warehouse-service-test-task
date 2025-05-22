from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from schemas import MovementResponse, InventoryResponse
from services import MovementService
from dependencies import get_movement_service

api_router = APIRouter(prefix="/api")

@router.get("/movements/{movement_id}", response_model=MovementResponse)
async def get_movement(
    movement_id: UUID,
    service: MovementService = Depends(get_movement_service)
):
    return await service.get_movement_info(movement_id)

@router.get("/warehouses/{warehouse_id}/products/{product_id}", response_model=InventoryResponse)
async def get_inventory(
    warehouse_id: UUID,
    product_id: UUID,
    service: MovementService = Depends(get_movement_service)
):
    return await service.get_inventory_info(warehouse_id, product_id)