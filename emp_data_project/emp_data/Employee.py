#TODO create emp class, use payroll.py as a starting point

from sre_parse import State
from types import CoroutineType


class Employee:
    def __init__(self, emp_id, first_name, last_name, city, state, zip, pay_classification, ssn, start_date, bank_info, dob, access_codes, job_title, job_dept, email):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.city = city
        self.state = state
        self.zip = zip
        self.pay_classification = pay_classification
        self.ssn = ssn
        self.start_date = start_date
        self.bank_info = bank_info
        self.dob = dob
        self.access_codes = access_codes
        self.job_title = job_title
        self.job_dept = job_dept
        self.email = email

    def make_hourly(self):
        self.pay_classification = 'hourly'

    def make_salaried(self):
        self.pay_classification = 'salaried'

    def make_commissioned(self):
        self.pay_classification = 'commissioned'

    def issue_payment(self):
        pass

    def generate_pay_report(self):
        pass