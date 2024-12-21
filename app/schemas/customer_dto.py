from datetime import datetime

from pydantic import BaseModel


class CustomerShortResponseDto(BaseModel):
    id: int
    name: str | None


class CustomerFullResponseDto(CustomerShortResponseDto):
    email: str | None
    username: str
    created_at: datetime
