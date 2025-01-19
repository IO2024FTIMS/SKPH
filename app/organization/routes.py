from flask import Blueprint, render_template, redirect, url_for
from app.extensions import db
from app.models.address import Address
from app.models.authorities import Authorities
from app.models.charity_campaign import CharityCampaign, OrganizationCharityCampaign
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
    return render_template('list_organization_charity_campaigns.jinja', organization_charity_campaigns=organization_charity_campaigns)


@bp.route('/add_sample_charity_campaign')
def add_sample_charity_campaign():
    a1 = Address(street='Miejska', street_number='1a', city='Łódź', voivodeship='Łódzkie')
    authority = Authorities(name='John Doe', phone='123456789', approved=True, address=a1)
    sample_campaign = CharityCampaign(name="Sample Campaign", description="This is a sample charity campaign.", authority=authority)
    db.session.add(sample_campaign)
    db.session.commit()
    return redirect(url_for('organization.list_charity_campaigns'))


@bp.route('/add_sample_organization_charity_campaign')
def add_sample_organization_charity_campaign():
    a1 = Address(street='Miejska', street_number='1a', city='Łódź', voivodeship='Łódzkie')
    authority = Authorities(name='John Doe', phone='123456789', approved=True, address=a1)
    sample_campaign = CharityCampaign(name="Sample Campaign", description="This is a sample charity campaign.", authority=authority)
    o1 = Organization(organization_name='Organization', description='desc', approved=True, address=a1)
    sample_organization_campaign = OrganizationCharityCampaign(organization=o1, charity_campaign=sample_campaign)

    v1 = Volunteer(first_name='John', last_name='Black', email='jblack@mail.com', phone='111111111')
    aa1 = Address(street='Miejska', street_number='1a', city='Łódź', voivodeship='Łódzkie')
    v1.address = aa1
    sample_organization_campaign.volunteers.append(v1)

    db.session.add(v1)
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
    volunteers = campaign.volunteers  # if campaign and campaign.authority else []
    return render_template('list_volunteers.jinja', volunteers=volunteers)
