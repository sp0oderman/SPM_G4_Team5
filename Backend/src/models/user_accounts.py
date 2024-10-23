from src.__init__ import db

class User_Accounts(db.Model):
    __tablename__ = 'user_accounts'

    login_id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    last_login = db.Column(db.DateTime)
    role = db.Column(db.Integer, nullable=False)