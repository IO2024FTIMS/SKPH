from app.extensions import db
from app.models.donor import Donor
from app.models.donation import DonationMoney, DonationItem
from datetime import date


def main():
    # Dodanie nowego darczyńcy
    new_donor = Donor(
        name="John",
        surname="Doe",
        phone_number="123456789",
        email="john.doe@example.com"
    )
    db.session.add(new_donor)
    db.session.commit()

    # Dodanie darowizny pieniężnej
    new_donation_money = DonationMoney(
        description="Charity Fundraiser",
        donation_date=date.today(),
        donation_type="Money",
        cashAmount=100.0,
        donor_id=new_donor.donor_id
    )
    db.session.add(new_donation_money)

    # Dodanie darowizny rzeczowej
    new_donation_item = DonationItem(
        description="T-shirt",
        donation_date=date.today(),
        donation_type="Clothes",
        number=10,
        donor_id=new_donor.donor_id
    )
    db.session.add(new_donation_item)
    db.session.commit()

    # Wyświetlenie wszystkich darczyńców i ich darowizn
    donors = db.session.query(Donor).all()
    for donor in donors:
        print(donor)
        for donation in donor.donations_money:
            print("  ", donation)
        for donation in donor.donations_items:
            print("  ", donation)


if __name__ == "__main__":
    main()
