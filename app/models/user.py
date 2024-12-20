from sqlalchemy import Column, VARCHAR
from sqlalchemy.orm import relationship

from app.utils.mixins import IdMixin, TimestampMixin
from metadata import Base


class User(IdMixin, TimestampMixin, Base):
    __tablename__ = "client"

    first_name = Column(VARCHAR(256), nullable=False, index=True)
    middle_name = Column(VARCHAR(256), nullable=True)
    last_name = Column(VARCHAR(256), nullable=False, index=True)

    username = Column(
        VARCHAR(64),
        nullable=False,
        unique=True
    )

    email = Column(
        VARCHAR(256),
        nullable=True,
        unique=True
    )

    hashed_password = Column(
        VARCHAR(512),
        nullable=False
    )

    operator_rel = relationship(
        "Operator",
        back_populates="connected_user",
        foreign_keys="Operator.connected_user_id",
        lazy="noload",
        uselist=False
    )

    customer_rel = relationship(
        "Customer",
        back_populates="connected_user",
        foreign_keys="Customer.connected_user_id",
        lazy="noload",
        uselist=False
    )
