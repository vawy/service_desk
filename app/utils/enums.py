from enum import Enum


class TicketStatuses(Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"


class MessageSenderType(Enum):
    CUSTOMER = "customer"
    OPERATOR = "operator"
    SYSTEM = "system"


class MessageDefaultResponse(Enum):
    FIRST_MESSAGE_RESPONSE = "Здравствуйте! Ваше сообщение в работе"
    DONE_MESSAGE_RESPONSE = "Здравствуйте! Ваша проблема решена"
