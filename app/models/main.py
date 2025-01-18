from app.extensions import db
from app.donors.donor import Donor
from app.donors.donation import DonationMoney,DonationItem
from datetime import date

# Tworzenie tabel w bazie danych

# Funkcja główna
def main():


    # Dodaj nowego darczyńcę
    new_donor = Donor(
        name="John",
        surname="Doe",
        phone_number="123456789",
        email="john.doe@example.com"
    )
    db.session.add(new_donor)
    db.session.commit()
    db.session.refresh(new_donor)  # Odświeża obiekt, aby uzyskać ID


    new_donation = DonationMoney(
        description="Charity Fundraiser",
        donation_date=date.today(),
        donation_type="Money",
        cashAmount=100.0,
        donor_id=new_donor.donor_id
    )
    db.session.add(new_donation)

    new_donation2 = DonationItem(
        description="koszulka",
        donation_date=date.today(),
        donation_type="clothes",
        number=10,
        donor_id=new_donor.donor_id
    )

    db.session.add(new_donation2)
    db.session.commit()

    # Wyświetl wszystkich darczyńców i ich donacje
    donors = db.session.query(Donor).all()
    for donor in donors:
        print(donor)
        for donation in donor.donations:
            print("  ", donation)



if __name__ == "__main__":
    main()
