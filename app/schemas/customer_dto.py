from datetime import datetime

from app.schemas.shared_dto import CustomerShortResponseDto


class CustomerFullResponseDto(CustomerShortResponseDto):
    email: str | None
    username: str
    created_at: datetime
