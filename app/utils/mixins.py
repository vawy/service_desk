import datetime

from sqlalchemy import Column, DateTime, func, BIGINT


class IdMixin:
    id = Column(
        BIGINT,
        primary_key=True,
        autoincrement=True
    )


class CreatedAtMixin:
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
        server_default=func.now(),
        index=True
    )


class TimestampMixin(CreatedAtMixin):
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        index=True
    )
