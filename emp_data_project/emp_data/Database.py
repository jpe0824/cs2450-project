#TODO outline database class, attr, methods
# Questions for meeting:
# how to save between runs
import Employee
class Fake_employee:
    def __init__(self):
        self.employees = [[]]
        self.cur_emp = ''
        
class Database:
    def __init__(self):
        self.employees = [[]]
        self.cur_emp = ''

    def load_employees(self):
        IN_FILE_NAME = "emp_data_project/emp_data/test.csv"
        
        emp_file = open(IN_FILE_NAME, 'r')
        test_emp = Employee()
        emp_file.readline()
        for line in emp_file:
            line_list = line.strip().split(",")

            self.employees.append(Employee(line_list[0],line_list[1],line_list[2],line_list[3],line_list[4],line_list[5],line_list[6],line_list[7],line_list[8]\
                ,line_list[9],line_list[10],line_list[11],line_list[12],line_list[13],line_list[14],line_list[15],line_list[16],line_list[17]))

        print(self.employees)

    def build_database():
        # creates a database that is based on employee IDs like so:
        '''
        [[1],[2],[3],[4],[5],[6],[7],[8],[9]
        [10],[11],[12],[13],[14],[15],[16],[17],[18],[19]
        ...
        ...
        ...
        [91],[92],[93],[94],[95],[96],[97],[98],[99]]
        '''
        # to find and insert data:
        '''
        if ID_number < 10:
            row = 0
            col = ID_number - 1

        else:
            col = (ID_number % 10) - 1
            row = (ID_number // 10) - 1
        '''

        pass
    def load_emp(self, cur_emp=''):
        # Brings up Employee and info concerning said employee
        pass

    def save_emp(self, cur_emp):
        # Saves data of employee into employee database
        pass

    def create_emp(self):
        # Allows creation of new employee data to add
        pass

    def deactivate_emp(self, cur_emp):
        # Removes employee from database in files
        # Flag ID so that new employees can use it
        pass

    def update_emp(self):
        # Allows for changing of employee information by those with admin permissions
        pass

    def update_self(self):
        # Allows changing of personal information for those without admin permissions
        pass

    def merge_database(self):
        # This method combines the data of separate files to form new database file for system
        pass

    def report_database(self):
        # Produces report of information within the database for the user to view
        pass

    def validate_form(self):
        # This formula verifies whether the specified file concerning the data entered is correct and valid according to data constraints
        pass

    def import_database(self):
        # Permits transfer of data from separate file for system
        pass

    def store_database(self):
        #saves the database as txt before closing
        pass

my_database = Database()
