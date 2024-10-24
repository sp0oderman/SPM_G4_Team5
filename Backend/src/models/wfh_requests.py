from src.__init__ import db

class WFH_Requests(db.Model):
    __tablename__ = 'wfh_requests'

    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_id = db.Column(db.Integer)
    reporting_manager = db.Column(db.Integer, nullable=False)
    dept = db.Column(db.String(50), nullable=False)
    chosen_date = db.Column(db.String(50), nullable=False)
    arrangement_type = db.Column(db.String(20), nullable=False)
    request_datetime = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    remarks = db.Column(db.String(500), nullable=True)

    def __init__(self, staff_id, reporting_manager, dept, chosen_date, arrangement_type, request_datetime, status, remarks):
        self.staff_id = staff_id
        self.reporting_manager = reporting_manager
        self.dept = dept
        self.chosen_date = chosen_date
        self.arrangement_type = arrangement_type
        self.request_datetime = request_datetime
        self.status = status
        self.remarks = remarks

    def json(self):
        return {
                "request_id": self.request_id,
                "staff_id": self.staff_id,
                "reporting_manager": self.reporting_manager,
                "dept": self.dept,
                "chosen_date": self.chosen_date,
                "chosen_date": self.chosen_date,
                "arrangement_type": self.arrangement_type,
                "request_datetime": self.request_datetime,
                "status": self.status,
                "remarks": self.remarks,
            }