from sqlalchemy import Column, BIGINT, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from app.utils.mixins import IdMixin, TimestampMixin
from metadata import Base


class Operator(IdMixin, TimestampMixin, Base):
    __tablename__ = "operator"

    connected_user_id = Column(
        BIGINT,
        ForeignKey("client.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )
    connected_user = relationship(
        "User",
        back_populates="operator_rel",
        foreign_keys="Operator.connected_user_id",
        lazy="noload"
    )

    tickets = relationship("Ticket", back_populates="operator", lazy="noload", secondaryjoin="")

    @hybrid_property
    def name(self):
        return (
            f"{self.connected_user.last_name} {self.connected_user.first_name} {self.connected_user.middle_name or ''}"
            .strip() or None
        )

    @hybrid_property
    def email(self):
        return self.connected_user.email or None

    @hybrid_property
    def username(self):
        return self.connected_user.username or None
