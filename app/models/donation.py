from datetime import date

from sqlalchemy import ForeignKey, DateTime

from app import db
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship


class DonationMoney(db.Model):

    donationMoney_id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    donation_date: Mapped[date] = date.today()
    donation_type: Mapped[str]
    cashAmount: Mapped[float]
    donor_id: Mapped[int] = mapped_column(ForeignKey('donor.donor_id'))
    charity_campaign_id: Mapped[int] = mapped_column(ForeignKey('charity_campaign.id'))
    charity_campaign = relationship('CharityCampaign')
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
    donation_type_id: Mapped[int] = mapped_column(ForeignKey('donation_type.id'))
    amount: Mapped[float]
    donor_id: Mapped[int] = mapped_column(ForeignKey('donor.donor_id'))
    donor: Mapped["Donor"] = relationship(back_populates="donations_items")
    charity_campaign_id: Mapped[int] = mapped_column(ForeignKey('charity_campaign.id'))
    charity_campaign = relationship('CharityCampaign')


    def return_confirmation(self) -> str:
        """Return a confirmation message."""
        return f"Donation confirmed: {self.description}, Amount: {self.amount}"

    def __repr__(self):
        return f"<Donation(description={self.description}, amount={self.amount})>"


class DonationType(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]