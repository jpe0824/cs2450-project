

import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import askyesno
from tkinter import font  as tkfont

from example_database import *
from Employee import *
uvuEmpDat = EmployeeDB()


#test database will contain a key (employee id) with a value containing employee password and privileges. 
testDataBase = {
            '999999': ['password', 'admin'],
            '123456': ['password', 'employee'],
            '0': ['0', 'admin'],
            '1': ['1', 'employee']
            }

Emp = Employee(None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
Emp.emp_id = '1'
Emp.first_name = 'Matt'
Emp.last_name = 'Ackerman'
Emp.address = '123 bvld street'
Emp.city = 'Orem'
Emp.state = 'Utah'
Emp.zipcode = '84058'
Emp.classification = '1'
Emp.payment_method = '0'
Emp.ssn = '000-00-0000'
Emp.start_date = '11/19/2022'
Emp.end_date = 'NA'
Emp.bank_info = ''
Emp.dob = '04/12/2000'
Emp.permission = 'employee'
Emp.job_title = 'Water Boy'
Emp.job_dept = 'R&D'
Emp.phone = '123-456-5678'
Emp.email = 'emp123@gmail.com'
Emp.rate = 'rate'
Emp.salary = 'salary'
Emp.comm_rate = 'commission'
Emp.password = '1'
Emp.job_status = 'Active'



class EmpApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.edit_employee = False
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1, minsize = 600)
        container.grid_columnconfigure(0, weight=1, minsize = 1000)
        self.resizable(False, False)
        self.frames = {}
        for F in (LoginPage, home_page, employee_directory_page, add_employee_page):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("LoginPage")
    
    def logout(self):
        if self.edit_employee is True:
            answer = askyesno(title="Warning", message="You have unsaved information, are you sure you want to logout?")
            if not answer:
                return 
            
        self.show_frame("LoginPage")
    
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        
        if page_name != 'LoginPage':
            frame.logoutBtn = tk.Button(frame, text="Logout", command= self.logout)
            frame.logoutBtn.place(x=950,y=0)
        if page_name != 'LoginPage' and page_name != 'add_employee_page' and page_name != 'home_page':
            frame.home = tk.Button(frame, text="Home", command= lambda: self.show_frame("home_page"))
            frame.home.place(x=900,y=0)
        
        frame.tkraise()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#333333')
        self.controller = controller
        self.employee = None # when user logs in, self.employee will contain employee id for reference. 

        username = StringVar()
        password = StringVar()
        
        # LabelFrame makes container for widgets in order to center login screen within main window
        border = tk.LabelFrame(self, text='Login', bg='#333333', fg="#FF3399", font=("Arial Bold", 20))
        border.pack(fill="both", expand="yes", padx=150, pady=150)


                #creating widgets for login page
        self.login_label = tk.Label(border, text="Login", bg='#333333', fg="#FF3399", font=('Arial', 30))
        self.username_label = tk.Label(border, text="Username", bg='#333333', fg="#FFFFFF", font=('Arial', 16))
        self.username_entry = tk.Entry(border, font=('Arial', 16), textvariable=username)
        self.password_entry = tk.Entry(border, show='*', font=('Arial', 16), textvariable=password)
        self.password_label = tk.Label(border, text='Password', bg='#333333', fg="#FFFFFF", font=('Arial', 16))
        self.login_button = tk.Button(border, text='Login', bg='#FF3399', fg='#FFFFFF', command=self.validateLogin)
    
        # Positioning widgets on the screen
        self.username_label.place(x=50, y=20)
        self.username_entry.place(x=180, y=20)
        self.password_label.place(x=50, y=80)
        self.password_entry.place(x=180, y=80)
        self.login_button.place(x=250, y=125)
        

    def validateLogin(self):

        if self.username_entry.get() in testDataBase:
           if self.password_entry.get() == testDataBase[self.username_entry.get()][0]:
                #initialize username and password entry for when user logs out
                self.employee = self.username_entry.get()
                self.username_entry.delete(0, END)
                self.password_entry.delete(0, END)
                #----------------------------------------------------
                self.focus() #removes focus on data fields
                
                if testDataBase[self.employee][1] != 'admin':                      
                    self.controller.frames['home_page'].addEmpBtn.pack_forget()       # removes 'Add Employee Button' when user doesn't have admin privileges. 
                elif testDataBase[self.employee][1] == 'admin':
                    self.controller.frames['home_page'].addEmpBtn.pack()        # relitialize home page to include 'Add Employee Button' when user has admin privilege.
                self.controller.show_frame("home_page")                  # calls show_frame from class EmpApp to change the frame to home_page
           else:
               self.password_entry.delete(0, END)                            
               messagebox.showerror("Invalid","invalid password")

        else: 
            self.password_entry.delete(0, END)
            messagebox.showerror("Invalid","invalid username and password")


