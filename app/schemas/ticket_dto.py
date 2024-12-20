from datetime import datetime

from pydantic import BaseModel

from app.utils.enums import TicketStatuses
from app.schemas.message_dto import MessageResponseDto
from app.schemas.operator_dto import OperatorShortResponseDto
from app.schemas.customer_dto import CustomerShortResponseDto


class TicketSearchDto(BaseModel):
    status: list[TicketStatuses] | None = None
    created_order: bool | None = None

    class Config:
        use_enum_values = True
        orm_mode = True

class ManyTicketResponseDto(BaseModel):
    id: int
    status: TicketStatuses
    operator: OperatorShortResponseDto | None
    customer: CustomerShortResponseDto | None
    created_at: datetime
    updated_at: datetime

    class Config:
        use_enum_values = True

class OneTicketResponseDto(ManyTicketResponseDto):
    messages: list[MessageResponseDto]


