from flask import Blueprint, Response, render_template
import csv
import io

from .chart_utils import create_bar_chart_base64
from .report_service import ReportService
from app.extensions import db
from app.models.affected import Affected
from app.models.volunteer import Volunteer

bp = Blueprint("reports", __name__, template_folder="templates/reports", static_folder="../static/reports")

report_service = ReportService()

@bp.route('/ui', methods=['GET'])
def ui():
    """
    Strona główna z dwoma przyciskami:
    - Raport Affected
    - Raport Volunteer
    """
    return render_template('reports/reports_ui.jinja')


# =================== RAPORT AFFECTED ===================

@bp.route('/affected-report', methods=['GET'])
def affected_report():
    affected_list = db.session.query(Affected).all()

    city_stats = report_service.stats_by_city()  # Affected wg miasta
    voiv_stats = report_service.stats_by_voivodeship()  # wg województwa
    needs_stats = report_service.stats_by_needs()  # wg needs

    city_chart_b64 = create_bar_chart_base64(city_stats, "Affected wg Miasta")
    voiv_chart_b64 = create_bar_chart_base64(voiv_stats, "Affected wg Województwa")
    needs_chart_b64 = create_bar_chart_base64(needs_stats, "Affected wg Needs")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8"/>
      <title>Raport Affected</title>
      <link rel="stylesheet" type="text/css" href="../../static/style.css">
    </head>
    <body class="bg-light">
      <div class="container mt-5">
        <h1 class="text-primary text-center">Raport Affected</h1>
        <p>Statystyki dotyczące poszkodowanych (Affected).</p>

        <h2>1. Wykresy</h2>
        <h3>1.1. Wg Miasta</h3>
        <img src="data:image/png;base64,{city_chart_b64}" alt="Chart by city" />

        <h3>1.2. Wg Województwa</h3>
        <img src="data:image/png;base64,{voiv_chart_b64}" alt="Chart by voivodeship" />

        <h3>1.3. Wg Needs</h3>
        <img src="data:image/png;base64,{needs_chart_b64}" alt="Chart by needs" />

        <hr/>
        <h2>2. Lista Affected</h2>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>ID</th>
              <th>Imię</th>
              <th>Nazwisko</th>
              <th>Needs</th>
              <th>Miasto</th>
              <th>Województwo</th>
            </tr>
          </thead>
          <tbody>
    """
    for aff in affected_list:
        city = aff.address.city if aff.address else ""
        voiv = aff.address.voivodeship if aff.address else ""
        html += f"""
            <tr>
              <td>{aff.id}</td>
              <td>{aff.first_name}</td>
              <td>{aff.last_name}</td>
              <td>{aff.needs or ""}</td>
              <td>{city}</td>
              <td>{voiv}</td>
            </tr>
        """

    html += """
          </tbody>
        </table>
        <div class="mt-4">
          <a href="/reports/affected-report-csv" class="btn btn-success">Pobierz CSV</a>
          <a href="/reports/ui" class="btn btn-secondary">Powrót</a>
        </div>
      </div>
    </body>
    </html>
    """
    return html


@bp.route('/affected-report-csv', methods=['GET'])
def affected_report_csv():
    affected_list = db.session.query(Affected).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "First Name", "Last Name", "Needs", "City", "Voivodeship"])

    for aff in affected_list:
        city = aff.address.city if aff.address else ""
        voiv = aff.address.voivodeship if aff.address else ""
        writer.writerow([
            aff.id, aff.first_name, aff.last_name, aff.needs or "", city, voiv
        ])

    csv_data = output.getvalue()
    output.close()

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=affected_report.csv"}
    )


# =================== RAPORT VOLUNTEER ===================

@bp.route('/volunteer-report', methods=['GET'])
def volunteer_report():
    volunteer_list = report_service.get_all_volunteers()

    city_stats = report_service.stats_by_city_volunteer()
    tasks_stats = report_service.stats_volunteer_task_count()

    city_chart_b64 = create_bar_chart_base64(city_stats, "Volunteer wg Miasta")
    tasks_chart_b64 = create_bar_chart_base64(tasks_stats, "Volunteer wg liczby zadań (Task)")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8"/>
      <title>Raport Volunteer</title>
      <link rel="stylesheet" type="text/css" href="../../static/style.css">
    </head>
    <body class="bg-light">
      <div class="container mt-5">
        <h1 class="text-primary text-center">Raport Volunteer</h1>
        <p>Statystyki wolontariuszy.</p>

        <h2>1. Wykresy</h2>
        <h3>1.1. Wg Miasta</h3>
        <img src="data:image/png;base64,{city_chart_b64}" alt="Volunteer by city" />

        <h3>1.2. Wg liczby zadań</h3>
        <img src="data:image/png;base64,{tasks_chart_b64}" alt="Volunteer tasks count" />

        <hr/>
        <h2>2. Lista Volunteer</h2>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>ID</th>
              <th>Imię</th>
              <th>Nazwisko</th>
              <th>Email</th>
              <th>Telefon</th>
              <th>Miasto</th>
              <th>Województwo</th>
              <th>Liczba Tasków</th>
            </tr>
          </thead>
          <tbody>
    """
    for vol in volunteer_list:
        city = vol.address.city if vol.address else ""
        voiv = vol.address.voivodeship if vol.address else ""
        tasks_count = len(vol.tasks) if vol.tasks else 0
        html += f"""
            <tr>
              <td>{vol.id}</td>
              <td>{vol.first_name}</td>
              <td>{vol.last_name}</td>
              <td>{vol.email}</td>
              <td>{vol.phone}</td>
              <td>{city}</td>
              <td>{voiv}</td>
              <td>{tasks_count}</td>
            </tr>
        """

    html += """
          </tbody>
        </table>
        <div class="mt-4">
          <a href="/reports/volunteer-report-csv" class="btn btn-success">Pobierz CSV</a>
          <a href="/reports/ui" class="btn btn-secondary">Powrót</a>
        </div>
      </div>
    </body>
    </html>
    """
    return html

@bp.route('/volunteer-report-csv', methods=['GET'])
def volunteer_report_csv():
    volunteer_list = report_service.get_all_volunteers()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "First Name", "Last Name", "Email", "Phone", "City", "Voivodeship", "Tasks Count"])
    for vol in volunteer_list:
        city = vol.address.city if vol.address else ""
        voiv = vol.address.voivodeship if vol.address else ""
        tasks_count = len(vol.tasks) if vol.tasks else 0
        writer.writerow([
            vol.id, vol.first_name, vol.last_name, vol.email, vol.phone, city, voiv, tasks_count
        ])
    csv_data = output.getvalue()
    output.close()

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=volunteer_report.csv"}
    )
