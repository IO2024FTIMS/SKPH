from flask import Blueprint, redirect, render_template, request

from sqlalchemy import text

from datetime import datetime

from app.extensions import db
from app.models.item_stock import ItemStock

from app.models.volunteer import Volunteer
from app.models.organization import Organization
from app.models.charity_campaign import OrganizationCharityCampaign
from app.models.address import Address
from app.models.affected import Affected
from app.models.donation import DonationItem, DonationType
from app.models.user import User
from app.models.donor import Donor
from app.models.authorities import Authorities
from app.models.request import Request
from app.models.charity_campaign import CharityCampaign
from app.supply_chain.resource_manager import ResourceManager

bp = Blueprint('supply_chain', __name__,
               template_folder='../templates/supply_chain',
               static_folder='static',
               static_url_path='supply-chain')

resource_manager = ResourceManager()


@bp.route('/')
def index():
    charity_campaign = db.session.query(CharityCampaign).all()
    if len(charity_campaign) == 0:
        return render_template('supply_chain.jinja',
                               charity_campaign=None,
                               item_donations=None)
    query = text('''select ist.id, dt.type, ist.amount  from item_stock ist
        join donation_type dt on ist.item_type_id = dt.id''')

    item_donations = db.session.execute(query).mappings().all()
    charity_campaign = CharityCampaign.query.filter(CharityCampaign.name == 'Charity campagin 1').first()
    avalible_volunteers = Volunteer.query.all()
    current_requests = Request.query \
        .join(DonationType, Request.donation_type_id == DonationType.id) \
        .join(Affected, Request.affected_id == Affected.id) \
        .join(Address, Request.req_address_id == Address.id) \
        .add_columns(Request.name, Request.status, Affected.first_name, Affected.last_name,
                     Address.city, Address.street, Address.voivodeship, DonationType.type, Request.amount) \
        .all()
    print(current_requests)

    return render_template('supply_chain.jinja',
                           item_donations=item_donations,
                           charity_campaign=charity_campaign,
                           volunteers=avalible_volunteers,
                           current_requests=current_requests)


@bp.route('/truncate')
def truncate():
    db.drop_all()
    db.create_all()
    print('what: ')
    return redirect('/supply-chain')


@bp.route('/resource/<int:item_id>', methods=['GET', 'POST'])
def manage_resource(item_id):
    resource = db.session.get(ItemStock, item_id)
    if request.method == 'GET':
        print('resource: ')
        print(resource)
        resource_type = db.session.get(DonationType, resource.item_type_id)
        return render_template('manage_resource.jinja',
                               resource=resource,
                               resource_type=resource_type,
                               affecteds=db.session.query(Affected).all())
    if request.method == 'POST':
        affected_assigned_resources = {}
        resouce_use_amount = 0
        for i in db.session.query(Affected).all():
            if int(request.form[i.id]) > 0:
                affected_assigned_resources[i.id] = int(request.form[i.id])
                resouce_use_amount += int(request.form[i.id])
        print(resource)
        return redirect('/')


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
            return render_template('supply_chain.jinja', item_donations=None, charity_campaign=None)
        else:
            charity_campaign = charity_campaign[0]
            query = text('select ist.id, dt.type, ist.amount from item_stock ist join donation_type dt on ist.item_type_id = dt.id')
            item_donations = db.session.execute(query).mappings().all()
            return render_template('supply_chain.jinja', item_donations=item_donations, charity_campaign=charity_campaign)
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

        user4 = User(
            email="affected@email.com",
            password_hash='pass222',
            active=True,
            type="affected"
        )

        user5 = User(
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

        print(User.query.filter(User.email == "org@email.com").first().email)

        donor1 = Donor(
            name="John",
            surname="Doe",
            phone_number="123-456-7890",
            email="john.doe2@example.com",
            user=user1
        )

        donor2 = Donor(
            name="Jane",
            surname="Smith",
            phone_number="987-654-3210",
            email="jane.smith@example.com",
            user_id=User.query.filter(User.email == "jane.smith@example.com").first().id
        )
        authority = Authorities(
            name="New York City Authority",
            phone="123-456-7890",
            address_id=Address.query.filter(Address.street == "123 Main St" and Address.city == 'New York').first().id,
            user_id=User.query.filter(User.email == "jane.smith234@example.com").first().id
        )
        db.session.add(authority)
        db.session.add(donor1)
        db.session.add(donor2)
        charity_campaign_1 = CharityCampaign(
            name="Charity campagin 1",
            description="Sample campagin",
            authorities_id=Authorities.query.filter(Authorities.name == "New York City Authority").first().id
        )

        db.session.add(charity_campaign_1)
        organization1 = Organization(
            organization_name="FUNDACJA OJCA RYDZYKA",
            description="bardzo dobra organizacja",
            approved=True,
            address_id=Address.query.filter(Address.street == "456 Elm St" and Address.street_number == 'Apt 202' and Address.city == 'Los Angeles').first().id,
            user_id=User.query.filter(User.email == "org@email.com").first().id,
        )

        db.session.add(organization1)
        organization_charity_campaign_1 = OrganizationCharityCampaign(
            charity_campaign=charity_campaign_1,
            organization=organization1
        )

        db.session.add(organization_charity_campaign_1)

        donation_type_2 = DonationType(type='Food')
        donation_type_3 = DonationType(type='Clothes')
        donation_type_4 = DonationType(type='Other')

        db.session.add(donation_type_2)
        db.session.add(donation_type_3)
        db.session.add(donation_type_4)

        # donation items
        donation_item1 = DonationItem(
            description="Test Donation 1",
            donation_date=datetime.today(),
            amount=100.0,
            donor_id=Donor.query.filter(Donor.email == 'john.doe2@example.com').first().donor_id,
            charity_campaign_id=OrganizationCharityCampaign.query.filter(CharityCampaign.name == 'Charity campagin 1').first().id,
            donation_type_id=DonationType.query.filter(DonationType.type == 'Food').first().id
        )

        donation_item2 = DonationItem(
            description="Test Donation 2",
            donation_date=datetime.today(),
            amount=50.0,
            donor_id=Donor.query.filter(Donor.email == 'jane.smith@example.com').first().donor_id,
            charity_campaign_id=CharityCampaign.query.filter(CharityCampaign.name == 'Charity campagin 1').first().id,
            donation_type_id=DonationType.query.filter(DonationType.type == 'Clothes').first().id
        )

        affected1 = Affected(
            first_name="John",
            last_name="Affected",
            needs="food",
            address_id=Address.query.filter(Address.street == "456 Elm St" and Address.street_number == 'Apt 202' and Address.city == 'Los Angeles').first().id,
            user_id=User.query.filter(User.email == "affected@email.com").first().id,
            campaign_id=CharityCampaign.query.filter(CharityCampaign.name == 'Charity campagin 1').first().id,
        )

        # create charity campaign
        stock_1 = ItemStock(item_type_id=donation_item1.donation_type_id,
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

        request_1 = Request(
            name='first reqest',
            status='PENDING',
            amount=10,
            req_address_id=Address.query.filter(Address.street == "456 Elm St" and Address.street_number == 'Apt 202' and Address.city == 'Los Angeles').first().id,
            affected_id=Affected.query.filter(Affected.first_name == 'John' and Affected.last_name == 'Affected').first().id,
            donation_type_id=DonationType.query.filter(DonationType.type == 'Food').first().id

        )
        db.session.add(request_1)

        db.session.commit()

        return redirect('/supply-chain')
