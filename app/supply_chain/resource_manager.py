from app.extensions import db

from datetime import datetime


from app.models.volunteer import Volunteer
from app.models.organization import Organization
from app.models.address import Address
from app.models.affected import Affected
from app.models.donation import DonationItem
from app.models.donation import DonationMoney
from app.models.donor import Donor
from app.models.user import User

class ResourceManager:
    def init(self):
        self.test = 'test'

    def get_all_resources(self):
        donation_items = db.session.query(DonationMoney)
        donation_money = db.session.query(DonationMoney)

        resources = {
            'donation_money': donation_money,
            'donation_items': donation_items
        }

        return resources
    
    
    def get_donation_money(self):
        donation_money = db.session.query(DonationMoney)
        return donation_money
    

    def initialize_resources(self):

        # Create two users
        user1 = User(
            id=1,
            email="john@example.com",
            type="donor"
        )
        user1.set_password("password123")

        user2 = User(
            id=2,
            email="jane@example.com",
            type="organization"
        )
        user2.set_password("password456")

        # Create some initial donors
        donor1 = Donor(
            donor_id=1,
            name="John",
            surname="Doe",
            phone_number="123-456-7890",
            email="john@example.com",
            user_id=1
        )


        donor2 = Donor(
            donor_id=2,
            name="Jane",
            surname="Smith",
            phone_number="987-654-3210",
            email="jane@example.com",
            user_id=2
        )
        # Create some initial donations
        donation_money1 = DonationMoney(
            donationMoney_id=1,
            description="Cash donation for charity event",
            donation_date=datetime.today(),
            donation_type="Cash",
            cashAmount=100.00,
            donor_id=1,
            donor=donor1
        )

        donation_money2 = DonationMoney(
            donationMoney_id=2,
            description="Cash donation for disaster relief",
            donation_date=datetime.today(),
            donation_type="Cash",
            cashAmount=50.00,
            donor_id=2,
            donor=donor2
        )

        donation_item1 = DonationItem(
            donationItem_id=1,
            description="Donation of 10 boxes of food",
            donation_date=datetime.today(),
            donation_type="Food",
            number=10.0,
            donor_id=1,
            donor=donor1
        )

        donation_item2 = DonationItem(
            donationItem_id=2,
            description="Donation of 5 boxes of clothing",
            donation_date=datetime.today(),
            donation_type="Clothing",
            number=5.0,
            donor_id=2,
            donor=donor2
        )

        db.session.add(user1)
        db.session.add(user2)
        db.session.add(donor1)
        db.session.add(donor2)
        db.session.add(donation_money1)
        db.session.add(donation_money2)
        db.session.add(donation_item1)
        db.session.add(donation_item2)

        db.session.commit()