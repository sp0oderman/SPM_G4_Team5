from src.__init__ import db

class User_Accounts(db.Model):
    __tablename__ = 'user_accounts'

    login_id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    last_login = db.Column(db.DateTime)
    role = db.Column(db.Integer, nullable=False)

    def __init__(self, login_id, staff_id, username, password_hash, last_login, role):
        self.login_id = login_id
        self.staff_id = staff_id
        self.username = username
        self.password_hash = password_hash
        self.last_login = last_login
        self.role = role

    def json(self):
        return {
                "login_id": self.login_id,
                "staff_id": self.staff_id,
                "username": self.username,
                "password_hash": self.password_hash,
                "last_login": self.last_login,
                "role": self.role
            }