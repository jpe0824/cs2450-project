#TODO outline database class, attr, methods
# Questions for meeting:
# how to save between runs
import Employee
class Fake_employee:
    def __init__(self, username, password, ID):
        self.username = username
        self.password = password
        self.ID = ID

        
class Database:
    def __init__(self):
        self.cur_emp = ''
        self.USERNAME_INDEX = 0
        self.PASSWORD_INDEX = 1
        self.EMPLOYEE_TYPE_INDEX = 2
        self.ID_NUMBER_INDEX = 3
        


    def load_user_data(self, username, password):
        ''' Brings up the user's data after checking username, password, and deactivated accounts '''



        # Get file where data is stored
        IN_FILE_NAME = "emp_data_project/emp_data/test.csv"
        emp_file = open(IN_FILE_NAME, 'r')

        # Read data into memory
        employee_data = emp_file.readlines()
        emp_file.close()
        # Check each employee in database
        for line in employee_data:
            
            # remove newline characters
            line = line.replace('\n','')

            # give each employee a list with their data
            cur_emp = (line.split(','))

            if username == cur_emp[self.USERNAME_INDEX] and password == cur_emp[self.PASSWORD_INDEX]:
                if cur_emp[self.EMPLOYEE_TYPE_INDEX] == '2':
                    # employee has been deactivated and has no access
                    print("user found but account has been deactivated")
                    return False
            
                # user has been found and is granted access: create employee object
                user = Fake_employee(cur_emp[self.USERNAME_INDEX],cur_emp[self.PASSWORD_INDEX],cur_emp[self.ID_NUMBER_INDEX])
                print("User found and given access")

                # set current user and return the user as an employee object
                self.cur_emp = user
                return user

        # user wasnt in database, return false
        print('user not found')
        return False

    def create_emp(self, data_list):
        # TODO check to make sure username is origional
        '''
        # takes a list of employee's data and saves it to the CSV
        # used to create new employees
        # Employee is given an ID so no need to pass it in
        '''
        # open file
        IN_FILE_NAME = "emp_data_project/emp_data/test.csv"
        emp_file = open(IN_FILE_NAME, 'a+')

        # move to begining of file and count all the lines
        emp_file.seek(0)
        ID_number = len(emp_file.readlines()) + 1

        # write all the data on the next line
        emp_file.write('\n')

        for data in data_list:
            emp_file.write(str(data))
            emp_file.write(',')
        
        # add the ID to the last spot on the line
        emp_file.write(str(ID_number))

        emp_file.close()
        print('saved employee')


    def deactivate_emp(self, emp_ID):
        # revokes access and changes status to deactive
        IN_FILE_NAME = "emp_data_project/emp_data/test.csv"
        emp_file = open(IN_FILE_NAME, 'r')

        # move to begining of file and load all data into memory
        emp_file.seek(0)
        data = emp_file.readlines()
        print(data[0])

        # create a list of specific data points for employee
        test = data[emp_ID - 1].split(',')
        test[self.EMPLOYEE_TYPE_INDEX] = 2

        # generate new string with updated deactive indicator
        my_string = ''
        i = 0
        while i < len(test):
            my_string += str(test[i])
            if i < len(test) - 1:
                my_string += ','
            i += 1
        
        # replace old data with new data in list
        data[emp_ID - 1] = my_string

        emp_file.close()

        # write the data to the file
        emp_file = open(IN_FILE_NAME, 'w')
        for line in data:
            emp_file.write(line)

    def update_emp(self):
        # Allows for changing of employee information by those with admin permissions
        pass

    def update_self(self):
        # Allows changing of personal information for those without admin permissions
        pass

    def report_database(self):
        # Produces report of information within the database for the user to view
        pass

    def validate_form(self):
        # This formula verifies whether the specified file concerning the data entered is correct and valid according to data constraints
        pass



def test_methods():
    my_database = Database()
    mylyst = ['username3','password3',0]

    #my_database.load_user_data('username1','password1')
    #my_database.create_emp(mylyst)
    my_database.deactivate_emp(1)
test_methods()