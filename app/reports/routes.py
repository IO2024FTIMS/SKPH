from flask import Blueprint, render_template, request, Response, jsonify
from .report_service import ReportService
from .report_generator import ReportGenerator

bp = Blueprint("reports", __name__, template_folder="/templates/reports", static_folder="static")

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
