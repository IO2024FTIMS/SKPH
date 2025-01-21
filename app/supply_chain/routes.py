from flask import Blueprint, flash, redirect, render_template, request, url_for

from sqlalchemy import text

from datetime import datetime

from app.extensions import db
from app.models.item_stock import ItemStock

from app.models.volunteer import Volunteer
from app.models.organization import Organization
from app.models.address import Address
from app.models.affected import Affected
from app.models.donation import DonationItem, DonationType
from app.models.donation import DonationMoney
from app.models.user import User
from app.models.donor import Donor
from app.models.authorities import Authorities

from app.models.charity_campaign import CharityCampaign
from app.models.charity_campaign import OrganizationCharityCampaign

from app.supply_chain.resource_manager import ResourceManager

bp = Blueprint('supply_chain', __name__, 
               template_folder='../templates/supply_chain',
               static_folder='static',
               static_url_path='supply_chain')

resource_manager = ResourceManager()
    

@bp.route('/')
def index():
    volunteers = db.session.query(Volunteer)
    charity_campaign = db.session.query(CharityCampaign).all()

    if len(charity_campaign) == 0:
        return render_template('supply_chain.jinja',
                               charity_campaign = None,
                               item_donations = None)
    # charity_campaign = charity_campaign[0]
    query = text('''select ist.id, dt.type, ist.amount  from item_stock ist
        join donation_type dt on ist.item_type_id = dt.id''')

    item_donations = db.session.execute(query).mappings().all()
    charity_campaign = charity_campaign[0]

    return render_template('supply_chain.jinja', 
                           item_donations=item_donations,
                           charity_campaign=charity_campaign)


@bp.route('/truncate')
def truncate():
    db.drop_all()
    db.create_all()
    print('what: ')
    return redirect('/supply_chain')

@bp.route('/resource/<int:id>')
def manage_resource(id):
    if request.method =='GET':
        resource = db.session.get(ItemStock, id)
        print('resource: ')
        print(resource)
        resource_type = db.session.get(DonationType, resource.item_type_id)
        return render_template('manage_resource.jinja',
                               resource=resource,
                               resource_type=resource_type,
                               affecteds = db.session.query(Affected).all())
    return redirect('/supply_chain')

@bp.route('/add-data')
def add_data():
    
    address1 = Address(
    street="123 Main St",
    street_number="Apt 101",
    city="New York",
    voivodeship="NY"
    )

    address2 = Address(
        street="456 Elm St",
        street_number="Apt 202",
        city="Los Angeles",
        voivodeship="CA"
    )

    address3 = Address(
        street="456 Elm St",
        street_number="Apt 202",
        city="lodz",
        voivodeship="lodzkie"
    )

    address_result = db.session.query(Address).all()
    if len(address_result) != 0:
        db.session.rollback()
        charity_campaign = db.session.query(CharityCampaign).all()
        if len(charity_campaign) == 0:
            return render_template('supply_chain.jinja', 
                            item_donations=None,
                            charity_campaign=None)
        else: 
            charity_campaign = charity_campaign[0]
            query = text('select ist.id, dt.type, ist.amount  from item_stock ist join donation_type dt on ist.item_type_id = dt.id')
            item_donations = db.session.execute(query).mappings().all()
            return render_template('supply_chain.jinja', 
                            item_donations=item_donations,
                            charity_campaign=charity_campaign)
    else: 

        db.session.add(address1)
        db.session.add(address2)
        db.session.add(address3)

        user1 = User(
            email="john.doe@example.com",
            password_hash="password123",
            active=True,
            type="donor"
        )

        user2 = User(
            email="jane.smith@example.com",
            password_hash="password456",
            active=True,
            type="donor"
        )

        user3 = User(
            email="jane.smith234@example.com",
            password_hash="password456",
            active=True,
            type="authorities"
        )

        user4= User(
            email="affected@email.com",
            password_hash='pass222',
            active=True,
            type="affected"
        )

        user5= User(
            email="org@email.com",
            password_hash='pass222',
            active=True,
            type="organization"
        )

        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.add(user4)
        db.session.add(user5)

        donor1 = Donor(
            name="John",
            surname="Doe",
            phone_number="123-456-7890",
            email="john.doe2@example.com",
            user_id=1
        )

        donor2 = Donor(
            name="Jane",
            surname="Smith",
            phone_number="987-654-3210",
            email="jane.smith@example.com",
            user_id=2
        )
        authority = Authorities(
            name="New York City Authority",
            phone="123-456-7890",
            address_id=3,
            user_id=3
        )
        db.session.add(authority)


        db.session.add(donor1)
        db.session.add(donor2)

        charity_campaign_1 = CharityCampaign(
            name="Charity campagin 1",
            description="Sample campagin",
            authorities_id=1
        )

        db.session.add(charity_campaign_1)

        donation_type_1 = DonationType(type='Money')
        donation_type_2 = DonationType(type='Food')
        donation_type_3 = DonationType(type='Clothes')
        donation_type_4 = DonationType(type='Other')

        db.session.add(donation_type_1)
        db.session.add(donation_type_2)
        db.session.add(donation_type_3)
        db.session.add(donation_type_4)

        # donation items
        donation_item1 = DonationItem(
        description="Test Donation 1",
        donation_date=datetime.today(),
        amount=100.0,
        donor_id=1,
        charity_campaign_id=1,
        donation_type_id=1
        )

        donation_item2 = DonationItem(
            description="Test Donation 2",
            donation_date=datetime.today(),
            amount=50.0,
            donor_id=2,
            charity_campaign_id=1,
            donation_type_id=2
        )

        affected1 = Affected(
            first_name="John",
            last_name="Affected",
            needs="food",
            address_id=1,
            user_id=4,
            campaign_id=1
        )

        # create charity campaign

        organization1 = Organization(
            organization_name="FUNDACJA OJCA RYDZYKA",
            description="bardzo dobra organizacja",
            approved=True,
            address_id=2,
            user_id=5,
        )

        stock_1 = ItemStock( item_type_id=donation_item1.donation_type_id,
                             campaign_id=donation_item1.charity_campaign_id,
                             amount=donation_item1.amount)

        stock_2 = ItemStock(item_type_id=donation_item2.donation_type_id,
                             campaign_id=donation_item2.charity_campaign_id,
                             amount=donation_item2.amount)

        db.session.add(donation_item1)
        db.session.add(donation_item2)
        db.session.add(stock_1)
        db.session.add(stock_2)
        db.session.add(affected1)
        db.session.add(organization1)
        db.session.commit()

        return redirect('/supply_chain')


