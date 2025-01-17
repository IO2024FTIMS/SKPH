from datetime import datetime
from collections import Counter

from app.extensions import db
from app.models.affected import Affected
from app.models import ResourceReport
from app.models.request import Request
from app.models.request import RequestStatus

class ReportService:
    def __init__(self):
        self._reports = []
        self._next_id = 1

    def generate_report(self):

        affected_list = db.session.query(Affected).all()

        needs_counter = Counter()
        for aff in affected_list:
            if aff.needs:
                needs_counter[aff.needs] += 1
            else:
                needs_counter["(no needs)"] += 1

        entries = []
        for need_value, count in needs_counter.items():
            entries.append({
                "resource_name": need_value,
                "quantity": count,
                "location": "N/A"
            })

        new_report = ResourceReport(
            report_id=self._next_id,
            created_at=datetime.now(),
            entries=entries
        )

        self._reports.append(new_report)
        self._next_id += 1

        return new_report

    def get_all_reports(self):
        return self._reports

    def get_report_by_id(self, report_id):
        for rep in self._reports:
            if rep.report_id == report_id:
                return rep
        return None

    def stats_by_city(self):
        data = {}
        affected_list = db.session.query(Affected).all()
        for aff in affected_list:
            city = aff.address.city if aff.address else "Brak"
            data[city] = data.get(city, 0) + 1
        return data

    def stats_by_voivodeship(self):
        data = {}
        affected_list = db.session.query(Affected).all()
        for aff in affected_list:
            voiv = aff.address.voivodeship if aff.address else "Brak"
            data[voiv] = data.get(voiv, 0) + 1
        return data

    def stats_by_needs(self):
        data = {}
        affected_list = db.session.query(Affected).all()
        for aff in affected_list:
            n = aff.needs if aff.needs else "Brak"
            data[n] = data.get(n, 0) + 1
        return data

    def stats_request_by_status(self):
        data = {}
        requests_list = db.session.query(Request).all()
        for req in requests_list:
            # req.status jest RequestStatus, np. RequestStatus.PENDING
            status_str = req.status.value  # 'Pending', 'Approved', ...
            data[status_str] = data.get(status_str, 0) + 1
        return data

    def stats_request_by_needs(self):
        data = {}
        requests_list = db.session.query(Request).all()
        for req in requests_list:
            n = req.needs if req.needs else "No needs"
            data[n] = data.get(n, 0) + 1
        return data