class home_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self._state = 'disabled'
        label = tk.Label(self, text="Home Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        def add_emp():
            pass
        
            
        def save_edit_emp():
            self.controller.frames['home_page'].saveBtn.pack_forget()
            self.controller.frames['home_page'].cancelBtn.pack_forget()
            self.controller.frames['home_page'].editEmp.pack()
            self.controller.edit_employee = False 
            parse_entry('disabled')
        
        def cancel_edit_emp():
            self.controller.frames['home_page'].saveBtn.pack_forget()
            self.controller.frames['home_page'].cancelBtn.pack_forget()
            self.controller.frames['home_page'].editEmp.pack()
            self.controller.edit_employee = False  
            parse_entry('disabled')

        def edit_emp():
            # self.controller.frames['home_page']._state = 'normal'
            self.controller.edit_employee = True
            self.controller.frames['home_page'].saveBtn.pack()
            self.controller.frames['home_page'].cancelBtn.pack()
            self.controller.frames['home_page'].editEmp.pack_forget()
            parse_entry('normal')
            
          
        def parse_entry(state):
            for widget in self.controller.frames['home_page'].view_frame.winfo_children():  # will parse through all widgets in home page frame
                if widget.winfo_class() == 'Entry':
                    widget['state'] = state
            self.controller.show_frame("home_page")
            
            
            
                
            
        self.addEmpBtn = tk.Button(self, text="Add New Employee",
                               command= add_emp)
        self.addEmpBtn.pack(side='left')
        
        self.editEmp = tk.Button(self, text='Edit Employee', command= edit_emp)
        self.editEmp.pack(side='left')
        
        self.saveBtn = tk.Button(self, text='Save', command=save_edit_emp)
        
        self.cancelBtn = tk.Button(self, text='Cancel', command=cancel_edit_emp)
        
        self.view_frame = LabelFrame(self, border=True) ################################# !!! REMINDER !!! -> Remove border when done formatting
        self.view_frame.pack(fill='x')

        # self.edit_employee = tk.Button(self.view_frame, text="Employee Directory",
        #                        command= lambda: controller.show_frame("employee_directory_page"))
        # self.employeeDirBtn.grid(column=0)
        
        var = StringVar()
        var.set('None')
        emp_id = StringVar()
        emp_id.set(Emp.emp_id)
        first_name = StringVar()
        first_name.set(Emp.first_name)
        last_name = StringVar()
        last_name.set(Emp.last_name)
        address = StringVar()
        address.set(Emp.address)
        city = StringVar()
        city.set(Emp.city)
        state = StringVar()
        state.set(Emp.state)
        zipcode = StringVar()
        zipcode.set(Emp.zipcode)
        classification = StringVar()
        classification.set(Emp.classification)
        payment_method = StringVar()
        payment_method.set(Emp.payment_method)
        ssn = StringVar()
        ssn.set(Emp.ssn)
        start_date = StringVar()
        start_date.set(Emp.start_date)
        end_date = StringVar()
        end_date.set(Emp.end_date)
        bank_info = StringVar()
        bank_info.set(Emp.bank_info)
        dob = StringVar()
        dob.set(Emp.dob)
        permission = StringVar()
        permission.set(Emp.permission)
        job_title = StringVar()
        job_title.set(Emp.job_title)
        job_dept = StringVar()
        job_dept.set(Emp.job_dept)
        phone = StringVar()
        phone.set(Emp.phone)
        email = StringVar()
        email.set(Emp.email)
        rate = StringVar()
        rate.set(Emp.rate)
        salary = StringVar()
        salary.set(Emp.salary)
        comm_rate = StringVar()
        comm_rate.set(Emp.comm_rate)
        password = StringVar()
        password.set(Emp.password)
        job_status = StringVar()
        job_status.set(Emp.job_status)

        
        self.emp_ID_label = tk.Label(self.view_frame, justify='right', text="Employee ID:", font=('Arial', 10))
        self.emp_ID_entry = tk.Entry(self.view_frame, font=('Arial', 10), state=self._state, textvariable=emp_id)
        self.first_name_label = tk.Label(self.view_frame, justify='right', text="First Name:", font=('Arial', 10))
        self.first_name_entry = tk.Entry(self.view_frame, font=('Arial', 10), state=self._state, textvariable=first_name)
        self.last_name_label = tk.Label(self.view_frame, justify='right', text="Last Name:", font=('Arial', 10))
        self.last_name_entry = tk.Entry(self.view_frame, font=('Arial', 10), state=self._state, textvariable=last_name)
        self.address_label = tk.Label(self.view_frame, justify='right', text="Address:", font=('Arial', 10))
        self.address_entry = tk.Entry(self.view_frame, font=('Arial', 10), state=self._state, textvariable=address)
        self.city_label = tk.Label(self.view_frame, justify='right', text="City:", font=('Arial', 10))
        self.city_entry = tk.Entry(self.view_frame, font=('Arial', 10), state=self._state, textvariable=city)
        self.state_label = tk.Label(self.view_frame, justify='right', text="State:", font=('Arial', 10))
        self.state_entry = tk.Entry(self.view_frame, font=('Arial', 10), state=self._state, textvariable=state)
        self.zip_label = tk.Label(self.view_frame, justify='right', text="Zip:", font=('Arial', 10))
        self.zip_entry = tk.Entry(self.view_frame, font=('Arial', 10), state=self._state, textvariable=zipcode)
        
        self.classification_label = tk.Label(self.view_frame, justify='right', text="Classification:", font=('Arial', 10))
        
        clicked = StringVar()
        classificationList = ['Salaried', 'Commission', 'Hourly']
        clicked.set(classificationList[int(Emp.classification)])
        self.classification_dropdown = OptionMenu(self.view_frame, clicked, "- Select -", "Salaried", "Commission", "Hourly")
        self.classification_dropdown.configure(state=self._state)
        
        self.office_phone_label = tk.Label(self.view_frame, justify='right', text="Office Phone:", font=('Arial', 10))
        self.office_phone_entry = tk.Entry(self.view_frame, font=('Arial', 10), state=self._state, textvariable=phone)
        self.office_email_label = tk.Label(self.view_frame, justify='right', text="Office Email:", font=('Arial', 10))
        self.office_email_entry = tk.Entry(self.view_frame, font=('Arial', 10), state=self._state, textvariable=email)
        self.personal_phone_label = tk.Label(self.view_frame, justify='right', text="Personal Phone:", font=('Arial', 10))
        self.personal_phone_entry = tk.Entry(self.view_frame, font=('Arial', 10), state=self._state, textvariable=phone)
        self.personal_email_label = tk.Label(self.view_frame, justify='right', text="Personal Email:", font=('Arial', 10))
        self.personal_email_entry = tk.Entry(self.view_frame, font=('Arial', 10), state=self._state, textvariable=email)
        self.DOB_label = tk.Label(self.view_frame, justify='right', text="Date of Birth:", font=('Arial', 10))
        self.DOB_entry = tk.Entry(self.view_frame, font=('Arial', 10), state=self._state, textvariable=dob)
        
        self.SSN_label = tk.Label(self.view_frame, justify='right', text="SSN:", font=('Arial', 10))
        self.SSN_entry = tk.Entry(self.view_frame, font=('Arial', 10), state=self._state, textvariable=ssn)
        self.routing_number_label = tk.Label(self.view_frame, justify='right', text="Routing Number:", font=('Arial', 10))
        self.routing_number_entry = tk.Entry(self.view_frame, font=('Arial', 10), state=self._state, textvariable=var)
        self.account_number_label = tk.Label(self.view_frame, justify='right', text="Account Number:", font=('Arial', 10))
        self.account_number_entry = tk.Entry(self.view_frame, font=('Arial', 10), state=self._state, textvariable=var)
        self.payment_method_label = tk.Label(self.view_frame, justify='right', text="Payment Method:", font=('Arial', 10))
        
        payment_method_clicked = StringVar()
        payment_methodList = ['Direct Deposit', 'Mail']
        payment_method_clicked.set(payment_methodList[int(Emp.payment_method)])
        self.payment_method_dropdown = OptionMenu(self.view_frame, payment_method_clicked, "- Select -", "Direct Deposit", "Mail")
        self.payment_method_dropdown.configure(state=self._state)
        
        self.permission_level_label = tk.Label(self.view_frame, justify='right', text="Permission Level:", font=('Arial', 10))
        self.permission_level_entry = tk.Entry(self.view_frame, font=('Arial', 10), state=self._state, textvariable=permission)
        self.job_title_label = tk.Label(self.view_frame, justify='right', text="Job Title:", font=('Arial', 10))
        self.job_title_entry = tk.Entry(self.view_frame, font=('Arial', 10), state=self._state, textvariable=job_title)
        self.job_department_label = tk.Label(self.view_frame, justify='right', text="Department:", font=('Arial', 10))
        self.job_department_entry = tk.Entry(self.view_frame, font=('Arial', 10), state=self._state, textvariable=job_dept)
        self.start_date_label = tk.Label(self.view_frame, justify='right', text="Start Date:", font=('Arial', 10))
        self.start_date_entry = tk.Entry(self.view_frame, font=('Arial', 10), state=self._state, textvariable=start_date)
        self.end_date_label = tk.Label(self.view_frame, justify='right', text="End Date:", font=('Arial', 10))
        self.end_date_entry = tk.Entry(self.view_frame, font=('Arial', 10), state=self._state, textvariable=end_date)
        self.employment_status_label = tk.Label(self.view_frame, justify='right', text="Employment Status:", font=('Arial', 10))
        self.employment_status_entry = tk.Entry(self.view_frame, font=('Arial', 10), state=self._state, textvariable=job_status)
        self.password_label = tk.Label(self.view_frame, justify='right', text="Password", font=('Arial', 10))
        self.password_entry = tk.Entry(self.view_frame, font=('Arial', 10), state=self._state, textvariable=password)
        
        self.emp_ID_label.grid(column=1, row=1, sticky='E', padx=15, pady=7)
        self.first_name_label.grid(column=1, row=2, sticky='E', padx=15, pady=7)
        self.last_name_label.grid(column=1, row=3, sticky='E', padx=15, pady=7)
        self.address_label.grid(column=1, row=4, sticky='E', padx=15, pady=7)
        self.city_label.grid(column=1, row=5, sticky='E', padx=15, pady=7)
        self.state_label.grid(column=1, row=6, sticky='E', padx=15, pady=7)
        self.zip_label.grid(column=1, row=7, sticky='E', padx=15, pady=7)
        self.classification_label.grid(column=1, row=8, sticky='E', padx=15, pady=7)
        self.office_phone_label.grid(column=1, row=9, sticky='E', padx=15, pady=7)
        self.office_email_label.grid(column=1, row=10, sticky='E', padx=15, pady=7)
        self.personal_phone_label.grid(column=1, row=11, sticky='E', padx=15, pady=7)
        self.personal_email_label.grid(column=1, row=12, sticky='E', padx=15, pady=7)
        
        self.DOB_label.grid(column=3, row=1, sticky='E', padx=15, pady=7)
        self.SSN_label.grid(column=3, row=2, sticky='E', padx=15, pady=7)
        self.routing_number_label.grid(column=3, row=3, sticky='E', padx=15, pady=7)
        self.account_number_label.grid(column=3, row=4, sticky='E', padx=15, pady=7)
        self.payment_method_label.grid(column=3, row=5, sticky='E', padx=15, pady=7)
        self.permission_level_label.grid(column=3, row=6, sticky='E', padx=15, pady=7)
        self.job_title_label.grid(column=3, row=7, sticky='E', padx=15, pady=7)
        self.job_department_label.grid(column=3, row=8, sticky='E', padx=15, pady=7)
        self.start_date_label.grid(column=3, row=9, sticky='E', padx=15, pady=7)
        self.end_date_label.grid(column=3, row=10, sticky='E', padx=15, pady=7)
        self.employment_status_label.grid(column=3, row=11, sticky='E', padx=15, pady=7)
        self.password_label.grid(column=3, row=12, sticky='E', padx=15, pady=7)
        
        self.emp_ID_entry.grid(column=2 , row=1)
        self.first_name_entry.grid(column=2 , row=2)
        self.last_name_entry.grid(column=2 , row=3)
        self.address_entry.grid(column=2 , row=4)
        self.city_entry.grid(column=2 , row=5)
        self.state_entry.grid(column=2 , row=6)
        self.zip_entry.grid(column=2 , row=7)
        self.classification_dropdown.grid(column=2 , row=8)
        self.office_phone_entry.grid(column=2 , row=9)
        self.office_email_entry.grid(column=2 , row=10)
        self.personal_phone_entry.grid(column=2 , row=11)
        self.personal_email_entry.grid(column=2 , row=12)
    
        self.DOB_entry.grid(column=4 , row=1)
        self.SSN_entry.grid(column=4 , row=2)
        self.routing_number_entry.grid(column=4 , row=3)
        self.account_number_entry.grid(column=4 , row=4)
        self.payment_method_dropdown.grid(column=4 , row=5)
        self.permission_level_entry.grid(column=4 , row=6)
        self.job_title_entry.grid(column=4 , row=7)
        self.job_department_entry.grid(column=4 , row=8)
        self.start_date_entry.grid(column=4 , row=9)
        self.end_date_entry.grid(column=4 , row=10)
        self.employment_status_entry.grid(column=4 , row=11)
        self.password_entry.grid(column=4 , row=12)


class employee_directory_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Employee Directory Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)


class add_employee_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="New Employee", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)        
        self.sumbitBnt = tk.Button(self, text="Submit")
        self.sumbitBnt.pack()


