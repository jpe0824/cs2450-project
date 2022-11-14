import Database
import Employee
import Gui


def test_employee_info():
    newEmployee = Employee
    newEmployee.emp_id = "Jared"
    assert newEmployee.emp_id == "Jared"

def test_hours():
    newHourly = Employee.Hourly
    newHourly.add_timecard(10) 
    assert newHourly.issue_payment() == 10

def test_salary():
    newSalaried = Employee.Salaried
    newSalaried.salary = 40000.40
    assert newSalaried.issue_payment ==  40000.40
    assert newSalaried.issue_payment != 40000

def test_commissioned():
    newCommissioned = Employee.Commissioned
    newCommissioned.salary = 50000.50
    assert newCommissioned.salary == 50000.50
    assert newCommissioned.salary != 50000