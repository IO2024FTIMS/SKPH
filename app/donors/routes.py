from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models.address import Address
from app.models.donation import DonationItem,DonationMoney
from app.models.donor import Donor
from app.models.evaluation import Evaluation
from app.models.task import Task
from app.models.user import User
from app.models.volunteer import Volunteer


bp = Blueprint('donors', __name__,
               template_folder='../templates/donors',
               static_folder='static',
               static_url_path='donors')

@bp.route('/')
def index():
    samples_added = db.session.query(Donor).count() > 0
    return render_template('donors.jinja', samples_added=samples_added)


@bp.route('/samples', methods=['GET'])
def samples():
    if db.session.query(Donor).count() > 0:
        flash('Sample data already added!')
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


    return redirect(url_for('volunteers.index'))


