import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import askyesno
from tkinter import font  as tkfont
from tkinter import ttk

# from example_database import *
from Database import *
EmpDat = EmployeeDB()



class EmpApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.edit_employee = False
        self.employee = None
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1, minsize = 600)
        container.grid_columnconfigure(0, weight=1, minsize = 1100)
        self.resizable(False, False)
        self.frames = {}
        for F in (LoginPage, emp_page, admin_page, add_employee_page):
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
        self.edit_employee = False
        self.frames['emp_page'].editEmp.grid(column=0, row=1)
        self.frames['emp_page'].saveBtn.grid_forget()
        self.frames['emp_page'].cancelBtn.grid_forget()
        self.show_frame("LoginPage")
    
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        
        if page_name != 'LoginPage':
            frame.logoutBtn = tk.Button(frame, text="Logout", command= lambda: self.logout())
            frame.logoutBtn.place(x=1050,y=0)
        # if page_name != 'LoginPage' and page_name != 'add_employee_page' and page_name != 'emp_page':
        #     frame.home = tk.Button(frame, text="Home", command= lambda: self.show_frame("emp_page"))
        #     frame.home.place(x=900,y=0)
        frame.tkraise()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#333333')
        self.controller = controller

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
        self.login_button = tk.Button(border, text='Login', bg='#FF3399', fg='#FFFFFF', command= lambda: self.validateLogin(self.username_entry.get(), self.password_entry.get()))
    
        # Positioning widgets on the screen
        self.username_label.place(x=50, y=20)
        self.username_entry.place(x=180, y=20)
        self.password_label.place(x=50, y=80)
        self.password_entry.place(x=180, y=80)
        self.login_button.place(x=250, y=125)
        

    def validateLogin(self, username, password):
        valid_username = False
        valid_password = False
        for employee in EmpDat.emp_list:
            if employee.id == int(username):
                valid_username = True
                if employee.password == password:
                    valid_password = True
                    self.controller.employee = employee
                    break

        if valid_username and valid_password:
            self.controller.user = employee
            #initialize username and password entry for when user logs out
            self.username_entry.delete(0, END)
            self.password_entry.delete(0, END)
            #----------------------------------------------------
            self.focus() #removes focus on data fields
            
            if self.controller.employee.permission == 'employee':
                self.controller.frames['emp_page'].emp_page_entries(employee, 'employee')
                self.controller.show_frame("emp_page")               # calls show_frame from class EmpApp to change the frame to emp_page
            elif self.controller.employee.permission == 'admin':
                self.controller.show_frame("admin_page")          # relitialize home page to include 'Add Employee Button' when user has admin privilege.
            
            
        elif valid_username and not valid_password:
            self.password_entry.delete(0, END)                            
            messagebox.showerror("Invalid","invalid password")

        else: 
            self.password_entry.delete(0, END)
            messagebox.showerror("Invalid","invalid username and password")


