import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import askyesno
from tkinter import font  as tkfont
from tkinter import ttk
import re
# from PIL import Image, ImageTk
import uuid

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
        self.mode = None
        self.employee_id = None
        label = tk.Label(self, text="Home Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        self.view_frame = LabelFrame(self, border=True) ################################# !!! REMINDER !!! -> Remove border when done formatting
        self.view_frame.pack(fill='x')
        
        self.editEmp = tk.Button(self.view_frame, text='Edit Employee', command=lambda: self.edit_emp())
        self.editEmp.grid(column=0, row=1)
        
        self.backBtn = tk.Button(self.view_frame, text='Back', command=lambda: self.controller.show_frame("admin_page") )
        
        self.submitBtn = tk.Button(self.view_frame, text='Submit', command=lambda: self.make_new_employee())
        
        self.saveBtn = tk.Button(self.view_frame, text='Save', command=lambda: self.save_edit_emp())
        
        self.cancelBtn = tk.Button(self.view_frame, text='Cancel', command=lambda: self.cancel_edit_emp())
        
        
    # Clears all data fields in employee page to fill in new employee info
    def add_emp_innit(self):
        self.parse_entry('parse', 'normal')
        self.classification_clicked.set('- Select -')
        self.state_dropdown.current(0)
        self.payment_method_clicked.set('- Select -')
        self.permission_level_clicked.set('- Select -')
        self.controller.frames['emp_page'].editEmp.grid_forget()
        self.controller.frames['emp_page'].submitBtn.grid(column=0,row=1)
        self.backBtn['text'] = 'Cancel'
        
    def validate_employee(self, emp):
        errorMsg = {}
        
        
        if not emp['first_name_entry'].strip():
            self.first_name_entry.config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
            errorMsg['first_name_empty_err'] = '• Error: First Name must have a value!\n' 
        elif not emp['first_name_entry'].isalpha():
            self.first_name_entry.config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
            errorMsg['first_name_NaN'] = '• Error: First Name must only contain letters!\n'
        else:
            if 'first_name_NaN' in errorMsg:
                del errorMsg['first_name_NaN']
            if 'first_name_empty_err' in errorMsg:
                del errorMsg['first_name_empty_err']
                
        if not emp['last_name_entry'].strip():
            self.last_name_entry.config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
            errorMsg['last_name_empty_err'] = '• Error: Last Name must have a value!\n' 
        elif not emp['last_name_entry'].isalpha():
            self.last_name_entry.config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
            errorMsg['last_name_NaN'] = '• Error: Last Name must only contain letters!\n'
        else:
            if 'last_name_NaN' in errorMsg:
                del errorMsg['last_name_NaN']
            if 'last_name_empty_err' in errorMsg:
                del errorMsg['last_name_empty_err']
                
        if re.search(r"[a-zA-Z]", emp['address_entry']) is None or \
                re.search("[0-9]", emp['address_entry']) is None:
            self.address_entry.config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
            errorMsg['address_err'] = '• Address must have letters and numbers!\n'
        else:
            if 'address_err' in errorMsg:
                del errorMsg['address_err']
                
        if re.search(r"^[a-zA-Z]+[ -]*[a-zA-Z]+$", emp['city_entry']) is None:
            self.city_entry.config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
            errorMsg['city_err'] = '• City must have letters only, with one space or dash allowed!\n'
        else:
            if 'city_err' in errorMsg:
                del errorMsg['city_err']
                
        if emp['State'] == '- Select -':
            errorMsg['state_err'] = '• State must have a value!\n'
        else:
            if 'state_err' in errorMsg:
                del errorMsg['state_err']
                
        if re.search(r"\d\d\d\d\d", emp['zip_entry']) is None:
            self.zip_entry.config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
            errorMsg['zip_err'] = '• Zip code must contain 5 consecutive digits!\n'
        else:
            if 'zip_err' in errorMsg:
                del errorMsg['zip_err']
                
        if re.search(r"^\(\d\d\d\)\d\d\d-\d\d\d\d$", emp['personal_phone_entry']) is None \
                and re.search(r"^\d\d\d-\d\d\d-\d\d\d\d$", emp['personal_phone_entry']) is \
                None and re.search(r"^\d\d\d\d\d\d\d\d\d\d$", emp['personal_phone_entry']) \
                is None:
            self.personal_phone_entry.config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
            errorMsg['personal_phone_err'] = '• Phone number must match one of the following formats: \n   (###)###-#### or ###-###-#### or ##########!\n'
        else:
            if 'personal_phone_err' in errorMsg:
                del errorMsg['personal_phone_err']
                
        if re.search(r"^.*\w.*@\w.*\.\w+$", emp['personal_email_entry']) is None:
            self.personal_email_entry.config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
            errorMsg['personal_email_err'] = '• Email address is not valid!\n'
        else:
            if 'personal_email_err' in errorMsg:
                del errorMsg['personal_email_err']
           
        if emp['Classification'] == '- Select -':
            errorMsg['classification_err'] = '• Classification must have a value!\n'
        else:
            if 'classification_err' in errorMsg:
                del errorMsg['classification_err']
        if re.search(r"^\d\d\/\d\d\/\d\d\d\d$", emp['dob_entry']) is None \
                and re.search(r"^\d\d-\d\d-\d\d\d\d$", emp['dob_entry']) is \
                None:
            self.DOB_entry.config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
            errorMsg['dob_err'] = '• Dates must match the format: MM/DD/YYYY or MM-DD-YYYY\n'
        else:
            if 'dob_err' in errorMsg:
                del errorMsg['dob_err']
                
        if re.search(r"^\d\d\d-\d\d-\d\d\d\d$", emp['ssn_entry']) is None and \
                re.search(r"^\d\d\d\d\d\d\d\d\d$", emp['ssn_entry']) is None:
            self.SSN_entry.config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
            errorMsg['ssn_err'] = '• SSN must match the format: ###-##-#### or ######### (9 digits)\n'
        else:
            if 'ssn_err' in errorMsg:
                del errorMsg['ssn_err']
                
        if emp['Pay_Method'] == '- Select -':
            errorMsg['Pay_Method_err'] = '• Pay_Method must have a value!\n'
        else:
            if 'Pay_Method_err' in errorMsg:
                del errorMsg['Pay_Method_err']
                
        ################################### Back Account Info Validation goes here !! Dont forget!! ########
                
        if re.search(r"^\w+.?\w+$", emp['job_title_entry']) is None:
            self.job_title_entry.config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
            errorMsg['job_title_err'] = '• Employee Title must have letters and numbers \
                          only, with one special character in between  \
                          characters allowed.\n'
        else:
            if 'job_title_err' in errorMsg:
                del errorMsg['job_title_err']
        if re.search(".+", emp['job_department_entry']) is None:
            self.job_department_entry.config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
            errorMsg['job_department_err'] = '• Employee department must not be empty!\n'
        else:
            if 'job_department_err' in errorMsg:
                del errorMsg['job_department_err']
        if re.search(r"^\d\d\/\d\d\/\d\d\d\d$", emp['start_date_entry']) is None \
                and re.search(r"^\d\d-\d\d-\d\d\d\d$", emp['start_date_entry']) is \
                None:
            self.start_date_entry.config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
            errorMsg['start_date_err'] = '• Start Date must match the format: MM/DD/YYYY or MM-DD-YYYY\n'
        else:
            if 'start_date_err' in errorMsg:
                del errorMsg['start_date_err']
        
        if emp['end_date_entry']:  
            if re.search(r"^\d\d\/\d\d\/\d\d\d\d$", emp['end_date_entry']) is None \
                    and re.search(r"^\d\d-\d\d-\d\d\d\d$", emp['end_date_entry']) is \
                    None:
                self.start_date_entry.config(highlightbackground = "red", highlightcolor= "red", highlightthickness=1)
                errorMsg['end_date_err'] = '• End Date must match the format: MM/DD/YYYY or MM-DD-YYYY\n'
            else:
                if 'end_date_err' in errorMsg:
                    del errorMsg['end_date_err']
                    
        if emp['permission'] == '- Select -':
            errorMsg['permission_err'] = '• Permission option must have a value!\n'
        else:
            if 'permission_err' in errorMsg:
                del errorMsg['permission_err']
       
           
           
        self.focus()
        if errorMsg:
            arr = ''.join(list(errorMsg.values()))
            messagebox.showerror("Error", arr)
        else:
            pass
            # add_new_employee(EmpDat, new_id, emp_f_name, emp_l_name,
            #                  emp_address, emp_city, emp_state, emp_zip, emp_class,
            #                  emp_pay_num, emp_b_day, emp_ssn, emp_phone, emp_email,
            #                  emp_start_date, emp_title, emp_dept, emp_permission,
            #                  emp_pwd, emp_route_num, emp_account_num)

    def make_new_employee(self):
        check_valid = {
                'input_hasValue': False
        }
        new_emp_val = {}
        new_emp_val['Classification'] = self.classification_clicked.get()
        new_emp_val['Pay_Method'] = self.payment_method_clicked.get()
        new_emp_val['State'] = self.state_dropdown.get()
        new_emp_val['permission'] = self.permission_level_clicked.get()
        
        for x in self.controller.frames['emp_page'].view_frame.children:
            if (('entry') in x or self.view_frame.children[x].widgetName ==  "tk_optionMenu") and (x not in 'emp_id_entry' and x not in 'employment_status_entry'):
                if ('entry') in x: 
                    new_emp_val[x] = self.controller.frames['emp_page'].view_frame.children[x].get()
        
        
        
            
            
            
            
            
            
        
    def add_emp_submit(self):
        Valid = True
        new_emp = self.make_new_employee()
        assert new_emp == Valid
        
    def submit_emp(self):
        print("submitting new employee form")
        
        
    def save_edit_emp(self):
        self.controller.edit_employee = False 
        self.controller.frames['emp_page'].saveBtn.grid_forget()
        self.controller.frames['emp_page'].cancelBtn.grid_forget()
        self.controller.frames['emp_page'].editEmp.grid(column=0, row=1)
        self.parse_entry('save','none')
    
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
            
        
    def parse_entry(self, mode = None, state = None):
        if mode == 'save':
            entryDict = {
                    'ID': self.emp_ID_entry.get(),
                    'Address': self.address_entry.get(),
                    'Name': " ".join([self.first_name_entry.get(), self.last_name_entry.get()]),
                    'City': self.city_entry.get(),
                    'State': self.state_dropdown.get(),
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
            
            
            EmpDat.edit_employee(self.employee_id, list(entryDict.keys()), list(entryDict.values()))
            self.parse_entry('parse', 'disabled')
            
            
         
        elif mode == 'parse':
            for x in self.controller.frames['emp_page'].view_frame.children:  # will parse through all widgets --acts like event handler that updates window when there are changes
                if self.controller.user.permission == 'admin':
                    if (('entry') in x or self.view_frame.children[x].widgetName ==  "tk_optionMenu" or self.view_frame.children[x].widgetName == "ttk::combobox") and (x not in 'emp_id_entry' and x not in 'employment_status_entry'):                     
                        if self.view_frame.children[x].widgetName == "ttk::combobox" and state == 'normal':
                            self.controller.frames['emp_page'].view_frame.children[x]['state'] = 'readonly'
                        else: self.controller.frames['emp_page'].view_frame.children[x]['state'] = state
                        if self.mode == 'add employee':
                            if ('entry') in x: 
                                self.controller.frames['emp_page'].view_frame.children[x].delete(0,END)
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
        self.mode = mode  # changes parser mode so it can initilize each individual field for new employee
        
        def remove_highlight(event):
            event.widget['highlightthickness'] = 0
        
        self.employee_selected = employee
        
        if self.controller.user.permission == 'admin':
            self.backBtn.grid(column=0, row=2)
        else:
            self.backBtn.grid_forget()
        
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
        if self.mode == 'add employee':
            self.first_name_entry.bind('<FocusIn>', remove_highlight)
        self.last_name_label = tk.Label(self.view_frame, name='last_name_label', justify='right', text="Last Name:", font=('Arial', 10))
        self.last_name_entry = tk.Entry(self.view_frame, name='last_name_entry', font=('Arial', 10), state=DISABLED, textvariable=last_name)
        if self.mode == 'add employee':
            self.last_name_entry.bind('<FocusIn>', remove_highlight)
        self.address_label = tk.Label(self.view_frame, name='address_label', justify='right', text="Address:", font=('Arial', 10))
        self.address_entry = tk.Entry(self.view_frame, name='address_entry', font=('Arial', 10), state=DISABLED, textvariable=address)
        if self.mode == 'add employee':
            self.address_entry.bind('<FocusIn>', remove_highlight)
        self.city_label = tk.Label(self.view_frame, name='city_label', justify='right', text="City:", font=('Arial', 10))
        self.city_entry = tk.Entry(self.view_frame, name='city_entry', font=('Arial', 10), state=DISABLED, textvariable=city)
        if self.mode == 'add employee':
            self.city_entry.bind('<FocusIn>', remove_highlight)
            
            
        
        self.state_label = tk.Label(self.view_frame, name='state_label', justify='right', text="State:", font=('Arial', 10))
        self.zip_label = tk.Label(self.view_frame, name='zip_label', justify='right', text="Zip:", font=('Arial', 10))
        self.zip_entry = tk.Entry(self.view_frame, name='zip_entry', font=('Arial', 10), state=DISABLED, textvariable=zipcode)
        if self.mode == 'add employee':
            self.zip_entry.bind('<FocusIn>', remove_highlight)
            
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
            stateDict = {
            0:'- Select -',1:'AL',2:'AK',3:'AZ',4:'AR',5:'CA',6:'CO',7:'CT',8:'DE',9:'FL',10:'GA',11:'HI',
            12:'ID',13:'IL',14:'IN',15:'IA',16:'KS',17:'KY',18:'LA',19:'ME',20:'MD',21:'MA',22:'MI',
            23:'MN',24:'MS',25:'MO',26:'MT',27:'NE',28:'NV',29:'NH',30:'NJ',31:'NM',32:'NY',33:'NC',
            34:'ND',35:'OH',36:'OK',37:'OR',38:'PA',39:'RI',40:'SC',41:'SD',42:'TN',43:'TX',44:'UT',
            45:'VT',46:'VA',47:'WA',48:'WV',49:'WI',50:'WY'
            }
             
            # self.state_dropdown = tk.Entry(self.view_frame, name='state_entry', font=('Arial', 10), state=DISABLED, textvariable=state)
            self.state_clicked = StringVar()
            self.state_clicked.set(employee.state)
            self.state_dropdown = ttk.Combobox(self.view_frame, value = list(stateDict.values()), state=DISABLED)
            for key,val in stateDict.items():
                if val == employee.state:
                    self.state_dropdown.current(key)
                    break
            
            
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
            
        self.state_dropdown.configure(state=DISABLED)
        self.classification_dropdown.configure(state=DISABLED)
        self.payment_method_dropdown.configure(state=DISABLED)
        self.permission_level_dropdown.configure(state=DISABLED)
        
        
   
        self.personal_phone_label = tk.Label(self.view_frame, name='personal_phone_label', justify='right', text="Personal Phone:", font=('Arial', 10))
        self.personal_phone_entry = tk.Entry(self.view_frame, name='personal_phone_entry', font=('Arial', 10), state=DISABLED, textvariable=phone)
        if self.mode == 'add employee':
            self.personal_phone_entry.bind('<FocusIn>', remove_highlight)
        self.personal_email_label = tk.Label(self.view_frame, name='personal_email_label', justify='right', text="Personal Email:", font=('Arial', 10))
        self.personal_email_entry = tk.Entry(self.view_frame, name='personal_email_entry', font=('Arial', 10), state=DISABLED, textvariable=email)
        if self.mode == 'add employee':
            self.personal_email_entry.bind('<FocusIn>', remove_highlight)
        
        self.DOB_label = tk.Label(self.view_frame, name='dob_label', justify='right', text="Date of Birth:", font=('Arial', 10))
        self.DOB_entry = tk.Entry(self.view_frame, name='dob_entry', font=('Arial', 10), state=DISABLED, textvariable=dob)
        if self.mode == 'add employee':
            self.DOB_entry.bind('<FocusIn>', remove_highlight)
            
        self.SSN_label = tk.Label(self.view_frame, name='ssn_label', justify='right', text="SSN:", font=('Arial', 10))
        self.SSN_entry = tk.Entry(self.view_frame, name='ssn_entry', font=('Arial', 10), state=DISABLED, textvariable=ssn)
        if self.mode == 'add employee':
            self.SSN_entry.bind('<FocusIn>', remove_highlight)
            
        self.routing_number_label = tk.Label(self.view_frame, name='routing_number_label', justify='right', text="Routing Number:", font=('Arial', 10))
        self.routing_number_entry = tk.Entry(self.view_frame, name='routing_number_entry', font=('Arial', 10), state=DISABLED, textvariable=routingNum)
        self.account_number_label = tk.Label(self.view_frame, name='account_number_label', justify='right', text="Account Number:", font=('Arial', 10))
        self.account_number_entry = tk.Entry(self.view_frame, name='account_number_entry', font=('Arial', 10), state=DISABLED, textvariable=accountNum)
        self.payment_method_label = tk.Label(self.view_frame, name='payment_method_label', justify='right', text="Payment Method:", font=('Arial', 10))
        
        self.job_title_label = tk.Label(self.view_frame, name='job_title_label', justify='right', text="Job Title:", font=('Arial', 10))
        self.job_title_entry = tk.Entry(self.view_frame, name='job_title_entry', font=('Arial', 10), state=DISABLED, textvariable=job_title)
        if self.mode == 'add employee':
            self.job_title_entry.bind('<FocusIn>', remove_highlight)
            
        self.job_department_label = tk.Label(self.view_frame, name='job_department_label', justify='right', text="Department:", font=('Arial', 10))
        self.job_department_entry = tk.Entry(self.view_frame, name='job_department_entry', font=('Arial', 10), state=DISABLED, textvariable=job_dept)
        if self.mode == 'add employee':
            self.job_department_entry.bind('<FocusIn>', remove_highlight)
            
        self.start_date_label = tk.Label(self.view_frame, name='start_date_label', justify='right', text="Start Date:", font=('Arial', 10))
        self.start_date_entry = tk.Entry(self.view_frame, name='start_date_entry', font=('Arial', 10), state=DISABLED, textvariable=start_date)
        if self.mode == 'add employee':
            self.start_date_entry.bind('<FocusIn>', remove_highlight)
            
        self.end_date_label = tk.Label(self.view_frame, name='end_date_label', justify='right', text="End Date:", font=('Arial', 10))
        self.end_date_entry = tk.Entry(self.view_frame, name='end_date_entry', font=('Arial', 10), state=DISABLED, textvariable=end_date)
        if self.mode == 'add employee':
            self.end_date_entry.bind('<FocusIn>', remove_highlight)
            
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
        self.state_dropdown.grid(column=2 , row=6)
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
        s=ttk.Style()
        s.theme_use('clam')
        s.configure('Treeview', rowheight=30)
        
        self.btn_frame = LabelFrame(self, border=True) ################################# !!! REMINDER !!! -> Remove border when done formatting
        self.btn_frame.pack(side='bottom', fill=BOTH)
        
            
        def add_emp():
            new_id = EmpDat.unusedIdList.pop()
            temp_emp = Employee(new_id, '', '', '', '', '', '', '','')
            self.controller.frames['emp_page'].emp_page_entries(temp_emp, 'add employee')
            self.controller.frames['emp_page'].add_emp_innit()
            
            
            
            
            # add_new_employee(uvuEmpDat, new_id, emp_f_name, emp_l_name,
            #                  emp_address, emp_city, emp_state, emp_zip, emp_class,
            #                  emp_pay_num, emp_b_day, emp_ssn, emp_phone, emp_email,
            #                  emp_start_date, emp_title, emp_dept, emp_permission,
            #                  emp_pwd, emp_route_num, emp_account_num)
            
            
        
        
        # SearchIcon = PhotoImage(file = 'emp_data_project/emp_data/SearchIcon.png')
        # photoimage = SearchIcon.subsample(1, 1)
        
        
        
        self.searchEmp_label = Label(self, text="Search", font=('Arial', 10)).place(x=500,y=420)
        # self.searchEmp_icon = Label(self, image=photoimage).grid(x=0,y=1)
        self.searchEmp_entry = Entry(self, font=('Arial', 10)).place(x=550,y=420)
        self.addEmpBtn = tk.Button(self, text="Add New Employee", command= lambda: add_emp()).place(x=550,y=450)
        
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