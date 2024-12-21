from fastapi import HTTPException

from sqlalchemy import select, and_

from starlette import status

from app.logic.base_dao import BaseDao
from app.utils.enums import TicketStatuses, MessageSenderType, MessageDefaultResponse
from app.models import Message, Ticket
from app.schemas.message_dto import SendMessageToOperatorDto, SendMessageToCustomerDto
from app.schemas.base_responses import BasicResultResponseDto


class MessageDao(BaseDao):
    list_options = [
    ]
    options = [
        *list_options
    ]

    def __init__(self, session, options=None):
        super().__init__(session=session, model=Message, options=options)

    async def send_to_operator(self, body: SendMessageToOperatorDto, customer_id: int):
        query = (
            select(Ticket)
            .where(
                and_(
                    Ticket.customer_id == customer_id,
                    Ticket.status != TicketStatuses.CLOSED.value
                )
            )
        )
        ticket = await self.find_one(query=query, raise_exception=False)

        message = Message(
            content=body.content,
            sender_type=MessageSenderType.CUSTOMER.value
        )
        self.session.add(message)

        if not ticket:
            message.root = True
            new_ticket = self._create_ticket(customer_id=customer_id)
            back_message = self._create_first_back_message()
            new_ticket.messages.append(message)
            new_ticket.messages.append(back_message)
            return back_message
        else:
            ticket.messages.append(message)

        return BasicResultResponseDto()

    async def send_to_customer(self, body: SendMessageToCustomerDto):
        """
        Отправка сообщения заказчику в тикет.
        """
        query = select(Ticket).where(Ticket.id == body.ticket_id)
        ticket = await self.find_one(query=query)

        if ticket.status == TicketStatuses.CLOSED.value:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{Ticket.__name__} with ID={body.ticket_id} was closed",
            )

        if not ticket.operator_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{Ticket.__name__} with ID={body.ticket_id} without operator. Please connect it to operator",
            )

        message = Message(
            content=body.content,
            sender_type=MessageSenderType.OPERATOR.value
        )
        ticket.messages.append(message)
        self.session.add(message)


    def _create_ticket(self, customer_id: int):
        new_ticket = Ticket(customer_id=customer_id)
        self.session.add(new_ticket)
        return new_ticket

    def _create_first_back_message(self):
        first_back_message = Message(
            content=MessageDefaultResponse.FIRST_MESSAGE_RESPONSE.value,
            sender_type=MessageSenderType.SYSTEM.value
        )
        self.session.add(first_back_message)
        return first_back_message

    def create_back_message_done(self, ticket: Ticket):
        back_message_done = Message(
            content=MessageDefaultResponse.DONE_MESSAGE_RESPONSE.value,
            sender_type=MessageSenderType.SYSTEM.value
        )
        ticket.messages.append(back_message_done)
        self.session.add(back_message_done)
        return back_message_done
