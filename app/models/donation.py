from _datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime

from app import db
from app.extensions import db
from sqlalchemy.orm import relationship, Mapped, mapped_column


class DonationMoney(db.Model):

    donation_id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    donation_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    donation_type: Mapped[str]
    cashAmount: Mapped[float]
    donor_id: Mapped[int] = mapped_column(Integer, ForeignKey('donor.id'), nullable=False)

    def return_confirmation(self) -> str:
        """Return a confirmation message."""
        return f"Donation confirmed: {self.description}, Amount: {self.cashAmount}"

    def __repr__(self):
        return f"<Donation(description={self.description}, amount={self.cashAmount})>"

class DonationItem(db.Model):
    donation_id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    donation_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    donation_type: Mapped[str]
    number: Mapped[float]
    donor_id: Mapped[int] = mapped_column(Integer, ForeignKey('donor.id'), nullable=False)


    def return_confirmation(self) -> str:
        """Return a confirmation message."""
        return f"Donation confirmed: {self.description}, Amount: {self.number}"

    def __repr__(self):
        return f"<Donation(description={self.description}, amount={self.number})>"
