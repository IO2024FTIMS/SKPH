from flask import Blueprint, redirect, render_template, url_for, request

from app.extensions import db
from app.models.address import Address
from app.models.authorities import Authorities
from app.models.charity_campaign import (CharityCampaign,
                                         OrganizationCharityCampaign)
from app.models.organization import Organization
from app.models.volunteer import Volunteer

bp = Blueprint('organization', __name__, template_folder='../templates/organization')


@bp.route('/')
def index():
    return render_template('organization_index.jinja')


@bp.route('/charity_campaigns')
def list_charity_campaigns():
    charity_campaigns = db.session.scalars(db.select(CharityCampaign)).all()
    return render_template('list_charity_campaigns.jinja', charity_campaigns=charity_campaigns)


@bp.route('/organization_charity_campaigns')
def list_organization_charity_campaigns():
    organization_charity_campaigns = db.session.scalars(db.select(OrganizationCharityCampaign)).all()
    return render_template('list_organization_charity_campaigns.jinja',
                           organization_charity_campaigns=organization_charity_campaigns)


@bp.route('/add_sample_charity_campaign')
def add_sample_charity_campaign():
    a1 = Address(street='Miejska', street_number='1a', city='Łódź', voivodeship='Łódzkie')
    authority = Authorities(name='John Doe', phone='123456789', approved=True, address=a1)
    sample_campaign = CharityCampaign(name="Sample Campaign",
                                      description="This is a sample charity campaign.",
                                      authority=authority)
    db.session.add(sample_campaign)
    db.session.commit()
    return redirect(url_for('organization.list_charity_campaigns'))


@bp.route('/add_sample_organization_charity_campaign')
def add_sample_organization_charity_campaign():
    a1 = Address(street='Miejska', street_number='1a', city='Łódź', voivodeship='Łódzkie')
    authority = Authorities(name='John Doe', phone='123456789', approved=True, address=a1)
    sample_campaign = CharityCampaign(name="Sample Campaign",
                                      description="This is a sample charity campaign.",
                                      authority=authority)
    o1 = Organization(organization_name='Organization', description='desc', approved=True, address=a1)
    sample_organization_campaign = OrganizationCharityCampaign(organization=o1, charity_campaign=sample_campaign)

    v1 = Volunteer(first_name='Michael', last_name='Johnson', email='mjohnson@mail.com', phone='957485273')
    aa1 = Address(street='Główna', street_number='4d', city='Gdańsk', voivodeship='Pomorskie')
    v1.address = aa1

    v2 = Volunteer(first_name='Jane', last_name='Doe', email='jdoe@mail.com', phone='823903283')
    aa2 = Address(street='Wiejska', street_number='2b', city='Warszawa', voivodeship='Mazowieckie')
    v2.address = aa2

    v3 = Volunteer(first_name='Alice', last_name='Smith', email='asmith@mail.com', phone='758292375')
    aa3 = Address(street='Krakowska', street_number='3c', city='Kraków', voivodeship='Małopolskie')
    v3.address = aa3

    sample_organization_campaign.volunteers.extend([v1, v2, v3])

    db.session.add_all([v1, v2, v3])
    db.session.add(sample_organization_campaign)
    db.session.commit()
    return redirect(url_for('organization.list_organization_charity_campaigns'))


@bp.route('/authorities/<int:authorities_id>')
def view_authorities(authorities_id):
    authority = db.session.get(Authorities, authorities_id)
    return render_template('view_authority.jinja', authorities=authority)


@bp.route('organization/<int:organization_id>')
def view_organization(organization_id):
    o1 = db.session.get(Organization, organization_id)
    return render_template('view_organization.jinja', organization=o1)


@bp.route('charity_campaign/<int:charity_campaign_id>')
def view_campaign(charity_campaign_id):
    cp = db.session.get(CharityCampaign, charity_campaign_id)
    return render_template('view_charity_campaign.jinja', campaign=cp)


@bp.route('/charity_campaign/<int:charity_campaign_id>/volunteers')
def list_volunteers(charity_campaign_id):
    campaign = db.session.get(OrganizationCharityCampaign, charity_campaign_id)
    volunteers = campaign.volunteers
    return render_template('list_volunteers.jinja', volunteers=volunteers)


@bp.route('/create_charity_campaign', methods=['GET', 'POST'])
def create_charity_campaign():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        authority_id = request.form['authority_id']
        authority = db.session.get(Authorities, authority_id)
        new_campaign = CharityCampaign(name=name, description=description, authority=authority)
        db.session.add(new_campaign)
        db.session.commit()
        return redirect(url_for('organization.list_charity_campaigns'))
    authorities = db.session.scalars(db.select(Authorities)).all()
    return render_template('create_charity_campaign.jinja', authorities=authorities)


@bp.route('/sign_to_charity_campaign', methods=['GET', 'POST'])
def sign_to_charity_campaign():
    if request.method == 'POST':
        organization_id = request.form['organization_id']
        charity_campaign_id = request.form['charity_campaign_id']
        organization = db.session.get(Organization, organization_id)
        charity_campaign = db.session.get(CharityCampaign, charity_campaign_id)
        new_organization_campaign = OrganizationCharityCampaign(organization=organization, charity_campaign=charity_campaign)
        db.session.add(new_organization_campaign)
        db.session.commit()
        return redirect(url_for('organization.list_organization_charity_campaigns'))
    organizations = db.session.scalars(db.select(Organization)).all()
    charity_campaigns = db.session.scalars(db.select(CharityCampaign)).all()
    return render_template('sign_to_charity_campaign.jinja', organizations=organizations, charity_campaigns=charity_campaigns)
