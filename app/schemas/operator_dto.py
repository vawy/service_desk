from datetime import datetime

from pydantic import BaseModel


class OperatorShortResponseDto(BaseModel):
    id: int
    name: str | None

class OperatorFullResponseDto(OperatorShortResponseDto):
    email: str | None
    username: str
    created_at: datetime
