'''
Project Name: Project 5, Payroll
Author: Jason Edman
Due Date: 11/12/21
Course: CS1410
'''

from abc import ABC
import os, os.path

employees = []

PAY_LOGFILE = 'payroll.txt'

def run_payroll():
    if os.path.exists(PAY_LOGFILE):
        os.remove(PAY_LOGFILE)
    for emp in employees:
        emp.issue_payment()

def load_employees():
    IN_FILE_NAME = "employees.csv"
    
    emp_file = open(IN_FILE_NAME, 'r')

    emp_file.readline()
    for line in emp_file:
        line_list = line.strip().split(",")
        employees.append(Employee(line_list[0],line_list[1],line_list[2],line_list[3],line_list[4],line_list[5],line_list[6],line_list[7],line_list[8],line_list[9],line_list[10]))
    
    return employees
    
def find_employee_by_id(emp_id):
    for employee in employees:
        if employee.emp_id == emp_id:
            return employee


def process_timecards():
    timecard_file = open("timecards.csv","r")
    for line in timecard_file:
        line = line.strip().split(',')
        emp_id = line[0]
        employee = find_employee_by_id(emp_id)
        for hours in line[1::]:
            if len(hours) > 0:
                employee.classification.add_timecard(float(hours))
    
def process_receipts():
    receipts_file = open("receipts.csv","r")
    for line in receipts_file:
        line = line.strip().split(",")
        emp_id = line[0]
        employee = find_employee_by_id(emp_id)
        for receipt in line[1::]:
            if len(receipt) > 0:
                employee.classification.add_receipt(float(receipt))

class Employee:
    def __init__(self,emp_id,first_name,last_name,address,city,state,zipcode,classification,salary,comm_rate,rate):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode

        if classification == '3':
            self.classification = Hourly(rate)
        elif classification == '1':
            self.classification = Salaried(salary)
        elif classification == '2':
            self.classification = Commissioned(salary,comm_rate)

    def make_hourly(self,rate):
        self.classification = Hourly(rate)

    def make_salaried(self,salary):
        self.classification = Salaried(salary)

    def make_commissioned(self,salary,comm_rate):
        self.classification = Commissioned(salary,comm_rate)

    def issue_payment(self):
        pay = self.classification.issue_payment()
        if pay > 0:
            FILE = open(PAY_LOGFILE,"a")
            FILE.write(f"Mailing {pay:.2f} to {self.first_name} {self.last_name} at {self.address} {self.city} {self.state} {self.zipcode}\n")
        else:
            pass
    
    def __repr__(self):
        return str(self.emp_id + " " + self.first_name)
    
    
class Classification(ABC):
    def issue_payment():
        pass

class Salaried(Classification):
    def __init__(self,salary):
        self.salary = float(salary)

    def issue_payment(self):
        pay = self.salary/24
        return float(pay)

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
        

class Commissioned(Classification):
    def __init__(self, salary, comm_rate):
        self.salary = float(salary)
        self.comm_rate = (float(comm_rate))/100
        self.receipts = []
    
    def add_receipt(self,amount):
        self.receipts.append(amount)

    def issue_payment(self):
        total_receipts = 0
        for receipt in self.receipts:
            total_receipts += receipt

        pay = (self.salary/24)+(self.comm_rate * total_receipts)
        self.receipts = []
        return float(pay)
