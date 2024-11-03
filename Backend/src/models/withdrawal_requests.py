from __init__ import db

class Withdrawal_Requests(db.Model):
    __tablename__ = 'withdrawal_requests'

    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_id = db.Column(db.Integer, nullable=False)
    reporting_manager = db.Column(db.Integer, nullable=False)
    wfh_request_id = db.Column(db.Integer, nullable=False)
    request_datetime = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    remarks = db.Column(db.String(5000), nullable=False)
    reason_for_status = db.Column(db.String(5000), nullable=True)

    def __init__(self, staff_id, reporting_manager, wfh_request_id, request_datetime, status, remarks, reason_for_status):
        self.staff_id = staff_id
        self.reporting_manager = reporting_manager
        self.wfh_request_id = wfh_request_id
        self.request_datetime = request_datetime
        self.status = status
        self.remarks = remarks
        self.reason_for_status = reason_for_status

    def json(self):
        return {
                "request_id": self.request_id,
                "staff_id": self.staff_id,
                "reporting_manager": self.reporting_manager,
                "wfh_request_id": self.wfh_request_id,
                "request_datetime": self.request_datetime,
                "status": self.status,
                "remarks": self.remarks,
                "reason_for_status": self.reason_for_status
            }