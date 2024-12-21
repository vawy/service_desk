from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from starlette import status

from app.logic.base_dao import BaseDao
from app.logic.message_dao import MessageDao
from app.models import Ticket, Operator, Customer
from app.utils.enums import TicketStatuses
from app.schemas.ticket_dto import TicketSearchDto


class TicketDao(BaseDao):
    list_options = [
        joinedload(Ticket.operator).joinedload(Operator.connected_user),
        joinedload(Ticket.customer).joinedload(Customer.connected_user)
    ]
    options = [
        *list_options,
        selectinload(Ticket.messages)
    ]

    def __init__(self, session, options=None):
        super().__init__(session=session, model=Ticket, options=options)

    async def find_tickets(self, body: TicketSearchDto):
        query = select(Ticket)

        if body.status:
            query = query.where(Ticket.status.in_(body.status))

        if body.created_order:
            query = query.order_by(Ticket.created_at.asc())
        else:
            query = query.order_by(Ticket.created_at.desc())

        return await self.find_all(query=query)

    async def close_ticket(self, ticket_id: int):
        ticket = await self.find_one(model_id=ticket_id)

        if ticket.status != TicketStatuses.IN_PROGRESS.value:
            if ticket.status == TicketStatuses.CLOSED.value:
                detail = f"{Ticket.__name__} with ID={ticket_id} was closed"
            else:
                detail = f"{Ticket.__name__} with ID={ticket_id} does not have an operator. To close it you should to connect an operator"

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=detail,
            )

        ticket.status = TicketStatuses.CLOSED.value

        message_dao = MessageDao(session=self.session)
        back_message_done = message_dao.create_back_message_done()
        ticket.messages.append(back_message_done)
        return back_message_done

    async def set_ticket(self, ticket_id: int, operator_id: int):
        ticket = await self.find_one(model_id=ticket_id)
        if ticket.operator_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{Ticket.__name__} with ID={ticket_id} has operator",
            )
        ticket.operator_id = operator_id
        ticket.status = TicketStatuses.IN_PROGRESS.value
