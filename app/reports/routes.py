import csv
import io

from flask import Blueprint, Response, render_template, request

from app.extensions import db
from app.models.affected import Affected

from .chart_utils import create_bar_chart_base64
from .report_service import ReportService

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

# =================== RAPORT DONOR ===================


@bp.route('/donor-report', methods=['GET'])
def donor_report():
    donors = report_service.get_all_donors()

    type_count_stats = report_service.stats_donation_type_count()
    sums_stats = report_service.stats_donation_sums()

    type_chart_b64 = create_bar_chart_base64(type_count_stats, "Donations: Money vs. Items")
    sums_chart_b64 = create_bar_chart_base64(sums_stats, "Total sums: cashAmount vs. item number")

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8"/>
      <title>Raport Donor</title>
      <link rel="stylesheet" type="text/css" href="../../static/style.css">
    </head>
    <body class="bg-light">
      <div class="container mt-5">
        <h1 class="text-primary text-center">Raport Donor</h1>
        <p>Statystyki darczyńców (Donor) i ich darowizn (Money / Items).</p>

        <h2>1. Wykresy</h2>
        <h3>1.1. Liczba darowizn (Money vs. Item)</h3>
        <img src="data:image/png;base64,{type_chart_b64}" alt="Money vs. Item" />

        <h3>1.2. Łączna suma (pieniędzy vs. liczba przedmiotów)</h3>
        <img src="data:image/png;base64,{sums_chart_b64}" alt="Sums chart" />

        <hr/>
        <h2>2. Lista Darczyńców (Donor)</h2>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>Donor ID</th>
              <th>Imię</th>
              <th>Nazwisko</th>
              <th>Email</th>
              <th>Telefon</th>
              <th>Liczba darowizn pieniężnych</th>
              <th>Liczba darowizn rzeczowych</th>
            </tr>
          </thead>
          <tbody>
    """
    for donor in donors:
        money_count = len(donor.donations_money) if donor.donations_money else 0
        item_count = len(donor.donations_items) if donor.donations_items else 0
        html_content += f"""
            <tr>
              <td>{donor.donor_id}</td>
              <td>{donor.name}</td>
              <td>{donor.surname}</td>
              <td>{donor.email}</td>
              <td>{donor.phone_number}</td>
              <td>{money_count}</td>
              <td>{item_count}</td>
            </tr>
        """

    html_content += """
          </tbody>
        </table>
        <div class="mt-4">
          <a href="/reports/donor-report-csv" class="btn btn-success">Pobierz CSV</a>
          <a href="/reports/ui" class="btn btn-secondary">Powrót</a>
        </div>
      </div>
    </body>
    </html>
    """
    return html_content


@bp.route('/donor-report-csv', methods=['GET'])
def donor_report_csv():
    donors = report_service.get_all_donors()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Donor ID", "Name", "Surname", "Email", "Phone number",
                     "Money donations count", "Item donations count"])

    for donor in donors:
        money_count = len(donor.donations_money) if donor.donations_money else 0
        item_count = len(donor.donations_items) if donor.donations_items else 0
        writer.writerow([
            donor.donor_id,
            donor.name,
            donor.surname,
            donor.email,
            donor.phone_number,
            money_count,
            item_count
        ])

    csv_data = output.getvalue()
    output.close()

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=donor_report.csv"}
    )


@bp.route('/single-donor-report', methods=['GET'])
def single_donor_report():
    donor_id = request.args.get('donor_id', type=int)
    if not donor_id:
        return "<h3>Brak parametru donor_id!</h3>", 400

    from app.models.donor import Donor
    donor = db.session.get(Donor, donor_id)
    if not donor:
        return f"<h3>Donor o ID={donor_id} nie istnieje!</h3>", 404

    money_list = donor.donations_money
    item_list = donor.donations_items

    total_money_sum = sum(dm.cashAmount for dm in money_list)
    total_item_sum = sum(di.number for di in item_list)
    money_count = len(money_list)
    item_count = len(item_list)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8"/>
      <title>Raport dla Donora ID={donor_id}</title>
      <link rel="stylesheet" type="text/css" href="../../static/style.css">
    </head>
    <body class="bg-light">
      <div class="container mt-5">
        <h1 class="text-primary">Raport dla Donora (ID={donor_id})</h1>
        <p>
          Imię i nazwisko: <strong>{donor.name} {donor.surname}</strong><br/>
          Email: <strong>{donor.email}</strong><br/>
          Telefon: <strong>{donor.phone_number}</strong><br/>
        </p>

        <h2>Statystyki darowizn</h2>
        <ul>
          <li>Liczba darowizn pieniężnych: <strong>{money_count}</strong></li>
          <li>Liczba darowizn rzeczowych: <strong>{item_count}</strong></li>
          <li>Łączna kwota darowizn pieniężnych: <strong>{total_money_sum}</strong></li>
          <li>Łączna liczba rzeczy: <strong>{total_item_sum}</strong></li>
        </ul>

        <hr/>
        <h3>Lista darowizn pieniężnych</h3>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>ID</th>
              <th>Opis</th>
              <th>Data</th>
              <th>Kwota</th>
            </tr>
          </thead>
          <tbody>
    """
    for dm in money_list:
        html += f"""
            <tr>
              <td>{dm.donationMoney_id}</td>
              <td>{dm.description}</td>
              <td>{dm.donation_date}</td>
              <td>{dm.cashAmount}</td>
            </tr>
        """

    html += """
          </tbody>
        </table>

        <hr/>
        <h3>Lista darowizn rzeczowych</h3>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>ID</th>
              <th>Opis</th>
              <th>Data</th>
              <th>Rodzaj</th>
              <th>Liczba</th>
            </tr>
          </thead>
          <tbody>
    """
    for di in item_list:
        html += f"""
            <tr>
              <td>{di.donationItem_id}</td>
              <td>{di.description}</td>
              <td>{di.donation_date}</td>
              <td>{di.donation_type}</td>
              <td>{di.number}</td>
            </tr>
        """

    html += f"""
          </tbody>
        </table>

        <hr/>
        <div class="mt-4">
          <a href="/reports/single-donor-report-csv?donor_id={donor_id}" class="btn btn-success">
            Pobierz CSV (ten donor)
          </a>
          <a href="/reports/ui" class="btn btn-secondary">Powrót</a>
        </div>
      </div>
    </body>
    </html>
    """
    return html


@bp.route('/single-donor-report-csv', methods=['GET'])
def single_donor_report_csv():
    donor_id = request.args.get('donor_id', type=int)
    if not donor_id:
        return "Brak parametru donor_id", 400

    from app.models.donor import Donor
    donor = db.session.get(Donor, donor_id)
    if not donor:
        return f"Donor o ID={donor_id} nie istnieje!", 404

    output = io.StringIO()
    fieldnames = [
        "donation_kind",
        "donation_id",
        "description",
        "donation_date",
        "donation_type",
        "amount"
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for dm in donor.donations_money:
        row = {
            "donation_kind": "MONEY",
            "donation_id": dm.donationMoney_id,
            "description": dm.description,
            "donation_date": dm.donation_date,
            "donation_type": dm.donation_type,
            "amount": dm.cashAmount
        }
        writer.writerow(row)

    for di in donor.donations_items:
        row = {
            "donation_kind": "ITEM",
            "donation_id": di.donationItem_id,
            "description": di.description,
            "donation_date": di.donation_date,
            "donation_type": di.donation_type,
            "amount": di.number
        }
        writer.writerow(row)

    csv_data = output.getvalue()
    output.close()

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename=donor_{donor_id}_report.csv"}
    )
