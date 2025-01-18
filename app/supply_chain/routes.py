from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.extensions import db

from app.models.volunteer import Volunteer
from app.models.organization import Organization
from app.models.address import Address
from app.models.affected import Affected


bp = Blueprint('supply_chain', __name__, 
               template_folder='../templates/supply_chain',
               static_folder='static',
               static_url_path='supply_chain')


@bp.route('/')
def index():
    volunteers = db.session.query(Volunteer)
    return render_template('supply_chain.jinja', volunteers=volunteers)