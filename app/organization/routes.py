from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

from app.extensions import db
from app.models.address import Address
from app.models.authorities import Authorities
from app.models.charity_campaign import (CharityCampaign,
                                         OrganizationCharityCampaign)
from app.models.evaluation import Evaluation
from app.models.organization import Organization
from app.models.task import Task
from app.models.volunteer import Volunteer
from app.utils.helpers import role_required

bp = Blueprint('organization', __name__, template_folder='../templates/organization')


@bp.route('/')
def index():
    return render_template('organization_index.jinja')


@bp.route('/charity_campaigns')
@role_required(['volunteer', 'donor'])  # example of access management
def list_charity_campaigns():
    charity_campaigns = db.session.scalars(db.select(CharityCampaign)).all()
    return render_template('list_charity_campaigns.jinja', charity_campaigns=charity_campaigns)


@bp.route('/organization_charity_campaigns')
def list_organization_charity_campaigns():
    organization_charity_campaigns = db.session.scalars(db.select(OrganizationCharityCampaign)).all()
    return render_template('list_organization_charity_campaigns.jinja',
                           organization_charity_campaigns=organization_charity_campaigns)


@bp.route('/add_sample_charity_campaign')  # NOTE: not neccesary
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
    address1 = Address(street='Miejska', street_number='1a', city='Łódź', voivodeship='Łódzkie')
    authority1 = Authorities(name='Aleksander Wika', phone='758934576', approved=True, address=address1)
    sample_campaign = CharityCampaign(name="Pomoc Dla Powodzian",
                                      description="Akcja ma na celu pomoc osobą dotkniętych powodzią na Dolnym Śląsku",
                                      authority=authority1)
    organization1 = Organization(organization_name='Fundacja Siepomaga',
                                 description='Fundacja Siepomaga powstała, by osiągać to,\
                                    co na pierwszy rzut oka wydaje się niemożliwe.\
                                    Ratujemy życie i zdrowie, które wyceniono na kwoty\
                                    niemożliwe do osiągnięcia przez Potrzebujących.',
                                 approved=True, address=address1)
    sample_organization_campaign = OrganizationCharityCampaign(organization=organization1,
                                                               charity_campaign=sample_campaign)

    volunteer1 = Volunteer(first_name='Michael', last_name='Johnson', email='mjohnson@mail.com', phone='957485273')
    address2 = Address(street='Główna', street_number='4d', city='Gdańsk', voivodeship='Pomorskie')
    volunteer1.address = address2

    volunteer2 = Volunteer(first_name='Jane', last_name='Doe', email='jdoe@mail.com', phone='823903283')
    address3 = Address(street='Wiejska', street_number='2b', city='Warszawa', voivodeship='Mazowieckie')
    volunteer2.address = address3

    volunteer3 = Volunteer(first_name='Alice', last_name='Smith', email='asmith@mail.com', phone='758292375')
    address4 = Address(street='Krakowska', street_number='3c', city='Kraków', voivodeship='Małopolskie')
    volunteer3.address = address4

    sample_organization_campaign.volunteers.extend([volunteer1, volunteer2, volunteer3])

    db.session.add_all([volunteer1, volunteer2, volunteer3])
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
@role_required(['organization', 'authorities', 'admin'])
def list_volunteers(charity_campaign_id):
    campaign = db.session.get(OrganizationCharityCampaign, charity_campaign_id)
    volunteers = campaign.volunteers
    return render_template('list_volunteers.jinja', volunteers=volunteers)


@bp.route('/create_charity_campaign', methods=['GET', 'POST'])
@role_required(['authorities', 'admin'])
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
@role_required(['organization', 'admin'])
def sign_to_charity_campaign():
    if request.method == 'POST':
        organization_id = request.form['organization_id']
        charity_campaign_id = request.form['charity_campaign_id']
        organization = db.session.get(Organization, organization_id)
        charity_campaign = db.session.get(CharityCampaign, charity_campaign_id)
        new_organization_campaign = OrganizationCharityCampaign(organization=organization,
                                                                charity_campaign=charity_campaign)
        db.session.add(new_organization_campaign)
        db.session.commit()
        return redirect(url_for('organization.list_organization_charity_campaigns'))
    organizations = db.session.scalars(db.select(Organization)).all()
    charity_campaigns = db.session.scalars(db.select(CharityCampaign)).all()
    return render_template('sign_to_charity_campaign.jinja',
                           organizations=organizations,
                           charity_campaigns=charity_campaigns)


@bp.route('/volunteer_sign_to_charity_campaign', methods=['GET', 'POST'])
@role_required(['volunteer'])
def volunteer_sign_to_charity_campaign():
    if request.method == 'POST':
        organization_charity_campaign_id = request.form['organization_charity_campaign_id']
        volunteer = db.session.scalar(db.select(Volunteer).where(Volunteer.user_id == current_user.id))
        organization_campaign = db.session.get(OrganizationCharityCampaign, organization_charity_campaign_id)

        if organization_campaign and volunteer:
            organization_campaign.volunteers.append(volunteer)
            db.session.commit()
            return redirect(url_for('organization.list_volunteers',
                                    charity_campaign_id=organization_charity_campaign_id))

    organization_charity_campaigns = db.session.scalars(db.select(OrganizationCharityCampaign)).all()
    return render_template('volunteer_sign_to_charity_campaign.jinja',
                           organization_charity_campaigns=organization_charity_campaigns)


@bp.route('/charity_campaign/<int:organization_charity_campaign_id>/tasks/create', methods=['GET', 'POST'])
@role_required(['organization', 'admin'])
def create_task(organization_charity_campaign_id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        volunteer_id = request.form['volunteer_id']
        new_task = Task(name=name, description=description,
                        volunteer_id=volunteer_id, charity_campaign_id=organization_charity_campaign_id)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('ogranization.list_volunteers', charity_campaign_id=organization_charity_campaign_id))
    organization_campaign = db.session.get(OrganizationCharityCampaign, organization_charity_campaign_id)
    return render_template('create_task_campaign.jinja',
                           volunteers=organization_campaign.volunteers,
                           campaign=organization_campaign)


@bp.route('/charity_campaign/<int:charity_campaign_id>/tasks/evaluate/<int:task_id>', methods=['GET', 'POST'])
@role_required(['organization', 'admin'])
def eval_task(task_id):
    task = db.session.query(Task).filter_by(id=task_id).first()
    if task is None:
        flash('Task not found.')
        return redirect(url_for('volunteers.fetch_all'))

    if request.method == 'POST':
        if not task.evaluation_:
            score = request.form['score']
            description = request.form['description']
            task_evaluation = Evaluation(score=score, description=description)
            task.evaluation_ = task_evaluation
            db.session.add(task)
            db.session.commit()
            flash('Evaluation added successfully!')
        else:
            flash('Task is already evaluated.')
        return redirect(url_for('volunteers.list_tasks', volunteer_id=task.volunteer.id))

    return render_template('eval_task.jinja', task=task)


@bp.route('/organizations')
def list_organizations():
    organizations = db.session.scalars(db.select(Organization)).all()
    return render_template('list_organizations.jinja', organizations=organizations)
