from sqlalchemy.orm import joinedload

from app.logic.base_dao import BaseDao
from app.models import Operator


class OperatorDao(BaseDao):
    list_options = [
        joinedload(Operator.connected_user)
    ]
    options = [
        *list_options
    ]

    def __init__(self, session, options=None):
        super().__init__(session=session, model=Operator, options=options)
