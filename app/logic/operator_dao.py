from sqlalchemy.orm import joinedload, selectinload

from app.logic.base_dao import BaseDao
from app.models import Operator, Ticket, Customer


class OperatorDao(BaseDao):
    list_options = [
        joinedload(Operator.connected_user)
    ]
    options = [
        *list_options,
        selectinload(Operator.tickets).joinedload(Ticket.customer).joinedload(Customer.connected_user)
    ]

    def __init__(self, session, options=None):
        super().__init__(session=session, model=Operator, options=options)
