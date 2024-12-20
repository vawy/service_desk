from sqlalchemy.orm import joinedload

from app.logic.base_dao import BaseDao
from app.models import Customer


class CustomerDao(BaseDao):
    list_options = [
        joinedload(Customer.connected_user)
    ]
    options = [
        *list_options
    ]

    def __init__(self, session, options=None):
        super().__init__(session=session, model=Customer, options=options)