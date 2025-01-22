from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.extensions import db
from app.models.address import Address
from app.models.affected import Affected
from app.models.request import Request, RequestStatus

bp = Blueprint('affected', __name__,
               template_folder='../templates/affected',
               static_folder='static',
               static_url_path='affected')


@bp.route('/')
def index():
    samples_added = db.session.query(Affected).count() > 0
    affected = db.session.scalars(db.select(Affected))
    return render_template('affected.jinja', samples_added=samples_added, affected=affected.all())


@bp.route('/all')
def fetch_all():
    affected = db.session.scalars(db.select(Affected))
    return render_template('all.jinja', affected=affected.all())


@bp.route('/samples', methods=['POST'])
def samples():
    if db.session.query(Affected).count() > 0:
        flash('Sample data already added!')
        return redirect(url_for('affected.index'))

    with db.session() as session:
        # Tworzenie przykładowych osób poszkodowanych
        aff1 = Affected(first_name='Geto', last_name='Mill', needs='Shelter')
        a1 = Address(street='Miejska', street_number='1a', city='Łódź', voivodeship='Łódzkie')
        aff1.address = a1

        aff2 = Affected(first_name='Lukas', last_name='Steven', needs='Food')
        a2 = Address(street='Wiejska', street_number='2b', city='Warsaw', voivodeship='Mazowieckie')
        aff2.address = a2

        session.add(aff1)
        session.add(aff2)

        # Tworzenie przykładowego requesta dla pierwszego poszkodowanego
        req1_address = Address(street='Pomocna', street_number='10', city='Gdańsk', voivodeship='Pomorskie')
        req2_address = Address(street='Pomocna', street_number='10', city='Gdańsk', voivodeship='Pomorskie')
        session.add(req1_address)
        session.add(req2_address)
        session.flush()  # Upewnij się, że ID adresu jest dostępne

        req1 = Request(
            name='Food Assistance',
            status=RequestStatus.PENDING,
            req_address=req1_address,
            needs='Food',
            affected_id=aff1.id
        )
        req2 = Request(
            name='Shelter needed',
            status=RequestStatus.PENDING,
            req_address=req2_address,
            needs='Shelter',
            affected_id=aff2.id
        )
        session.add(req1)
        session.add(req2)
        session.commit()

    flash('Sample data added successfully!')
    return redirect(url_for('affected.index'))


@bp.route('/select_affected', methods=['GET', 'POST'])
def select_affected():
    if request.method == 'POST':
        affected_id = request.form['affected_id']
        return redirect(url_for('affected.create_request', affected_id=affected_id))

    affected = db.session.scalars(db.select(Affected))
    return render_template('select_affected.jinja', affected=affected.all())


@bp.route('/request/create/<int:affected_id>', methods=['GET', 'POST'])
def create_request(affected_id):
    affected = db.get_or_404(Affected, affected_id)

    if request.method == 'POST':
        name = request.form['name']
        status = RequestStatus.PENDING
        needs = request.form.get('needs')
        street = request.form['street']
        street_number = request.form['street_number']
        city = request.form['city']
        voivodeship = request.form['voivodeship']

        # Validation
        if not all([name, needs, street, street_number, city, voivodeship]):
            return redirect(url_for('affected.create_request', affected_id=affected_id))

        # Create new address
        new_address = Address(
            street=street,
            street_number=street_number,
            city=city,
            voivodeship=voivodeship
        )
        db.session.add(new_address)
        db.session.commit()

        # Create new request
        new_request = Request(
            name=name,
            status=status,
            req_address=new_address,
            needs=needs,
            affected_id=affected_id
        )
        db.session.add(new_request)
        db.session.commit()

        return redirect(url_for('affected.affected_details', affected_id=affected_id))

    return render_template('create_request.jinja', affected=affected)


@bp.route('/requests')
def all_requests():
    requests = db.session.scalars(db.select(Request)).all()

    return render_template('all_requests.jinja', requests=requests)


@bp.route('/affected/<int:affected_id>')
def affected_details(affected_id):
    affected = db.get_or_404(Affected, affected_id)

    requests = db.session.query(Request).filter_by(affected_id=affected_id).all()

    return render_template('affected_details.jinja', affected=affected, requests=requests, RequestStatus=RequestStatus)


@bp.route('/request/update_status/<int:request_id>', methods=['GET', 'POST'])
def update_request_status(request_id):
    request_obj = db.get_or_404(Request, request_id)

    if request.method == 'POST':
        new_status = request.form.get('status')
        if new_status not in RequestStatus.__members__:
            return redirect(url_for('affected.update_request_status', request_id=request_id))

        request_obj.status = RequestStatus[new_status]
        db.session.commit()

        return redirect(url_for('affected.affected_details', affected_id=request_obj.affected_id))

    return render_template('update_request_status.jinja', request=request_obj, statuses=RequestStatus)


@bp.route('/request/edit/<int:request_id>', methods=['GET', 'POST'])
def edit_request(request_id):
    request_obj = db.get_or_404(Request, request_id)

    # Tylko requesty w statusie PENDING mogą być edytowane
    if request_obj.status != RequestStatus.PENDING:
        return redirect(url_for('affected.affected_details', affected_id=request_obj.affected_id))

    if request.method == 'POST':
        name = request.form.get('name')
        needs = request.form.get('needs')
        street = request.form.get('street')
        street_number = request.form.get('street_number')
        city = request.form.get('city')
        voivodeship = request.form.get('voivodeship')

        # Walidacja
        if not all([name, needs, street, street_number, city, voivodeship]):
            return redirect(url_for('affected.edit_request', request_id=request_id))

        # Aktualizacja danych
        request_obj.name = name
        request_obj.needs = needs
        request_obj.req_address.street = street
        request_obj.req_address.street_number = street_number
        request_obj.req_address.city = city
        request_obj.req_address.voivodeship = voivodeship

        db.session.commit()

        return redirect(url_for('affected.affected_details', affected_id=request_obj.affected_id))

    return render_template('edit_request.jinja', request=request_obj)


@bp.route('/request/delete/<int:request_id>', methods=['POST', 'GET'])
def delete_request(request_id):
    request_obj = db.get_or_404(Request, request_id)

    # Only delete requests with the PENDING status
    if request_obj.status != RequestStatus.PENDING:
        return redirect(url_for('affected.affected_details', affected_id=request_obj.affected_id))

    # Delete the request and its associated address
    affected_id = request_obj.affected_id
    db.session.delete(request_obj.req_address)  # First delete the address
    db.session.delete(request_obj)  # Then delete the request
    db.session.commit()

    return redirect(url_for('affected.affected_details', affected_id=affected_id))
