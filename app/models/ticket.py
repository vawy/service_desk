from sqlalchemy import Column, VARCHAR, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.utils.mixins import IdMixin, TimestampMixin
from app.utils.enums import TicketStatuses
from metadata import Base


class Ticket(IdMixin, TimestampMixin, Base):
    __tablename__ = "ticket"

    status = Column(VARCHAR, default=TicketStatuses.NEW.value, index=True)

    operator_id = Column(Integer, ForeignKey("operator.id"), nullable=True, index=True)
    operator = relationship("Operator", back_populates="tickets", lazy="noload")

    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False, index=True)
    customer = relationship("Customer", back_populates="ticket", uselist=False, lazy="noload")

    messages = relationship("Message", back_populates="ticket", cascade="all, delete-orphan", lazy="noload")
