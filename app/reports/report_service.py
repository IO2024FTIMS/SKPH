import csv
import os
from datetime import datetime

class ResourceReport:
    def __init__(self, report_id, created_at, entries):
        self.report_id = report_id
        self.created_at = created_at
        self.entries = entries

    def to_dict(self):
        return {
            "report_id": self.report_id,
            "created_at": self.created_at.isoformat(),
            "entries": self.entries
        }

class ReportService:
    def __init__(self):
        self.data_file = os.path.join(os.path.dirname(__file__), 'reports_data.csv')
        self._reports = []
        self._next_id = 1

    def generate_report(self):
        # Wczytaj dane z CSV i utwórz nowy raport
        entries = []
        with open(self.data_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                entries.append({
                    "resource_name": row['resource_name'],
                    "quantity": int(row['quantity']),
                    "location": row['location']
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
        for r in self._reports:
            if r.report_id == report_id:
                return r
        return None
