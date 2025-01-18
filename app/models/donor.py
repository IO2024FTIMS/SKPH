from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class Donor(db.Model):

    donor_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    phone_number: Mapped[str]
    email: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    donations_money: Mapped[list["DonationMoney"]] = relationship(
        back_populates="donor", cascade="all, delete-orphan"
    )
    donations_items: Mapped[list["DonationItem"]] = relationship(
        back_populates="donor", cascade="all, delete-orphan"
    )


    def request_confirmation(self, donation_id: int) -> str:
        """Request confirmation for a specific donation."""
        return f"Confirmation requested for donation ID: {donation_id}"

    def __repr__(self):
        return f"<Donor(name={self.name}, email={self.email})>"
