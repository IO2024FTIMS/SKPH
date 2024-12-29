from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from donor import Base
from sqlalchemy.orm import relationship

class Donation(Base):
    __tablename__ = "donations"  # Nazwa tabeli w bazie danych

    donation_id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    donation_date = Column(Date, nullable=False)
    donation_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    donor_id = Column(Integer, ForeignKey("donors.donor_id"))

    # Relacja z tabelą Donor
    donor = relationship("Donor", back_populates="donations")

    def return_confirmation(self) -> str:
        """Return a confirmation message."""
        return f"Donation confirmed: {self.description}, Amount: {self.amount}"

    def __repr__(self):
        return f"<Donation(description={self.description}, amount={self.amount})>"
