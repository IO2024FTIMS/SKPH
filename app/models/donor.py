from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class Donor(db.Model):
    donor_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    phone_number: Mapped[str]
    email: Mapped[str]


    def request_confirmation(self, donation_id: int) -> str:
        """Request confirmation for a specific donation."""
        return f"Confirmation requested for donation ID: {donation_id}"

    def __repr__(self):
        return f"<Donor(name={self.name}, email={self.email})>"