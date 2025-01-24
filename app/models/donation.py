from datetime import date
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db

if TYPE_CHECKING:
    from app.models.donor import Donor


class ItemDonationType(Enum):
    WATER = "water"
    FOOD = "food"
    CLOTHES = "clothes"
    MEDICINE = "medicine"


class DonationMoney(db.Model):
    donationMoney_id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    donation_date: Mapped[date] = mapped_column(default=date.today)
    donation_type: Mapped[str]
    cashAmount: Mapped[float]
    charity_campaign = relationship('OrganizationCharityCampaign', back_populates='donations_money')
    charity_campaign_id = mapped_column(ForeignKey('organization_charity_campaign.id'))
    donor_id: Mapped[int] = mapped_column(ForeignKey('donor.donor_id'))
    donor: Mapped["Donor"] = relationship("Donor", back_populates="donations_money")

    def return_confirmation(self) -> str:
        """Return a confirmation message."""
        return f"Donation confirmed: {self.description}, Amount: {self.cashAmount}"

    def __repr__(self):
        return f"<Donation(description={self.description}, amount={self.cashAmount})>"


class DonationItem(db.Model):
    donationItem_id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    donation_date: Mapped[date] = mapped_column(default=date.today)
    donation_type: Mapped[ItemDonationType]
    number: Mapped[int]
    charity_campaign = relationship('OrganizationCharityCampaign', back_populates='donations_item')
    charity_campaign_id = mapped_column(ForeignKey('organization_charity_campaign.id'))
    donor_id: Mapped[int] = mapped_column(ForeignKey('donor.donor_id'))
    donor: Mapped["Donor"] = relationship("Donor", back_populates="donations_items")

    def return_confirmation(self) -> str:
        """Return a confirmation message."""
        return f"Donation confirmed: {self.description}, Amount: {self.number}"

    def __repr__(self):
        return f"<Donation(description={self.description}, amount={self.number})>"
