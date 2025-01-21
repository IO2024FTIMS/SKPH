from enum import Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Enum as SQLEnum
from app.extensions import db


class RequestStatus(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    COMPLETED = "Completed"


class Request(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    status: Mapped[RequestStatus] = mapped_column(SQLEnum(RequestStatus), nullable=False)
    req_address = relationship('Address')
    req_address_id = mapped_column(ForeignKey('address.id'))
    affected_id = mapped_column(ForeignKey('affected.id'))
    needs: Mapped[str]

    affected = relationship('Affected', back_populates='requests')

    def __repr__(self):
        return (
            f'Request:(id={self.id!r}, name={self.name!r}, '
            f'status={self.status.value!r},  affected_id={self.affected_id!r})'
        )
