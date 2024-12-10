from flask import Blueprint, redirect, render_template, request, url_for

from app.extensions import db

bp = Blueprint("volunteers", __name__,
               template_folder="../templates/volunteers",
               static_folder="static",
               static_url_path="volunteers")


@bp.route('/')
def index():
    return '<h1>Volunteers Module<h1>', 200


@bp.route('/all')
def fetch_all():
    from app.models.volunteer import Volunteer
    volunteers = db.session.scalars(db.select(Volunteer))
    return render_template('view.jinja', volunteers=volunteers.all())


@bp.route('/samples')
def samples():
    from app.models.address import Address
    from app.models.task import Task
    from app.models.volunteer import Volunteer
    with db.session() as session:
        v1 = Volunteer(first_name='Wiktor', last_name='Stepniewski', email='ws', phone='wsphone')
        a1 = Address(street='Pomorska', street_number='42a', city='Lodz', voivodeship='Lodzkie')
        v1.address = a1
        t1 = Task(name='Test task', description='TestDesc', volunteer=v1)
        v1.tasks.append(t1)
        session.add(v1)
        session.commit()
    return "Samples added to db", 200


@bp.route('/tasks/<int:volunteer_id>')
def list_tasks(volunteer_id):
    from app.models.volunteer import Volunteer
    volunteer = db.session.get(Volunteer, volunteer_id)
    if volunteer is None:
        return "Volunteer not found", 404
    return render_template('tasks.jinja', volunteer=volunteer)


@bp.route('/tasks/create', methods=['GET', 'POST'])
def create_task():
    from app.models.task import Task
    from app.models.volunteer import Volunteer
    volunteers = db.session.scalars(db.select(Volunteer))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        volunteer_id = request.form['volunteer_id']

        new_task = Task(name=name, description=description, volunteer_id=volunteer_id)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('volunteers.index'))

    return render_template('create_task.jinja', volunteers=volunteers.all())


@bp.route('/tasks/evaluate/<int:task_id>', methods=['GET', 'POST'])
def eval_task(task_id):
    from app.models.evaluation import Evaluation
    from app.models.task import Task

    task = db.session.scalar(db.select(Task, task_id))
    if request.method == 'POST':
        score = request.form['score']
        description = request.form['description']

        task_evaluation = Evaluation(score=score, description=description)
        task.evaluation_ = task_evaluation
        db.session.add(task)
        db.session.commit()

    return render_template('eval_task.jinja', task=task)
