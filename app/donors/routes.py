from datetime import date
from flask import Blueprint, flash, redirect, render_template, url_for, request
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models.donation import DonationItem, DonationMoney
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


@bp.route('/all')
def fetch_donors():
    donors = db.session.scalars(db.select(Donor))
    return render_template('donor_view.jinja', donors=donors.all())


@bp.route('/tasks/create', methods=['GET', 'POST'])
def create_donation():
    donors = db.session.scalars(db.select(Donor))
    if request.method == 'POST':
        description = request.form['description']
        type = request.form['donation_type']
        donor_id = request.form['donor_id']
        amount = request.form['Amount']
        if type == 'money':
            new_donation_money = DonationMoney(
                description=description,
                donation_date=date.today(),
                donation_type="Money",
                cashAmount=amount,
                donor_id=donor_id
            )
            db.session.add(new_donation_money)
            db.session.commit()
            flash('money donated with id ' + str(new_donation_money.donationMoney_id))
            del new_donation_money

        if type == 'item':
            new_donation_item = DonationItem(
                description=description,
                donation_date=date.today(),
                donation_type="Item",
                number=amount,
                donor_id=donor_id
            )
            db.session.add(new_donation_item)
            db.session.commit()
            flash('item donated with id ' + str(new_donation_item.donationItem_id))
            del new_donation_item

        return redirect(url_for('donors.index'))

    return render_template('create_donation.jinja', donors=donors.all())


@bp.route('/donations/<int:donor_id>')
def list_donations(donor_id):
    donationsMoney = db.session.scalars(
        db.select(DonationMoney).where(DonationMoney.donor_id == donor_id)
    )
    donationsItems = db.session.scalars(
        db.select(DonationItem).where(DonationItem.donor_id == donor_id)
    )
    donor = db.session.get(Donor, donor_id)
    if Donor is None:
        return 'donor not found', 404
    return render_template('donations.jinja', donationsMoney=donationsMoney.all(), donor=donor,
                           donationsItems=donationsItems.all())


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
    del new_donation_item
    del new_donation_money

    return redirect(url_for('donors.index'))