class emp_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.employee_id = None
        label = tk.Label(self, text="Home Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        self.view_frame = LabelFrame(self, border=True) ################################# !!! REMINDER !!! -> Remove border when done formatting
        self.view_frame.pack(fill='x')
        
        self.editEmp = tk.Button(self.view_frame, text='Edit Employee', command=lambda: self.edit_emp())
        self.editEmp.grid(column=0,row=1)
        
        self.saveBtn = tk.Button(self.view_frame, text='Save', command=lambda: self.save_edit_emp())
        
        self.cancelBtn = tk.Button(self.view_frame, text='Cancel', command=lambda: self.cancel_edit_emp())
        
    def add_emp(self):
        pass
    
        
    def save_edit_emp(self):
        self.controller.edit_employee = False 
        self.controller.frames['emp_page'].saveBtn.grid_forget()
        self.controller.frames['emp_page'].cancelBtn.grid_forget()
        self.controller.frames['emp_page'].editEmp.grid(column=0, row=1)
        self.parse_entry('save','none')
        self.parse_entry('parse', 'disabled')
    
    def cancel_edit_emp(self):
        self.controller.edit_employee = False  
        self.controller.frames['emp_page'].saveBtn.grid_forget()
        self.controller.frames['emp_page'].cancelBtn.grid_forget()
        self.controller.frames['emp_page'].editEmp.grid(column=0, row=1)
        self.parse_entry('cancel', 'disabled')

    def edit_emp(self):
        self.controller.edit_employee = True
        self.controller.frames['emp_page'].editEmp.grid_forget()
        self.controller.frames['emp_page'].saveBtn.grid(column=0, row=1)
        self.controller.frames['emp_page'].cancelBtn.grid(column=0, row=2)
        self.parse_entry('parse', 'normal')
        
        
        
    def parse_entry(self, mode, state):
        if mode == 'save':
            entryDict = {
                    'ID': self.emp_ID_entry.get(),
                    'Address': self.address_entry.get(),
                    'Name': " ".join([self.first_name_entry.get(), self.last_name_entry.get()]),
                    'City': self.city_entry.get(),
                    'State': self.state_entry.get(),
                    'Zip': self.zip_entry.get(),
                    'Phone': self.personal_phone_entry.get(),
                    'Email': self.personal_email_entry.get(),
                    'Birth_Date': self.DOB_entry.get(),
                    'SSN': self.SSN_entry.get(),
                    'Start_Date': self.start_date_entry.get(),
                    'End_Date': self.end_date_entry.get(),
                    'Title': self.job_title_entry.get(),
                    'Dept': self.job_department_entry.get(),
                    'Permission': self.permission_level_clicked.get(),
                    'Password': self.password_entry.get(),
                }
            if self.classification_clicked.get() == 'hourly':
                entryDict['Classification'] = '1'
            elif self.classification_clicked.get() == 'salary':
                entryDict['Classification'] = '2'
            elif self.classification_clicked.get() == 'commissioned':
                entryDict['Classification'] = '3'
            if self.payment_method_clicked.get() == 'direct deposit':
                entryDict['Pay_Method'] = '1'
            elif self.payment_method_clicked.get() == 'mail':
                entryDict['Pay_Method'] = '2'
            
            # if self.priviledge == 'admin':
            #     EmpDat.edit_employee(self.controller.employee.id, list(entryDict.keys()), list(entryDict.values())) 
            # elif self.priviledge == 'employee':
            #     entryDict = {
            #         'Address': self.address_entry.get(),
            #         'City': self.city_entry.get(),
            #         'State': self.state_entry.get(),
            #         'Zip': self.zip_entry.get(),
            #         'Phone': self.personal_phone_entry.get(),
            #         'Email': self.personal_email_entry.get()
            #     }
            
            
            
            EmpDat.edit_employee(self.employee_id, list(entryDict.keys()), list(entryDict.values()))
            # self.parse_entry('parse', 'disabled')
            
            
         
        elif mode == 'parse':
            for x in self.controller.frames['emp_page'].view_frame.children:  # will parse through all widgets --acts like event handler that updates window when there are changes
                if self.controller.user.permission == 'admin':
                    if (('entry') in x or self.view_frame.children[x].widgetName ==  "tk_optionMenu") and (x not in 'emp_id_entry' and x not in 'employment_status_entry'):
                        self.controller.frames['emp_page'].view_frame.children[x]['state'] = state
                elif self.controller.user.permission == 'employee':
                    if x in ('personal_phone_entry', 'personal_email_entry', 'address_entry', 'city_entry', 'state_entry', 'zip_entry', 'state_entry'):
                        self.controller.frames['emp_page'].view_frame.children[x]['state'] = state        
            self.controller.show_frame("emp_page")
            
        elif mode == 'cancel':
            self.emp_page_entries(self.employee_selected, 'cancel')
            self.classification_clicked.set(str(self.employee_selected.classification))
            self.payment_method_clicked.set(str(self.employee_selected.pay_method))
            self.permission_level_clicked.set(self.employee_selected.permission)
            
    def emp_page_entries(self, employee, mode = None):
        self.employee_selected = employee
        
        var = StringVar()
        var.set('None')
        emp_id = StringVar()
        emp_id.set(employee.id)
        first_name = StringVar()
        first_name.set(employee.first_name)
        last_name = StringVar()
        last_name.set(employee.last_name)
        address = StringVar()
        address.set(employee.address)
        city = StringVar()
        city.set(employee.city)
        state = StringVar()
        state.set(employee.state)
        zipcode = StringVar()
        zipcode.set(employee.zip)
        classification = StringVar()
        classification.set(str(employee.classification))
        payment_method = StringVar()
        payment_method.set(str(employee.pay_method))
        ssn = StringVar()
        ssn.set(employee.ssn)
        start_date = StringVar()
        start_date.set(employee.start_date)
        end_date = StringVar()
        end_date.set(employee.end_date)
        dob = StringVar()
        dob.set(employee.birth_date)
        job_title = StringVar()
        job_title.set(employee.title)
        job_dept = StringVar()
        job_dept.set(employee.dept)
        phone = StringVar()
        phone.set(employee.phone)
        email = StringVar()
        email.set(employee.email) 
        password = StringVar()
        password.set(employee.password)
        job_status = StringVar()
        job_status.set(employee.job_status)
        routingNum = StringVar()
        accountNum = StringVar()
        
        if str(employee.pay_method) == 'direct deposit':
            routingNum.set(employee.pay_method.route_num)
            accountNum.set(employee.pay_method.account_num)
        else:
            routingNum.set('None')
            accountNum.set('None')
        
        
        try:
            hourly_rate = StringVar()
            hourly_rate.set(employee.classification.hourly_rate)
        except AttributeError:
            pass
        try:
            salary = StringVar()
            salary.set(employee.classification.salary)
        except AttributeError:
            pass
        try:
            commission = StringVar()
            commission.set(employee.classification.commission_rate)
        except AttributeError:
            pass

        self.emp_ID_label = tk.Label(self.view_frame, name='emp_id_label', justify='right', text="Employee ID:", font=('Arial', 10))
        self.emp_ID_entry = tk.Entry(self.view_frame, name='emp_id_entry', font=('Arial', 10), state=DISABLED, textvariable=emp_id)
        self.first_name_label = tk.Label(self.view_frame, name='first_name_label', justify='right', text="First Name:", font=('Arial', 10))
        self.first_name_entry = tk.Entry(self.view_frame, name='first_name_entry', font=('Arial', 10), state=DISABLED, textvariable=first_name)
        self.last_name_label = tk.Label(self.view_frame, name='last_name_label', justify='right', text="Last Name:", font=('Arial', 10))
        self.last_name_entry = tk.Entry(self.view_frame, name='last_name_entry', font=('Arial', 10), state=DISABLED, textvariable=last_name)
        self.address_label = tk.Label(self.view_frame, name='address_label', justify='right', text="Address:", font=('Arial', 10))
        self.address_entry = tk.Entry(self.view_frame, name='address_entry', font=('Arial', 10), state=DISABLED, textvariable=address)
        self.city_label = tk.Label(self.view_frame, name='city_label', justify='right', text="City:", font=('Arial', 10))
        self.city_entry = tk.Entry(self.view_frame, name='city_entry', font=('Arial', 10), state=DISABLED, textvariable=city)
        self.state_label = tk.Label(self.view_frame, name='state_label', justify='right', text="State:", font=('Arial', 10))
        self.state_entry = tk.Entry(self.view_frame, name='state_entry', font=('Arial', 10), state=DISABLED, textvariable=state)
        self.zip_label = tk.Label(self.view_frame, name='zip_label', justify='right', text="Zip:", font=('Arial', 10))
        self.zip_entry = tk.Entry(self.view_frame, name='zip_entry', font=('Arial', 10), state=DISABLED, textvariable=zipcode)
        
        self.classification_label = tk.Label(self.view_frame, name='classification_label', justify='right', text="Classification:", font=('Arial', 10))
        
        self.hourly_label = tk.Label(self.view_frame, name='hourly_label', text="Hourly Rate:", font=('Arial', 10)) 
        self.hourly_entry = tk.Entry(self.view_frame, name='hourly_entry', state=DISABLED, textvariable=hourly_rate, font=('Arial', 10))
        self.salary_label = tk.Label(self.view_frame, name='salary_label', text="Salary:", font=('Arial', 10)) 
        self.salary_entry = tk.Entry(self.view_frame, name='salary_entry', state=DISABLED, textvariable=salary, font=('Arial', 10))
        self.commission_label = tk.Label(self.view_frame, name='commision_label', text="Commission Rate:", font=('Arial', 10))
        self.commission_entry = tk.Entry(self.view_frame, name='commision_entry', state=DISABLED, textvariable=commission, font=('Arial', 10))
        
        def classification_dropdown_func(*args):
            print(f"the variable has changed to '{self.classification_clicked.get()}'")
                # Show pay amounts, based on classification type:
            if self.classification_clicked.get() == "hourly":
                self.hourly_label.grid(column=1,row=11, sticky='E', padx=15, pady=7)
                self.hourly_entry.grid(column=2,row=11)
                self.commission_label.grid_forget()
                self.commission_entry.grid_forget()
                self.salary_label.grid_forget()
                self.salary_label.grid_forget()
                
            # Salary
            elif self.classification_clicked.get() == "salary":
                self.salary_label.grid(column=1,row=11, sticky='E', padx=15, pady=7)
                self.salary_entry.grid(column=2,row=11)
                self.hourly_label.grid_forget()
                self.hourly_entry.grid_forget()
                self.commission_label.grid_forget()
                self.commission_entry.grid_forget()
            # Commission
            elif self.classification_clicked.get() == "commissioned":
                self.salary_label.grid(column=1,row=11, sticky='E', padx=15, pady=7)
                self.salary_entry.grid(column=2,row=11)
                self.commission_label.grid(column=1,row=12, sticky='E', padx=15, pady=7)
                self.commission_entry.grid(column=2,row=12)
                self.hourly_label.grid_forget()
                self.hourly_entry.grid_forget()
                
                
        if mode != 'cancel':
            self.classification_clicked = StringVar()
            self.classification_clicked.trace('w', classification_dropdown_func)
            self.classification_clicked.set(str(employee.classification))
            self.classification_dropdown = OptionMenu(self.view_frame, self.classification_clicked, "- Select -", "hourly", "salary", "commissioned")
            
            self.payment_method_clicked = StringVar()
            self.payment_method_clicked.set(str(employee.pay_method))
            self.payment_method_dropdown = OptionMenu(self.view_frame, self.payment_method_clicked, "- Select -", "direct deposit", "mail")

            self.permission_level_clicked = StringVar()
            self.permission_level_clicked.set(employee.permission)
            self.permission_level_dropdown = OptionMenu(self.view_frame, self.permission_level_clicked, "- Select -", "employee", "admin")
            
        self.classification_dropdown.configure(state=DISABLED)
        self.payment_method_dropdown.configure(state=DISABLED)
        self.permission_level_dropdown.configure(state=DISABLED)
        
        
   
        self.personal_phone_label = tk.Label(self.view_frame, name='personal_phone_label', justify='right', text="Personal Phone:", font=('Arial', 10))
        self.personal_phone_entry = tk.Entry(self.view_frame, name='personal_phone_entry', font=('Arial', 10), state=DISABLED, textvariable=phone)
        self.personal_email_label = tk.Label(self.view_frame, name='personal_email_label', justify='right', text="Personal Email:", font=('Arial', 10))
        self.personal_email_entry = tk.Entry(self.view_frame, name='personal_email_entry', font=('Arial', 10), state=DISABLED, textvariable=email)
        self.DOB_label = tk.Label(self.view_frame, name='dob_label', justify='right', text="Date of Birth:", font=('Arial', 10))
        self.DOB_entry = tk.Entry(self.view_frame, name='dob_entry', font=('Arial', 10), state=DISABLED, textvariable=dob)
        
        self.SSN_label = tk.Label(self.view_frame, name='ssn_label', justify='right', text="SSN:", font=('Arial', 10))
        self.SSN_entry = tk.Entry(self.view_frame, name='ssn_entry', font=('Arial', 10), state=DISABLED, textvariable=ssn)
        
        self.routing_number_label = tk.Label(self.view_frame, name='routing_number_label', justify='right', text="Routing Number:", font=('Arial', 10))
        self.routing_number_entry = tk.Entry(self.view_frame, name='routing_number_entry', font=('Arial', 10), state=DISABLED, textvariable=routingNum)
        self.account_number_label = tk.Label(self.view_frame, name='account_number_label', justify='right', text="Account Number:", font=('Arial', 10))
        self.account_number_entry = tk.Entry(self.view_frame, name='account_number_entry', font=('Arial', 10), state=DISABLED, textvariable=accountNum)
        self.payment_method_label = tk.Label(self.view_frame, name='payment_method_label', justify='right', text="Payment Method:", font=('Arial', 10))
        
        self.job_title_label = tk.Label(self.view_frame, name='job_title_label', justify='right', text="Job Title:", font=('Arial', 10))
        self.job_title_entry = tk.Entry(self.view_frame, name='job_title_entry', font=('Arial', 10), state=DISABLED, textvariable=job_title)
        self.job_department_label = tk.Label(self.view_frame, name='job_department_label', justify='right', text="Department:", font=('Arial', 10))
        self.job_department_entry = tk.Entry(self.view_frame, name='job_department_entry', font=('Arial', 10), state=DISABLED, textvariable=job_dept)
        self.start_date_label = tk.Label(self.view_frame, name='start_date_label', justify='right', text="Start Date:", font=('Arial', 10))
        self.start_date_entry = tk.Entry(self.view_frame, name='start_date_entry', font=('Arial', 10), state=DISABLED, textvariable=start_date)
        self.end_date_label = tk.Label(self.view_frame, name='end_date_label', justify='right', text="End Date:", font=('Arial', 10))
        self.end_date_entry = tk.Entry(self.view_frame, name='end_date_entry', font=('Arial', 10), state=DISABLED, textvariable=end_date)
        self.employment_status_label = tk.Label(self.view_frame, name='employment_status_label', justify='right', text="Employment Status:", font=('Arial', 10))
        self.employment_status_entry = tk.Entry(self.view_frame, name='employment_status_entry', font=('Arial', 10), state=DISABLED, textvariable=job_status)
        self.password_label = tk.Label(self.view_frame, name='password_label', justify='right', text="Password:", font=('Arial', 10))
        self.password_entry = tk.Entry(self.view_frame, name='password_entry', font=('Arial', 10), state=DISABLED, textvariable=password)
        self.permission_level_label = tk.Label(self.view_frame, name='permission_level_label', justify='right', text="Permission Level:", font=('Arial', 10))
        
        
        self.emp_ID_label.grid(column=1, row=1, sticky='E', padx=15, pady=7)
        self.first_name_label.grid(column=1, row=2, sticky='E', padx=15, pady=7)
        self.last_name_label.grid(column=1, row=3, sticky='E', padx=15, pady=7)
        self.address_label.grid(column=1, row=4, sticky='E', padx=15, pady=7)
        self.city_label.grid(column=1, row=5, sticky='E', padx=15, pady=7)
        self.state_label.grid(column=1, row=6, sticky='E', padx=15, pady=7)
        self.zip_label.grid(column=1, row=7, sticky='E', padx=15, pady=7)
        self.personal_phone_label.grid(column=1, row=8, sticky='E', padx=15, pady=7)
        self.personal_email_label.grid(column=1, row=9, sticky='E', padx=15, pady=7)
        self.classification_label.grid(column=1, row=10, sticky='E', padx=15, pady=7)
        
        self.DOB_label.grid(column=3, row=1, sticky='E', padx=15, pady=7)
        self.SSN_label.grid(column=3, row=2, sticky='E', padx=15, pady=7)
        self.payment_method_label.grid(column=3, row=5, sticky='E', padx=15, pady=7)
        self.job_title_label.grid(column=3, row=7, sticky='E', padx=15, pady=7)
        self.job_department_label.grid(column=3, row=8, sticky='E', padx=15, pady=7)
        self.start_date_label.grid(column=3, row=9, sticky='E', padx=15, pady=7)
        self.end_date_label.grid(column=3, row=10, sticky='E', padx=15, pady=7)
        self.employment_status_label.grid(column=3, row=11, sticky='E', padx=15, pady=7)
        
        self.password_label.grid(column=5, row=1, sticky='E', padx=15, pady=7)
        self.permission_level_label.grid(column=5, row=2, sticky='E', padx=15, pady=7)
        
        self.emp_ID_entry.grid(column=2 , row=1)
        self.first_name_entry.grid(column=2 , row=2)
        self.last_name_entry.grid(column=2 , row=3)
        self.address_entry.grid(column=2 , row=4)
        self.city_entry.grid(column=2 , row=5)
        self.state_entry.grid(column=2 , row=6)
        self.zip_entry.grid(column=2 , row=7)
        self.personal_phone_entry.grid(column=2 , row=8)
        self.personal_email_entry.grid(column=2 , row=9)
        self.classification_dropdown.grid(column=2 , row=10)
    
        self.DOB_entry.grid(column=4 , row=1)
        self.SSN_entry.grid(column=4 , row=2)
        self.payment_method_dropdown.grid(column=4 , row=5)
        self.job_title_entry.grid(column=4 , row=7)
        self.job_department_entry.grid(column=4 , row=8)
        self.start_date_entry.grid(column=4 , row=9)
        self.end_date_entry.grid(column=4 , row=10)
        self.employment_status_entry.grid(column=4 , row=11)
        
        self.password_entry.grid(column=6 , row=1)
        self.permission_level_dropdown.grid(column=6 , row=2)

        if str(employee.pay_method) == 'direct deposit':
            self.routing_number_label.grid(column=3, row=3, sticky='E', padx=15, pady=7)
            self.account_number_label.grid(column=3, row=4, sticky='E', padx=15, pady=7)
            self.routing_number_entry.grid(column=4 , row=3)
            self.account_number_entry.grid(column=4 , row=4)
            
class admin_page(tk.Frame):
    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Admin Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        # self.addEmpBtn = tk.Button(self.view_frame, text="Add New Employee",
        #                         command= self.add_emp)
        # self.addEmpBtn.grid(column=0, row=0)
        
        columns_list = ("emp_ip_column", "first_name_column", "last_name_column", 
                        "phone_number_column", "email_column", "start_date_column", 
                        "end_date_column", "classification_column", "title_column",
                        "deptartment_column")
    
        emp_tree = ttk.Treeview(self, columns=columns_list, show='headings')
        
        for col in columns_list:
            emp_tree.column(col, width=120)
            
        def treeview_sort_column(treeview, col, reverse):
            """Sort a treeview column when clicked"""
            data = [
                (treeview.set(iid, col), iid)
                for iid in treeview.get_children('')
            ]
            
            data.sort(reverse=reverse)
            
            for index, (sort_val, iid) in enumerate(data):
                treeview.move(iid, '', index)
                
            treeview.heading(
                col,
                command=lambda c=col: treeview_sort_column(treeview, c, not reverse)
            )
                
        for col in columns_list:
            emp_tree.heading(col, 
                            command=lambda c=col: treeview_sort_column(emp_tree, c, False)
                            )
        
        
        #create heading
        # my_tree.heading("#0", text="Label", anchor=W) #text is optional
        emp_tree.heading("emp_ip_column", text="Employee ID", anchor=W)
        emp_tree.heading("first_name_column", text="First Name", anchor=W)
        emp_tree.heading("last_name_column", text="Last Name", anchor=W)
        emp_tree.heading("phone_number_column", text="Phone Number", anchor=W)
        emp_tree.heading("email_column", text="Email", anchor=W)
        emp_tree.heading("start_date_column", text="Start Date", anchor=W)
        emp_tree.heading("end_date_column", text="End Date", anchor=W)
        emp_tree.heading("classification_column", text="Classification", anchor=W)
        emp_tree.heading("title_column", text="Title", anchor=W)
        emp_tree.heading("deptartment_column", text="Department", anchor=W)
        
        emp_tree.pack(pady=20)
        
        # Iterate through all employees to list them out.
        global COUNT
        COUNT = 0
        for emp in EmpDat.emp_list:
            if COUNT % 2 == 0:
                emp_tree.insert('', END, values=(emp.id, emp.first_name,
                                                    emp.last_name, emp.phone, emp.email,
                                                    emp.start_date, emp.end_date,
                                                    str(emp.classification), emp.title, emp.dept),
                                    tags=("evenrows",))
            else:
                emp_tree.insert('', END, values=(emp.id, emp.first_name,
                                                    emp.last_name, emp.phone, emp.email,
                                                    emp.start_date, emp.end_date,
                                                    str(emp.classification), emp.title,
                                                    emp.dept), tags=("oddrows",))
            COUNT += 1
            
        #########
        # Binds #
        #########
        
        def selected_employee(event):
            """Brings up an employee's information in a separate GUI window.
            Intended to be called with a double-click event handler, so that
            an employee's info shows up when you click on them.
            """
            # Bring up employee information after double-click
            for selected_emp_idx in emp_tree.selection():
                emp_data = emp_tree.item(selected_emp_idx)
                emp_id = emp_data["values"][0]
                emp = find_employee_by_id(emp_id, EmpDat.emp_list) 
            self.controller.frames['emp_page'].emp_page_entries(emp)
            self.controller.show_frame("emp_page")          
        emp_tree.bind("<Double 1>", selected_employee)
        emp_tree.pack()

class add_employee_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="New Employee", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)        
        self.sumbitBnt = tk.Button(self, text="Submit")
        self.sumbitBnt.pack()