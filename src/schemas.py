# app/schemas/kafka.py
from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, Field, validator, field_validator
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class MovementEventType(str, Enum):
    ARRIVAL = "arrival"
    DEPARTURE = "departure"


class MovementData(BaseModel):
    movement_id: UUID = Field(..., alias="movement_id")
    warehouse_id: UUID = Field(..., alias="warehouse_id")
    event: MovementEventType = Field(..., alias="event")
    product_id: UUID = Field(..., alias="product_id")
    quantity: int = Field(..., gt=0, alias="quantity")
    timestamp: datetime = Field(..., alias="timestamp")


class KafkaMessage(BaseModel):
    source: str = Field(..., pattern=r"^WH-\d{4}$")
    data: MovementData

    @field_validator("source")
    def validate_source(cls, v):
        return v.split(":")[0]


class MovementEventResponse(BaseModel):
    warehouse_id: UUID
    timestamp: datetime
    event_type: str
    quantity: int

class MovementResponse(BaseModel):
    movement_id: UUID
    product_id: UUID
    departure: MovementEventResponse | None
    arrival: MovementEventResponse | None
    time_elapsed: str | None
    quantity_diff: int | None

class InventoryResponse(BaseModel):
    warehouse_id: UUID
    product_id: UUID
    current_quantity: int
    last_updated: datetime