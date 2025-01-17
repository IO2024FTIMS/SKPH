from flask import Blueprint, render_template, request, Response, jsonify
from .report_service import ReportService
from .report_generator import ReportGenerator
from app.extensions import db
from app.models.affected import Affected
from .chart_utils import create_bar_chart_base64

bp = Blueprint("reports", __name__, template_folder="templates/reports", static_folder="../static/reports")

report_service = ReportService()

@bp.route('/')
def index():
    return "We are in reports/"

@bp.route('/all')
def fetch_all():
    reports = report_service.get_all_reports()
    return render_template('reports/view.jinja', reports=reports)

@bp.route('/generate', methods=['GET'])
def generate_report():
    new_report = report_service.generate_report()
    return jsonify(new_report.to_dict()), 201

@bp.route('/view', methods=['GET'])
def view_reports():
    reports = report_service.get_all_reports()
    return jsonify([r.to_dict() for r in reports]), 200

@bp.route('/export', methods=['GET'])
def export_report():
    report_id = request.args.get('report_id', type=int)
    if not report_id:
        return jsonify({"error": "Missing report_id parameter"}), 400

    report = report_service.get_report_by_id(report_id)
    if not report:
        return jsonify({"error": "Report not found"}), 404

    csv_data = ReportGenerator.to_csv(report)
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={"Content-disposition": f"attachment; filename=report_{report_id}.csv"}
    )

@bp.route('/ui', methods=['GET'])
def ui():
    return render_template('reports/reports_ui.jinja')

@bp.route('/affected', methods=['GET'])
def show_affected():
    affected_list = db.session.query(Affected).all()
    return render_template('reports/affected_view.jinja', affected_list=affected_list)
@bp.route('/affected/export', methods=['GET'])
def affected_csv():
    affected_list = db.session.query(Affected).all()

    import csv
    import io

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "First Name", "Last Name", "Needs", "City", "Voivodeship"])

    for aff in affected_list:
        city = aff.address.city if aff.address else ""
        voiv = aff.address.voivodeship if aff.address else ""
        writer.writerow([
            aff.id,
            aff.first_name,
            aff.last_name,
            aff.needs or "",
            city,
            voiv
        ])

    csv_data = output.getvalue()
    output.close()

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=affected.csv"}
    )

@bp.route('/affected/detailed', methods=['GET'])
def affected_detailed():
    affected_list = db.session.query(Affected).all()
    city_stats = report_service.stats_by_city()
    voiv_stats = report_service.stats_by_voivodeship()
    needs_stats = report_service.stats_by_needs()

    city_chart = create_bar_chart_base64(city_stats, "Liczba poszkodowanych wg Miasta")
    voiv_chart = create_bar_chart_base64(voiv_stats, "Liczba poszkodowanych wg Województwa")
    needs_chart = create_bar_chart_base64(needs_stats, "Rozkład NEEDS (rodzaj pomocy)")

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"/>
        <title>Raport Affected (szczegółowy)</title>
        <link rel="stylesheet" type="text/css" href="../../static/style.css">
    </head>
    <body class="bg-light">
        <div class="container mt-5">
            <h1 class="text-primary text-center">Bogaty raport poszkodowanych</h1>
            <p>
                Poniżej znajduje się zestaw statystyk dotyczących tabeli <strong>Affected</strong>,
                w tym liczba osób w danym mieście, województwie oraz rozkład typów potrzeb (<em>needs</em>).
            </p>

            <h2>1. Statystyki i wykresy</h2>
            <h3>1.1. Liczba poszkodowanych wg Miasta</h3>
            <img src="data:image/png;base64,{city_chart}" alt="Wykres wg miasta"/>

            <h3>1.2. Liczba poszkodowanych wg Województwa</h3>
            <img src="data:image/png;base64,{voiv_chart}" alt="Wykres wg województwa"/>

            <h3>1.3. Rozkład rodzajów needs</h3>
            <img src="data:image/png;base64,{needs_chart}" alt="Wykres needs"/>

            <hr/>

            <h2>2. Szczegółowa lista poszkodowanych</h2>
            <p>Poniżej pełna tabela z danymi z bazy:</p>
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
        html_content += f"""
                    <tr>
                        <td>{aff.id}</td>
                        <td>{aff.first_name}</td>
                        <td>{aff.last_name}</td>
                        <td>{aff.needs or ""}</td>
                        <td>{city}</td>
                        <td>{voiv}</td>
                    </tr>
        """

    html_content += """
                </tbody>
            </table>
            <hr/>
            <a href="/reports/ui" class="btn btn-secondary">Powrót do Reports UI</a>
        </div>
    </body>
    </html>
    """

    return html_content

