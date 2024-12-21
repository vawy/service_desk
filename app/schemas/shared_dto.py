from datetime import datetime

from pydantic import BaseModel

from app.utils.enums import TicketStatuses


class OperatorShortResponseDto(BaseModel):
    id: int
    name: str | None


class CustomerShortResponseDto(BaseModel):
    id: int
    name: str | None


class TicketShortResponseDto(BaseModel):
    id: int
    status: TicketStatuses
    customer: CustomerShortResponseDto | None
    created_at: datetime
    updated_at: datetime

    class Config:
        use_enum_values = True
