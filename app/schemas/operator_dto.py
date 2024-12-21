from datetime import datetime

from app.schemas.shared_dto import TicketShortResponseDto, OperatorShortResponseDto


class OperatorFullResponseDto(OperatorShortResponseDto):
    email: str | None
    username: str
    created_at: datetime

class OperatorOneResponseDto(OperatorFullResponseDto):
    tickets: list[TicketShortResponseDto]
