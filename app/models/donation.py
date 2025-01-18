from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.donor import Donor


class DonationMoney(db.Model):
    donationMoney_id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    donation_date: Mapped[date] = date.today()
    donation_type: Mapped[str]
    cashAmount: Mapped[float]
    donor_id: Mapped[int] = mapped_column(ForeignKey('donor.donor_id'))
    donor: Mapped["Donor"] = relationship(back_populates="donations_money")

    def return_confirmation(self) -> str:
        """Return a confirmation message."""
        return f"Donation confirmed: {self.description}, Amount: {self.cashAmount}"

    def __repr__(self):
        return f"<Donation(description={self.description}, amount={self.cashAmount})>"


class DonationItem(db.Model):
    donationItem_id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    donation_date: Mapped[date] = date.today()
    donation_type: Mapped[str]
    number: Mapped[float]
    donor_id: Mapped[int] = mapped_column(ForeignKey('donor.donor_id'))
    donor: Mapped["Donor"] = relationship(back_populates="donations_items")

    def return_confirmation(self) -> str:
        """Return a confirmation message."""
        return f"Donation confirmed: {self.description}, Amount: {self.number}"

    def __repr__(self):
        return f"<Donation(description={self.description}, amount={self.number})>"
