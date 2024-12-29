from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

engine = create_engine("postgresql+psycopg2://admin:admin@localhost:5432/skph_db")

# Tworzenie klasy bazowej dla modeli
Base = declarative_base()

# Tworzenie sesji do interakcji z bazą danych
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Donor(Base):
    __tablename__ = "donors"  # Nazwa tabeli w bazie danych

    donor_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)

    # Relacja z tabelą Donation
    donations = relationship("Donation", back_populates="donor")

    def request_confirmation(self, donation_id: int) -> str:
        """Request confirmation for a specific donation."""
        return f"Confirmation requested for donation ID: {donation_id}"

    def __repr__(self):
        return f"<Donor(name={self.name}, email={self.email})>"