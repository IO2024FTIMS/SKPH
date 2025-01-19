from flask import Blueprint, render_template, redirect, url_for
from app import organization
from app.extensions import db
from app.models import charity_campaign
from app.models.address import Address
from app.models.authorities import Authorities
from app.models.charity_campaign import CharityCampaign, OrganizationCharityCampaign
from app.models.organization import Organization

bp = Blueprint('organization', __name__, template_folder='../templates/organization')


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
    db.session.add(sample_organization_campaign)
    db.session.commit()
    return redirect(url_for('organization.list_organization_charity_campaigns'))
