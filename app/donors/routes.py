from datetime import date

from flask import (Blueprint, abort, flash, redirect, render_template,
                   url_for)
from flask_login import current_user
from werkzeug.security import generate_password_hash

from app.auth.user_service import roles_required
from app.extensions import db
# from app.models.charity_campaign import OrganizationCharityCampaign
# from flask import request
from app.models.donation import DonationItem, DonationMoney, DonationType
from app.models.donor import Donor
from app.models.user import User

bp = Blueprint('donors', __name__,
               template_folder='../templates/donors',
               static_folder='static',
               static_url_path='donors')


@bp.route('/')
def index():
    samples_added = db.session.query(Donor).count() > 0
    return render_template('donors.jinja', samples_added=samples_added)


@bp.route('donor/profile')
@roles_required(['donor'])
def donor_profile():
    donor = db.session.get(Donor, current_user.donor.donor_id)
    return render_template('donor_profile.jinja', donor=donor)


@bp.route('/all')
@roles_required(['authorities'])
def fetch_donors():
    donors = db.session.scalars(db.select(Donor))
    return render_template('donor_view.jinja', donors=donors.all())

# TODO: Link the donation to a specific charity campaign


@bp.route('/donation/create', methods=['GET', 'POST'])
@roles_required(['donor'])
def create_donation():
    return redirect('/donors')
    # TODO - change behavior of DonationType
    # donor = db.session.scalar(db.select(Donor).where(Donor.donor_id == current_user.donor.donor_id))
    # if request.method == 'POST':
    #     description = request.form['description']
    #     type_d = request.form['donation_type']

    #     if type_d == 'money':
    #         amount = request.form['amount']
    #         new_donation_money = DonationMoney(
    #             description=description,
    #             donation_date=date.today(),
    #             donation_type="Money",
    #             cashAmount=amount,
    #             donor_id=donor.donor_id
    #         )
    #         db.session.add(new_donation_money)
    #         db.session.commit()
    #         flash('Donation created successfully')
    #         del new_donation_money

    #     if type_d == 'item':
    #         item_type = request.form['item_donation_type']
    #         item_count = request.form['count']
    #         new_donation_item = DonationItem(
    #             description=description,
    #             donation_date=date.today(),
    #             donation_type=ItemDonation(item_type),
    #             number=item_count,
    #             donor_id=donor.donor_id
    #         )
    #         db.session.add(new_donation_item)
    #         db.session.commit()
    #         flash('Donation created successfully')
    #         del new_donation_item

    #     return redirect(url_for('donors.list_donations', donor_id=donor.donor_id))
    # charity_campaigns = db.session.scalars(db.select(OrganizationCharityCampaign)).all()
    # return render_template('create_donation.jinja',
    #                        charity_campaigns=charity_campaigns,
    #                        ItemDonationType=ItemDonationType)


@bp.route('/donations/<int:donor_id>')
@roles_required(['donor', 'organization', 'authorities'])
def list_donations(donor_id):
    if current_user.type == 'donor':
        if current_user.donor.donor_id != donor_id:
            return abort(403)

    donor = db.session.get(Donor, donor_id)
    if Donor is None:
        return 'Donor not found', 404

    donations_money = db.session.scalars(
        db.select(DonationMoney).where(DonationMoney.donor_id == donor_id)
    )
    donations_items = db.session.scalars(
        db.select(DonationItem).where(DonationItem.donor_id == donor_id)
    )

    return render_template('donations.jinja', donations_money=donations_money.all(), donor=donor,
                           donations_items=donations_items.all())


@bp.route('/samples', methods=['POST'])
def donor_samples():
    if db.session.query(Donor).count() > 0:
        flash('EXISTING DATA FOUND, NOT ADDED!')
        return redirect(url_for('volunteers.index'))

    new_user = User(
        email="john.doe@example.com",
        password_hash=generate_password_hash("secure_password123"),
        active=True,
        type="donor"
    )

    db.session.add(new_user)
    db.session.commit()
    db.session.refresh(new_user)

    new_donor = Donor(
        name="John",
        surname="Doe",
        phone_number="123456789",
        email="john.doe@example.com",
        user_id=new_user.id
    )
    db.session.add(new_donor)
    db.session.commit()
    db.session.refresh(new_donor)

    donation_type_1 = DonationType('Food')
    donation_type_2 = DonationType('Clothes')

    db.session.add(donation_type_1)
    db.session.add(donation_type_2)

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
        donation_type=donation_type_1,
        number=10,
        donor_id=new_donor.donor_id
    )
    db.session.add(new_donation_item)
    db.session.commit()
    del new_donation_item
    del new_donation_money

    return redirect(url_for('donors.index'))
