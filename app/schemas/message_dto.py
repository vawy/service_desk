from pydantic import BaseModel

from app.utils.enums import MessageSenderType


class BaseMessageDto(BaseModel):
    content: str

class SendMessageToOperatorDto(BaseMessageDto):
    pass

class SendMessageToCustomerDto(BaseMessageDto):
    ticket_id: int

class MessageResponseDto(BaseMessageDto):
    id: int
    sender_type: MessageSenderType
    root: bool

    class Config:
        use_enum_values = True
