from pydantic import BaseModel


class BasicResultResponseDto(BaseModel):
    result: str = 'OK'
