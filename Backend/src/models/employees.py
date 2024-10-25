from __init__ import db

class Employees(db.Model):
    __tablename__ = 'employees'

    staff_id = db.Column(db.Integer, primary_key=True)
    staff_fname = db.Column(db.String(100), nullable=False)
    staff_lname = db.Column(db.String(100), nullable=False)
    dept = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    reporting_manager = db.Column(db.Integer, nullable=True)
    role = db.Column(db.String(100), nullable=False)

    def __init__(self, staff_id, staff_fname, staff_lname, dept, position, country, email, reporting_manager, role):
        self.staff_id = staff_id
        self.staff_fname = staff_fname
        self.staff_lname = staff_lname
        self.dept = dept
        self.position = position
        self.country = country
        self.email = email
        self.reporting_manager = reporting_manager
        self.role = role

    def json(self):
        return {
            "staff_id": self.staff_id,
            "staff_fname": self.staff_fname,
            "staff_lname": self.staff_lname,
            "dept": self.dept,
            "position": self.position,
            "country": self.country,
            "email": self.email,
            "reporting_manager": self.reporting_manager,
            "role": self.role
        }