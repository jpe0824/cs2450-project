#TODO create emp class, use payroll.py as a starting point

from sre_parse import State
from types import CoroutineType


class Employee:
    def __init__(self, emp_id, first_name, last_name, city, state, zipcode, classification, ssn, start_date, bank_info, dob, access_codes, job_title, job_dept, email):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.classification = classification
        self.ssn = ssn
        self.start_date = start_date
        self.bank_info = bank_info
        self.dob = dob
        self.access_codes = access_codes
        self.job_title = job_title
        self.job_dept = job_dept
        self.email = email

        if classification == '3':
            self.classification = Hourly(rate)
        elif classification == '1':
            self.classification = Salaried(salary)
        '''elif classification == '2':
            self.classification = Commissioned(salary,comm_rate)''' # Add comm_rate to employee

    def make_hourly(self,rate):
        self.pay_classification = Hourly(rate)

    def make_salaried(self):
        self.pay_classification = Salaried(salary)

    '''def make_commissioned(self):
        self.pay_classification = Commissioned(salary,comm_rate'''

    def issue_payment(self):
        pass

    def generate_pay_report(self):
        pass

class Hourly(Classification):
    def __init__(self,hourly_rate):
        self.hourly_rate = float(hourly_rate)
        self.hours_worked = []
    
    def add_timecard(self, hours):
        self.hours_worked.append(hours)

    def issue_payment(self):
        total_hours = 0
        for hour in self.hours_worked:
            total_hours += hour
        pay = total_hours * self.hourly_rate
        self.hours_worked = []
        return float(pay)