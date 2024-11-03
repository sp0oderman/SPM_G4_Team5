from src.models.employees import Employees
from src.models.wfh_requests import WFH_Requests
from src.models.withdrawal_requests import Withdrawal_Requests

# Import all email notification functions
from src.utils.email_functions import *

class Withdrawal_Requests_Service:
    def __init__(self, db):
        self.db = db

        
