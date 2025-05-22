from fastapi import Depends
from faststream.kafka.fastapi import KafkaRouter
import logging

from dependencies import get_movement_service
from schemas import KafkaMessage
from services import MovementService

kafka_router = KafkaRouter("kafka:9092")

logger = logging.getLogger(__name__)

@kafka_router.subscriber("warehouse_movements")
async def handle_movement_event(
    message: KafkaMessage,
    movement_service: MovementService = Depends(get_movement_service)
):
    data = message.data

    try:
        await movement_service.process_movement(
            movement_id=data.movement_id,
            event_type=data.event,
            warehouse_code=message.source,
            product_id=data.product_id,
            quantity=data.quantity,
            timestamp=data.timestamp
        )
    except ValueError as e:
        logger.error(f"Error processing movement: {e}")