from sqlalchemy import Column, VARCHAR, BIGINT, ForeignKey, TEXT, BOOLEAN
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from app.utils.mixins import IdMixin, TimestampMixin
from metadata import Base


class Message(IdMixin, TimestampMixin, Base):
    __tablename__ = "message"

    content = Column(TEXT)
    sender_type = Column(VARCHAR, nullable=False)
    root = Column(BOOLEAN, server_default=expression.false(), nullable=False, index=True)

    ticket_id = Column(BIGINT, ForeignKey('ticket.id'), nullable=False, index=True)
    ticket = relationship("Ticket", back_populates="messages", lazy="noload")
