from donor import Base, engine, SessionLocal
from donor import Donor
from donation import Donation
from datetime import date

# Tworzenie tabel w bazie danych
Base.metadata.create_all(bind=engine)

# Funkcja główna
def main():
    # Otwórz sesję
    session = SessionLocal()

    # Dodaj nowego darczyńcę
    new_donor = Donor(
        name="John",
        surname="Doe",
        phone_number="123456789",
        email="john.doe@example.com"
    )
    session.add(new_donor)
    session.commit()
    session.refresh(new_donor)  # Odświeża obiekt, aby uzyskać ID

    # Dodaj donację dla tego darczyńcy
    new_donation = Donation(
        description="Charity Fundraiser",
        donation_date=date.today(),
        donation_type="Money",
        amount=100.0,
        donor_id=new_donor.donor_id
    )
    session.add(new_donation)
    session.commit()

    # Wyświetl wszystkich darczyńców i ich donacje
    donors = session.query(Donor).all()
    for donor in donors:
        print(donor)
        for donation in donor.donations:
            print("  ", donation)

    # Zamknij sesję
    session.close()

if __name__ == "__main__":
    main()
