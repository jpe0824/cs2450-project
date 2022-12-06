import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import askyesno
from tkinter import font as tkfont
from tkinter import ttk
import re
import itertools as it
# from PIL import Image, ImageTk
import uuid
import os

# from example_database import *
from Database import *
EmpDat = EmployeeDB()


class mycombobox(ttk.Combobox):
    """helper class for combobox that enables user to select their State by keyvalue. 
    i.e. 'user presses the key for letter "U" after clicking on widget, and the widget selection moves to "UT"'"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pd = self.tk.call('ttk::combobox::PopdownWindow',
                          self)  # get popdownWindow reference
        lb = pd + '.f.l'  # get popdown listbox
        self._bind(('bind', lb), "<KeyPress>", self.popup_key_pressed, None)

    def popup_key_pressed(self, evt):
        values = self.cget("values")
        for i in it.chain(range(self.current() + 1, len(values)), range(0, self.current())):
            if evt.char.lower() == values[i][0].lower():
                self.current(i)
                self.icursor(i)
                # clear current selection
                self.tk.eval(evt.widget + ' selection clear 0 end')
                self.tk.eval(evt.widget + ' selection set ' +
                             str(i))  # select new element
                # spin combobox popdown for selected element will be visible
                self.tk.eval(evt.widget + ' see ' + str(i))
                return


class EmpApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.edit_employee = False
        self.employee = None
        self.title_font = tkfont.Font(
            family='Helvetica', size=18, weight="bold", slant="italic")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1, minsize=600)
        container.grid_columnconfigure(0, weight=1, minsize=1100)
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
            answer = askyesno(
                title="Warning", message="You have unsaved information, are you sure you want to logout?")
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
            frame.logoutBtn = tk.Button(
                frame, text="Logout", command=lambda: self.logout())
            frame.logoutBtn.place(x=1050, y=0)
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
        border = tk.LabelFrame(
            self, text='Login', bg='#333333', fg="#FF3399", font=("Arial Bold", 20))
        border.pack(fill="both", expand="yes", padx=150, pady=150)
        def enterKey_func(event):
            if self.username_entry.get() and not self.password_entry.get():
                self.validateLogin(
            self.username_entry.get(), '')
            elif not self.username_entry.get() and self.password_entry.get():
                self.validateLogin(
            '', self.password_entry.get())
            elif not self.username_entry.get() and not self.password_entry.get():
                self.validateLogin(
            '','')
            else:
                self.validateLogin(
            self.username_entry.get(), self.password_entry.get())
        # creating widgets for login page
        self.login_label = tk.Label(
            border, text="Login", bg='#333333', fg="#FF3399", font=('Arial', 30))
        self.username_label = tk.Label(
            border, text="Username", bg='#333333', fg="#FFFFFF", font=('Arial', 16))
        self.username_entry = tk.Entry(
            border, font=('Arial', 16), textvariable=username)
        self.username_entry.bind('<Return>', enterKey_func)
        
        self.password_entry = tk.Entry(
            border, show='*', font=('Arial', 16), textvariable=password)
        self.password_entry.bind('<Return>', enterKey_func)
        self.password_label = tk.Label(
            border, text='Password', bg='#333333', fg="#FFFFFF", font=('Arial', 16))
        self.login_button = tk.Button(border, text='Login', bg='#FF3399', fg='#FFFFFF', command=lambda: self.validateLogin(
            self.username_entry.get(), self.password_entry.get()))
        

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
            try:
                if employee.id == int(username):
                    valid_username = True
                if employee.password == password:
                    valid_password = True
                    self.controller.employee = employee
                    break
            except ValueError:
                continue

        if valid_username and valid_password:
            self.controller.user = employee
            # initialize username and password entry for when user logs out
            self.username_entry.delete(0, END)
            self.password_entry.delete(0, END)
            # ----------------------------------------------------
            self.focus()  # removes focus on data fields

            if self.controller.employee.permission == 'employee':
                self.controller.frames['emp_page'].emp_page_entries(
                    employee, 'employee')
                # calls show_frame from class EmpApp to change the frame to emp_page
                self.controller.show_frame("emp_page")
            elif self.controller.employee.permission == 'admin':
                # relitialize home page to include 'Add Employee Button' when user has admin privilege.
                self.controller.show_frame("admin_page")

        elif valid_username and not valid_password:
            self.password_entry.delete(0, END)
            messagebox.showerror("Invalid", "invalid password")

        else:
            self.password_entry.delete(0, END)
            messagebox.showerror("Invalid", "invalid username and password")


class emp_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.mode = None
        self.employee_id = None
        label = tk.Label(self, text="Home Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        # !!! REMINDER !!! -> Remove border when done formatting
        self.view_frame = LabelFrame(self, border=True)
        self.view_frame.pack(fill='x')

        self.editEmp = tk.Button(
            self.view_frame, text='Edit Employee', command=lambda: self.edit_emp())
        self.editEmp.grid(column=0, row=1)

        self.backBtn = tk.Button(self.view_frame, text='Back',
                                 command=lambda: self.controller.show_frame("admin_page"))

        self.submitBtn = tk.Button(
            self.view_frame, text='Submit', command=lambda: self.make_new_employee())

        self.saveBtn = tk.Button(
            self.view_frame, text='Save', command=lambda: self.save_edit_emp())

        self.cancelBtn = tk.Button(
            self.view_frame, text='Cancel', command=lambda: self.cancel_edit_emp())

    # Clears all data fields in employee page to fill in new employee info

    def add_emp_innit(self):
        self.parse_entry('parse', 'normal')
        self.controller.frames['emp_page'].editEmp.grid_forget()
        self.controller.frames['emp_page'].submitBtn.grid(column=0, row=1)
        self.backBtn['text'] = 'Cancel'

    def validate_employee(self, emp):
        errorMsg = {}

        if not emp['first_name_entry'].strip():
            self.first_name_entry.config(
                highlightbackground="red", highlightcolor="red", highlightthickness=1)
            errorMsg['first_name_empty_err'] = '• Error: First Name must have a value!\n'
        elif not emp['first_name_entry'].isalpha():
            self.first_name_entry.config(
                highlightbackground="red", highlightcolor="red", highlightthickness=1)
            errorMsg['first_name_NaN'] = '• Error: First Name must only contain letters!\n'

        if not emp['last_name_entry'].strip():
            self.last_name_entry.config(
                highlightbackground="red", highlightcolor="red", highlightthickness=1)
            errorMsg['last_name_empty_err'] = '• Error: Last Name must have a value!\n'
        elif not emp['last_name_entry'].isalpha():
            self.last_name_entry.config(
                highlightbackground="red", highlightcolor="red", highlightthickness=1)
            errorMsg['last_name_NaN'] = '• Error: Last Name must only contain letters!\n'

        if re.search(r"[a-zA-Z]", emp['address_entry']) is None or \
                re.search("[0-9]", emp['address_entry']) is None:
            self.address_entry.config(
                highlightbackground="red", highlightcolor="red", highlightthickness=1)
            errorMsg['address_err'] = '• Error: Address must have letters and numbers!\n'

        if re.search(r"^[a-zA-Z]+[ -]*[a-zA-Z]+$", emp['city_entry']) is None:
            self.city_entry.config(
                highlightbackground="red", highlightcolor="red", highlightthickness=1)
            errorMsg['city_err'] = '• Error: City must have letters only, with one space or dash allowed!\n'

        if emp['State'] == '- Select -':
            errorMsg['state_err'] = '• Error: State must have a value!\n'

        if re.search(r"\d\d\d\d\d", emp['zip_entry']) is None:
            self.zip_entry.config(highlightbackground="red",
                                  highlightcolor="red", highlightthickness=1)
            errorMsg['zip_err'] = '• Error: Zip code must contain 5 consecutive digits!\n'

        if re.search(r"^\(\d\d\d\)\d\d\d-\d\d\d\d$", emp['personal_phone_entry']) is None \
                and re.search(r"^\d\d\d-\d\d\d-\d\d\d\d$", emp['personal_phone_entry']) is \
                None and re.search(r"^\d\d\d\d\d\d\d\d\d\d$", emp['personal_phone_entry']) \
                is None:
            self.personal_phone_entry.config(
                highlightbackground="red", highlightcolor="red", highlightthickness=1)
            errorMsg[
                'personal_phone_err'] = '• Error: Phone number must match one of the following formats: \n   (###)###-#### or ###-###-#### or ##########!\n'

        if re.search(r"^.*\w.*@\w.*\.\w+$", emp['personal_email_entry']) is None:
            self.personal_email_entry.config(
                highlightbackground="red", highlightcolor="red", highlightthickness=1)
            errorMsg['personal_email_err'] = '• Error: Email address is not valid!\n'

        if emp['Classification'] == '- Select -':
            errorMsg['classification_err'] = '• Error: Classification must have a value!\n'

        if self.hourly_entry.grid_info():
            try:
                emp['hourly_entry'] == float(emp['hourly_entry'])
            except ValueError:
                self.hourly_entry.config(
                    highlightbackground="red", highlightcolor="red", highlightthickness=1)
                errorMsg['hourly_err'] = '• Error: Hourly pay must be a number, with 1 decimal point allowed.\n'

        if self.salary_entry.grid_info():
            try:
                emp['salary_entry'] == float(emp['salary_entry'])
            except ValueError:
                self.salary_entry.config(
                    highlightbackground="red", highlightcolor="red", highlightthickness=1)
                errorMsg['salary_err'] = '• Error: Salary must be a number, with 1 decimal point allowed.\n'

        if self.commission_entry.grid_info():
            try:
                emp['commission_entry'] == float(emp['commission_entry'])
            except ValueError:
                self.commission_entry.config(
                    highlightbackground="red", highlightcolor="red", highlightthickness=1)
                errorMsg['commission_err'] = '• Error: Commission must be a number, with 1 decimal point allowed.\n'

        if re.search("^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$", emp['dob_entry']) is None:
            self.DOB_entry.config(highlightbackground="red",
                                  highlightcolor="red", highlightthickness=1)
            errorMsg['dob_err'] = '• Error: Dates must match the format: MM/DD/YYYY\n'

        if re.search(r"^\d\d\d-\d\d-\d\d\d\d$", emp['ssn_entry']) is None and \
                re.search(r"^\d\d\d\d\d\d\d\d\d$", emp['ssn_entry']) is None:
            self.SSN_entry.config(highlightbackground="red",
                                  highlightcolor="red", highlightthickness=1)
            errorMsg[
                'ssn_err'] = '• Error: SSN must match the format: ###-##-#### or ######### (9 digits)\n'

        if emp['Pay_Method'] == '- Select -':
            errorMsg['Pay_Method_err'] = '• Error: Pay_Method must have a value!\n'

        if emp['Pay_Method'] == 'Direct Deposit':
            if re.search(r"^\d+-?\d+$", emp['account_number_entry']) is None:
                self.account_number_entry.config(
                    highlightbackground="red", highlightcolor="red", highlightthickness=1)
                errorMsg['account_number_err'] = '• Error: Bank account number should be numeric, with one dash allowed.\n'

            if re.search(r"^\d+-?\d+-?\d+$", emp['routing_number_entry']) is None:
                self.routing_number_entry.config(
                    highlightbackground="red", highlightcolor="red", highlightthickness=1)
                errorMsg['routing_number_err'] = '• Error: Routing number should be numeric, with up to two dashes allowed.\n'

        if re.search(r"^\w+.?\w+$", emp['job_title_entry']) is None:
            self.job_title_entry.config(
                highlightbackground="red", highlightcolor="red", highlightthickness=1)
            errorMsg['job_title_err'] = '• Error: Employee Title must have letters and numbers \
                          only, with one special character in between  \
                          characters allowed.\n'

        if re.search(".+", emp['job_department_entry']) is None:
            self.job_department_entry.config(
                highlightbackground="red", highlightcolor="red", highlightthickness=1)
            errorMsg['job_department_err'] = '• Error: Employee department must not be empty!\n'

        if re.search("^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$", emp['start_date_entry']) is None:
            self.start_date_entry.config(
                highlightbackground="red", highlightcolor="red", highlightthickness=1)
            errorMsg['start_date_err'] = '• Error: Start Date must match the format: MM/DD/YYYY\n'

        if emp['end_date_entry'] and emp['end_date_entry'] != 'MM/DD/YYYY':
            if re.search("^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$", emp['end_date_entry']) is None:
                self.end_date_entry.config(
                    highlightbackground="red", highlightcolor="red", highlightthickness=1)
                errorMsg['end_date_err'] = '• Error: End Date must match the format: MM/DD/YYYY\n'

        if not emp['password_entry'].strip():
            self.password_entry.config(
                highlightbackground="red", highlightcolor="red", highlightthickness=1)
            errorMsg['password_empty_err'] = '• Error: password must have a value!\n'

        if emp['permission'] == '- Select -':
            errorMsg['permission_err'] = '• Error: Permission option must have a value!\n'

        self.focus()
        if errorMsg:
            arr = ''.join(list(errorMsg.values()))
            messagebox.showerror("Error", arr)
            return False
        else:
            return True

    def get_emp_val(self):
        new_emp_dict = {}
        new_emp_dict['Classification'] = self.classification_clicked.get()
        new_emp_dict['Pay_Method'] = self.payment_method_clicked.get()
        new_emp_dict['State'] = self.state_dropdown.get()
        new_emp_dict['permission'] = self.permission_level_clicked.get()
        new_emp_dict['ID'] = self.employee_selected.id

        for x in self.controller.frames['emp_page'].view_frame.children:
            if ('entry') in x and (x not in 'emp_id_entry' and x not in 'employment_status_entry'):
                if ('entry') in x:
                    new_emp_dict[x] = self.controller.frames['emp_page'].view_frame.children[x].get(
                    )
        return new_emp_dict

    def make_new_employee(self):
        valid = True

        new_emp = self.get_emp_val()

        if self.validate_employee(new_emp) is valid:
            if new_emp['Classification'] == 'Hourly':

                emp_class = create_classification(1, new_emp['hourly_entry'])
            elif new_emp['Classification'] == 'Salary':
                emp_class = create_classification(2, new_emp['salary_entry'])
            else:
                emp_class = create_classification(
                    3, new_emp['salary_entry'], new_emp['commission_entry'])

            if new_emp['Pay_Method'] == 'Direct Deposit':
                pay_method_num = 1
            elif new_emp['Pay_Method'] == 'Mail':
                pay_method_num = 2

            employee = add_new_employee(EmpDat, new_emp['ID'], new_emp['first_name_entry'], new_emp['last_name_entry'],
                                        new_emp['address_entry'], new_emp['city_entry'], new_emp['State'], new_emp['zip_entry'], emp_class,
                                        pay_method_num, new_emp['dob_entry'], new_emp['ssn_entry'], new_emp[
                                            'personal_phone_entry'], new_emp['personal_email_entry'],
                                        new_emp['start_date_entry'], new_emp['job_title_entry'], new_emp[
                                            'job_department_entry'], new_emp['permission'],
                                        new_emp['password_entry'], new_emp['routing_number_entry'], new_emp['account_number_entry'])
            self.controller.frames['admin_page'].emp_tree.insert('', END, values=(employee.id, employee.first_name,
                                                                                  employee.last_name, employee.phone, employee.email,
                                                                                  employee.start_date, employee.end_date,
                                                                                  str(employee.classification), employee.title, employee.dept))
            self.controller.show_frame("admin_page")

    def add_emp_submit(self):
        Valid = True
        new_emp = self.make_new_employee()
        assert new_emp == Valid

    def submit_emp(self):
        print("submitting new employee form")

    def save_edit_emp(self):
        if (self.validate_employee(self.get_emp_val())):
            self.controller.edit_employee = False
            self.controller.frames['emp_page'].saveBtn.grid_forget()
            self.controller.frames['emp_page'].cancelBtn.grid_forget()
            self.controller.frames['emp_page'].editEmp.grid(column=0, row=1)
            self.parse_entry('save', 'none')

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

    def parse_entry(self, mode=None, state=None):
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

            EmpDat.edit_employee(self.employee_id, list(
                entryDict.keys()), list(entryDict.values()))
            self.parse_entry('parse', 'disabled')

        elif mode == 'parse':
            # will parse through all widgets --acts like event handler that updates window when there are changes
            for x in self.controller.frames['emp_page'].view_frame.children:
                if self.controller.user.permission == 'admin':
                    if (('entry') in x or self.view_frame.children[x].widgetName == "tk_optionMenu" or self.view_frame.children[x].widgetName == "ttk::combobox") and (x not in 'emp_id_entry' and x not in 'employment_status_entry'):
                        if self.view_frame.children[x].widgetName == "ttk::combobox" and state == 'normal':
                            self.controller.frames['emp_page'].view_frame.children[x]['state'] = 'readonly'
                        else:
                            self.controller.frames['emp_page'].view_frame.children[x]['state'] = state
                        if self.mode == 'add employee':
                            if ('entry') in x:
                                self.controller.frames['emp_page'].view_frame.children[x].delete(
                                    0, END)
                elif self.controller.user.permission == 'employee':
                    if x in ('personal_phone_entry', 'personal_email_entry', 'address_entry', 'city_entry', 'state_entry', 'zip_entry', 'state_entry'):
                        self.controller.frames['emp_page'].view_frame.children[x]['state'] = state
            self.controller.show_frame("emp_page")

        elif mode == 'cancel':
            self.emp_page_entries(self.employee_selected, 'cancel')
            self.classification_clicked.set(
                str(self.employee_selected.classification))
            self.payment_method_clicked.set(
                str(self.employee_selected.pay_method))
            self.permission_level_clicked.set(
                self.employee_selected.permission)

    def emp_page_entries(self, employee, mode=None):
        # changes parser mode so it can initilize each individual field for new employee
        self.mode = mode
        self.row_shift = 0

        if mode == 'select':

            self.backBtn['text'] = 'Back'
            self.submitBtn.grid_forget()
            self.editEmp.grid(column=0, row=1)

        def remove_highlight(event):
            event.widget['highlightthickness'] = 0
            event.widget['fg'] = 'black'
            if event.widget._name in ('start_date_entry', 'end_date_entry', 'dob_entry'):
                if event.widget.get() == 'MM/DD/YYYY':
                    event.widget.delete(0, END)

        def date_hasVal(event):
            if not event.widget.get():
                event.widget['fg'] = 'grey'
                event.widget.insert(0, 'MM/DD/YYYY')

        self.employee_selected = employee

        if self.controller.user.permission == 'admin':
            self.backBtn.grid(column=0, row=2)
        else:
            self.backBtn.grid_forget()

        var = StringVar()
        var.set('None')
        emp_id = StringVar(
            self.view_frame, value=employee.id, name='emi_id_var')
        first_name = StringVar(
            self.view_frame, value=employee.first_name, name='first_name')
        last_name = StringVar(
            self.view_frame, value=employee.last_name, name='last_name_var')
        address = StringVar(
            self.view_frame, value=employee.address, name='address_var')
        city = StringVar(self.view_frame, value=employee.city, name='city_var')
        zipcode = StringVar(
            self.view_frame, value=employee.zip, name='zipcode_var')
        ssn = StringVar(self.view_frame, value=employee.ssn, name='ssn_var')
        start_date = StringVar(
            self.view_frame, value=employee.start_date, name='start_date_var')
        if not start_date.get():
            start_date.set('MM/DD/YYYY')
        end_date = StringVar(
            self.view_frame, value=employee.end_date, name='end_date_var')
        if not end_date.get():
            end_date.set('MM/DD/YYYY')
        dob = StringVar(self.view_frame,
                        value=employee.birth_date, name='dob_var')
        if not dob.get():
            dob.set('MM/DD/YYYY')
        job_title = StringVar(
            self.view_frame, value=employee.title, name='job_title_var')
        job_dept = StringVar(
            self.view_frame, value=employee.dept, name='job_dept_var')
        phone = StringVar(
            self.view_frame, value=employee.phone, name='phone_var')
        email = StringVar(
            self.view_frame, value=employee.email, name='email_var')
        password = StringVar(
            self.view_frame, value=employee.password, name='password_var')
        job_status = StringVar(
            self.view_frame, value=employee.job_status, name='job_status_var')
        routingNum = StringVar(self.view_frame, value='',
                               name='routingNum_var')
        accountNum = StringVar(self.view_frame, value='',
                               name='accountNum_var')

        if str(employee.pay_method) == 'Direct Deposit':
            routingNum.set(employee.pay_method.route_num)
            accountNum.set(employee.pay_method.account_num)
        else:
            routingNum.set('None')
            accountNum.set('None')

        try:
            hourly_rate = StringVar(self.view_frame, name='hourly_rate_val')
            hourly_rate.set(employee.classification.hourly_rate)
        except AttributeError:
            pass
        try:
            salary = StringVar(self.view_frame, name='salary_val')
            salary.set(employee.classification.salary)
        except AttributeError:
            pass
        try:
            commission = StringVar(self.view_frame, name='commission_val')
            commission.set(employee.classification.commission_rate)
        except AttributeError:
            pass

        self.emp_ID_label = tk.Label(
            self.view_frame, name='emp_id_label', justify='right', text="Employee ID:", font=('Arial', 10))
        self.emp_ID_entry = tk.Entry(self.view_frame, name='emp_id_entry', font=(
            'Arial', 10), state=DISABLED, textvariable=emp_id)
        self.first_name_label = tk.Label(
            self.view_frame, name='first_name_label', justify='right', text="First Name:", font=('Arial', 10))
        self.first_name_entry = tk.Entry(self.view_frame, name='first_name_entry', font=(
            'Arial', 10), state=DISABLED, textvariable=first_name)
        self.first_name_entry.bind('<FocusIn>', remove_highlight)

        self.last_name_label = tk.Label(
            self.view_frame, name='last_name_label', justify='right', text="Last Name:", font=('Arial', 10))
        self.last_name_entry = tk.Entry(self.view_frame, name='last_name_entry', font=(
            'Arial', 10), state=DISABLED, textvariable=last_name)
        self.last_name_entry.bind('<FocusIn>', remove_highlight)

        self.address_label = tk.Label(
            self.view_frame, name='address_label', justify='right', text="Address:", font=('Arial', 10))
        self.address_entry = tk.Entry(self.view_frame, name='address_entry', font=(
            'Arial', 10), state=DISABLED, textvariable=address)
        self.address_entry.bind('<FocusIn>', remove_highlight)

        self.city_label = tk.Label(
            self.view_frame, name='city_label', justify='right', text="City:", font=('Arial', 10))
        self.city_entry = tk.Entry(self.view_frame, name='city_entry', font=(
            'Arial', 10), state=DISABLED, textvariable=city)
        self.city_entry.bind('<FocusIn>', remove_highlight)

        self.state_label = tk.Label(
            self.view_frame, name='state_label', justify='right', text="State:", font=('Arial', 10))
        self.zip_label = tk.Label(
            self.view_frame, name='zip_label', justify='right', text="Zip:", font=('Arial', 10))
        self.zip_entry = tk.Entry(self.view_frame, name='zip_entry', font=(
            'Arial', 10), state=DISABLED, textvariable=zipcode)
        self.zip_entry.bind('<FocusIn>', remove_highlight)

        self.classification_label = tk.Label(
            self.view_frame, name='classification_label', justify='right', text="Classification:", font=('Arial', 10))

        self.hourly_label = tk.Label(
            self.view_frame, name='hourly_label', text="Hourly Rate:", font=('Arial', 10))
        self.hourly_entry = tk.Entry(self.view_frame, name='hourly_entry',
                                     state=DISABLED, textvariable=hourly_rate, font=('Arial', 10))
        self.hourly_entry.bind('<FocusIn>', remove_highlight)

        self.salary_label = tk.Label(
            self.view_frame, name='salary_label', text="Salary:", font=('Arial', 10))
        self.salary_entry = tk.Entry(
            self.view_frame, name='salary_entry', state=DISABLED, textvariable=salary, font=('Arial', 10))
        self.salary_entry.bind('<FocusIn>', remove_highlight)

        self.commission_label = tk.Label(
            self.view_frame, name='commission_label', text="Commission Rate:", font=('Arial', 10))
        self.commission_entry = tk.Entry(
            self.view_frame, name='commission_entry', state=DISABLED, textvariable=commission, font=('Arial', 10))
        self.commission_entry.bind('<FocusIn>', remove_highlight)

        self.personal_phone_label = tk.Label(
            self.view_frame, name='personal_phone_label', justify='right', text="Personal Phone:", font=('Arial', 10))
        self.personal_phone_entry = tk.Entry(self.view_frame, name='personal_phone_entry', font=(
            'Arial', 10), state=DISABLED, textvariable=phone)
        self.personal_phone_entry.bind('<FocusIn>', remove_highlight)

        self.personal_email_label = tk.Label(
            self.view_frame, name='personal_email_label', justify='right', text="Personal Email:", font=('Arial', 10))
        self.personal_email_entry = tk.Entry(self.view_frame, name='personal_email_entry', font=(
            'Arial', 10), state=DISABLED, textvariable=email)
        self.personal_email_entry.bind('<FocusIn>', remove_highlight)

        self.DOB_label = tk.Label(self.view_frame, name='dob_label',
                                  justify='right', text="Date of Birth:", font=('Arial', 10))
        self.DOB_entry = tk.Entry(self.view_frame, name='dob_entry', font=(
            'Arial', 10), state=DISABLED, textvariable=dob)
        if dob.get() == 'MM/DD/YYYY':
            self.DOB_entry.config(fg='grey')
        self.DOB_entry.bind('<FocusIn>', remove_highlight)
        self.DOB_entry.bind('<FocusOut>', date_hasVal)

        self.SSN_label = tk.Label(
            self.view_frame, name='ssn_label', justify='right', text="SSN:", font=('Arial', 10))
        self.SSN_entry = tk.Entry(self.view_frame, name='ssn_entry', font=(
            'Arial', 10), state=DISABLED, textvariable=ssn)
        self.SSN_entry.bind('<FocusIn>', remove_highlight)

        self.routing_number_label = tk.Label(
            self.view_frame, name='routing_number_label', justify='right', text="Routing Number:", font=('Arial', 10))
        self.routing_number_entry = tk.Entry(self.view_frame, name='routing_number_entry', font=(
            'Arial', 10), state=DISABLED, textvariable=routingNum)
        self.routing_number_entry.bind('<FocusIn>', remove_highlight)

        self.account_number_label = tk.Label(
            self.view_frame, name='account_number_label', justify='right', text="Account Number:", font=('Arial', 10))
        self.account_number_entry = tk.Entry(self.view_frame, name='account_number_entry', font=(
            'Arial', 10), state=DISABLED, textvariable=accountNum)
        self.account_number_entry.bind('<FocusIn>', remove_highlight)

        self.payment_method_label = tk.Label(
            self.view_frame, name='payment_method_label', justify='right', text="Payment Method:", font=('Arial', 10))

        self.job_title_label = tk.Label(
            self.view_frame, name='job_title_label', justify='right', text="Job Title:", font=('Arial', 10))
        self.job_title_entry = tk.Entry(self.view_frame, name='job_title_entry', font=(
            'Arial', 10), state=DISABLED, textvariable=job_title)
        self.job_title_entry.bind('<FocusIn>', remove_highlight)

        self.job_department_label = tk.Label(
            self.view_frame, name='job_department_label', justify='right', text="Department:", font=('Arial', 10))
        self.job_department_entry = tk.Entry(self.view_frame, name='job_department_entry', font=(
            'Arial', 10), state=DISABLED, textvariable=job_dept)
        self.job_department_entry.bind('<FocusIn>', remove_highlight)

        self.start_date_label = tk.Label(
            self.view_frame, name='start_date_label', justify='right', text="Start Date:", font=('Arial', 10))
        self.start_date_entry = tk.Entry(self.view_frame, name='start_date_entry', font=(
            'Arial', 10), state=DISABLED, textvariable=start_date)
        if start_date.get() == 'MM/DD/YYYY':
            self.start_date_entry.config(fg='grey')
        self.start_date_entry.bind('<FocusIn>', remove_highlight)
        self.start_date_entry.bind('<FocusOut>', date_hasVal)

        self.end_date_label = tk.Label(
            self.view_frame, name='end_date_label', justify='right', text="End Date:", font=('Arial', 10))
        self.end_date_entry = tk.Entry(self.view_frame, name='end_date_entry', font=(
            'Arial', 10), state=DISABLED, textvariable=end_date)
        if end_date.get() == 'MM/DD/YYYY':
            self.end_date_entry.config(fg='grey')
        self.end_date_entry.bind('<FocusIn>', remove_highlight)
        self.end_date_entry.bind('<FocusOut>', date_hasVal)

        self.employment_status_label = tk.Label(
            self.view_frame, name='employment_status_label', justify='right', text="Employment Status:", font=('Arial', 10))
        self.employment_status_entry = tk.Entry(self.view_frame, name='employment_status_entry', font=(
            'Arial', 10), state=DISABLED, textvariable=job_status)
        self.password_label = tk.Label(
            self.view_frame, name='password_label', justify='right', text="Password:", font=('Arial', 10))
        self.password_entry = tk.Entry(self.view_frame, name='password_entry', font=(
            'Arial', 10), state=DISABLED, textvariable=password)
        self.password_entry.bind('<FocusIn>', remove_highlight)

        self.permission_level_label = tk.Label(
            self.view_frame, name='permission_level_label', justify='right', text="Permission Level:", font=('Arial', 10))

        def updateCol3():
            self.job_title_label.grid(
                column=3, row=4+self.row_shift, sticky='E', padx=15, pady=7)
            self.job_department_label.grid(
                column=3, row=5+self.row_shift, sticky='E', padx=15, pady=7)
            self.start_date_label.grid(
                column=3, row=6+self.row_shift, sticky='E', padx=15, pady=7)
            self.end_date_label.grid(
                column=3, row=7+self.row_shift, sticky='E', padx=15, pady=7)
            self.employment_status_label.grid(
                column=3, row=8+self.row_shift, sticky='E', padx=15, pady=7)
            self.job_title_entry.grid(column=4, row=4+self.row_shift)
            self.job_department_entry.grid(column=4, row=5+self.row_shift)
            self.start_date_entry.grid(column=4, row=6+self.row_shift)
            self.end_date_entry.grid(column=4, row=7+self.row_shift)
            self.employment_status_entry.grid(column=4, row=8+self.row_shift)

        def classification_dropdown_func(*args):
            print(
                f"the variable has changed to '{self.classification_clicked.get()}'")
            # Show pay amounts, based on classification type:
            if self.classification_clicked.get() == "Hourly":
                self.hourly_label.grid(
                    column=1, row=11, sticky='E', padx=15, pady=7)
                self.hourly_entry.grid(column=2, row=11)
                self.commission_label.grid_forget()
                self.commission_entry.grid_forget()
                self.salary_label.grid_forget()
                self.salary_label.grid_forget()

            # Salary
            elif self.classification_clicked.get() == "Salary":
                self.salary_label.grid(
                    column=1, row=11, sticky='E', padx=15, pady=7)
                self.salary_entry.grid(column=2, row=11)
                self.hourly_label.grid_forget()
                self.hourly_entry.grid_forget()
                self.commission_label.grid_forget()
                self.commission_entry.grid_forget()
            # Commission
            elif self.classification_clicked.get() == "Commissioned":
                self.salary_label.grid(
                    column=1, row=11, sticky='E', padx=15, pady=7)
                self.salary_entry.grid(column=2, row=11)
                self.commission_label.grid(
                    column=1, row=12, sticky='E', padx=15, pady=7)
                self.commission_entry.grid(column=2, row=12)
                self.hourly_label.grid_forget()
                self.hourly_entry.grid_forget()

        def pay_method_dropdown_func(*args):
            if self.payment_method_clicked.get() == 'Mail':
                self.row_shift = 0
                self.routing_number_label.grid_forget()
                self.account_number_label.grid_forget()
                self.routing_number_entry.grid_forget()
                self.account_number_entry.grid_forget()
            elif self.payment_method_clicked.get() == 'Direct Deposit':
                self.row_shift = 2
                self.account_number_label.grid(
                    column=3, row=4, sticky='E', padx=15, pady=7)
                self.routing_number_label.grid(
                    column=3, row=5, sticky='E', padx=15, pady=7)
                self.account_number_entry.grid(column=4, row=4)
                self.routing_number_entry.grid(column=4, row=5)
            updateCol3()

        if mode != 'cancel':
            stateList = [
                '- Select -', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI',
                'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI',
                'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC',
                'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT',
                'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
            ]

            self.state_clicked = StringVar(
                self.view_frame, value=employee.state, name='state_clicked_val')
            self.state_dropdown = mycombobox(
                self.view_frame, value=stateList, state=DISABLED)
            if employee.state:
                self.state_dropdown.set(employee.state)
            else: 
                self.state_dropdown.set('- Select -')
            self.state_dropdown.grid(column=2,row=6)

            classList = ["- Select -", "Hourly", "Salary", "Commissioned"]
            self.classification_clicked = StringVar(
                self.view_frame, value='', name='classification_clicked_val')
            self.classification_clicked.trace(
                'w', classification_dropdown_func)
            
            if str(employee.classification):       
                self.classification_clicked.set(str(employee.classification))
            else:
                self.classification_clicked.set('- Select -')
                
            self.classification_dropdown = mycombobox(self.view_frame, value=
                classList, textvariable=self.classification_clicked)
            self.classification_dropdown.grid(column=2, row=10)

            paymentMethodList = ["- Select -", "Direct Deposit", "Mail"]
            self.payment_method_clicked = StringVar(
                self.view_frame, value='', name='payment_method_clicked_val')
            self.payment_method_clicked.trace('w', pay_method_dropdown_func)
            
            if str(employee.pay_method):
                self.payment_method_clicked.set(str(employee.pay_method))
            else:
                self.classification_clicked.set('- Select -')
                
            self.payment_method_dropdown = mycombobox(
                self.view_frame, textvariable=self.payment_method_clicked, value=paymentMethodList)
            self.payment_method_dropdown.grid(column=4, row=3)

            permissionList = ["- Select -", "employee", "admin"]
            self.permission_level_clicked = StringVar(
                self.view_frame, value='', name='permission_level_clicked_val')
            
            if employee.permission:
                self.permission_level_clicked.set(employee.permission)
            else:
                self.classification_clicked.set('- Select -')
                
            self.permission_level_dropdown = mycombobox(
                self.view_frame, textvariable=self.permission_level_clicked, value=permissionList)
            self.permission_level_dropdown.grid(column=6, row=2)

        self.state_dropdown.configure(state=DISABLED)
        self.classification_dropdown.configure(state=DISABLED)
        self.payment_method_dropdown.configure(state=DISABLED)
        self.permission_level_dropdown.configure(state=DISABLED)

        self.emp_ID_label.grid(column=1, row=1, sticky='E', padx=15, pady=7)
        self.first_name_label.grid(
            column=1, row=2, sticky='E', padx=15, pady=7)
        self.last_name_label.grid(column=1, row=3, sticky='E', padx=15, pady=7)
        self.address_label.grid(column=1, row=4, sticky='E', padx=15, pady=7)
        self.city_label.grid(column=1, row=5, sticky='E', padx=15, pady=7)
        self.state_label.grid(column=1, row=6, sticky='E', padx=15, pady=7)
        self.zip_label.grid(column=1, row=7, sticky='E', padx=15, pady=7)
        self.personal_phone_label.grid(
            column=1, row=8, sticky='E', padx=15, pady=7)
        self.personal_email_label.grid(
            column=1, row=9, sticky='E', padx=15, pady=7)
        self.classification_label.grid(
            column=1, row=10, sticky='E', padx=15, pady=7)

        self.DOB_label.grid(column=3, row=1, sticky='E', padx=15, pady=7)
        self.SSN_label.grid(column=3, row=2, sticky='E', padx=15, pady=7)
        self.payment_method_label.grid(
            column=3, row=3, sticky='E', padx=15, pady=7)

        self.password_label.grid(column=5, row=1, sticky='E', padx=15, pady=7)
        self.permission_level_label.grid(
            column=5, row=2, sticky='E', padx=15, pady=7)

        self.emp_ID_entry.grid(column=2, row=1)
        self.first_name_entry.grid(column=2, row=2)
        self.last_name_entry.grid(column=2, row=3)
        self.address_entry.grid(column=2, row=4)
        self.city_entry.grid(column=2, row=5)
        self.zip_entry.grid(column=2, row=7)
        self.personal_phone_entry.grid(column=2, row=8)
        self.personal_email_entry.grid(column=2, row=9)

        self.DOB_entry.grid(column=4, row=1)
        self.SSN_entry.grid(column=4, row=2)

        self.password_entry.grid(column=6, row=1)


class admin_page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Admin Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        self.offsetx = 0
        self.filterVar = 'Last Name'
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('Treeview', rowheight=30)
        
        def remove_init_text(event):
            if event.widget.get() == "Search by Last Name" or event.widget.get() == "Search by ID":
                event.widget['fg'] = 'black'
                event.widget.delete(0, END)

        def set_filterVar(*args):
            if self.searchFilterClick.get() != 'Filter':
                self.filterVar = self.searchFilterClick.get()
                self.search_var.set("Search by {0}".format(self.filterVar))
                
        def searchFocusOut(event):
            if not self.search_var.get():
                event.widget['fg'] = 'grey'
                self.search_var.set("Search by {0}".format(self.filterVar))
        
        self.btn_frame = LabelFrame(self)
        self.btn_frame.pack(side='bottom', fill=BOTH)
        self.offsetx = -35
        
        self.searchEmp_Btn = Button(self, text="Search", font=(
            'Arial', 10), command=lambda: self.search_for_emp()).place(x=710 + self.offsetx, y=420)
        
        
        self.search_var = StringVar()
        self.search_var.set("Search by {0}".format(self.filterVar))
        self.searchEmp_entry = Entry(self, textvariable = self.search_var, font=('Arial', 10), fg='grey')
        self.searchEmp_entry.bind('<FocusIn>', remove_init_text)
        self.searchEmp_entry.bind('<FocusOut>', searchFocusOut)
        self.searchEmp_entry.place(x=550 + self.offsetx, y=420)
        self.search_var.trace('w', self.search_for_emp)
        
        
        self.filters = ('Last Name','ID')
        self.searchFilterClick = StringVar()
        self.searchFilterClick.trace('w', set_filterVar)
        self.searchFilterClick.set('Filter')
        self.searchFilter_dropdown = OptionMenu(self, self.searchFilterClick, *self.filters)
        self.searchFilter_dropdown.place(x=770 + self.offsetx, y=420)
        
        self.addEmpBtn = tk.Button(
            self, text="Add New Employee", command=lambda: self.add_emp()).place(x=550, y=460)
        
        self.columns_list = ("emp_ip_column", "first_name_column", "last_name_column",
                             "phone_number_column", "email_column", "start_date_column",
                             "end_date_column", "classification_column", "title_column",
                             "deptartment_column")

        self.emp_tree = ttk.Treeview(
            self, columns=self.columns_list, show='headings')

        for col in self.columns_list:
            self.emp_tree.column(col, width=120)

        for col in self.columns_list:
            self.emp_tree.heading(col,
                                  command=lambda c=col: self.treeview_sort_column(
                                      self.emp_tree, c, False)
                                  )
            # create heading
        # my_tree.heading("#0", text="Label", anchor=W) #text is optional
        self.emp_tree.heading("emp_ip_column", text="Employee ID", anchor=W)
        self.emp_tree.heading("first_name_column", text="First Name", anchor=W)
        self.emp_tree.heading("last_name_column", text="Last Name", anchor=W)
        self.emp_tree.heading("phone_number_column",
                              text="Phone Number", anchor=W)
        self.emp_tree.heading("email_column", text="Email", anchor=W)
        self.emp_tree.heading("start_date_column", text="Start Date", anchor=W)
        self.emp_tree.heading("end_date_column", text="End Date", anchor=W)
        self.emp_tree.heading("classification_column",
                              text="Classification", anchor=W)
        self.emp_tree.heading("title_column", text="Title", anchor=W)
        self.emp_tree.heading("deptartment_column",
                              text="Department", anchor=W)

        self.emp_tree.pack(pady=20)
        self.emp_tree_init()
        self.emp_tree.bind("<Double 1>", self.selected_employee)
        self.emp_tree.pack()


    def search_for_emp(self, *args):
        self.lookup_record = self.searchEmp_entry.get()
        if self.lookup_record == 'Search by Last Name' or self.lookup_record == 'Search by ID':
            return
        #take the string currently in the widget, all the way up to the last character
        if self.filterVar == 'ID':
            if not self.lookup_record.isdigit() and self.lookup_record:
                self.searchEmp_entry.delete(0,END)
                self.searchEmp_entry.insert(0,self.lookup_record[:-1])
                return
        elif self.filterVar == 'Last Name':
            if self.lookup_record.isdigit() and self.lookup_record:
                self.searchEmp_entry.delete(0,END)
                self.searchEmp_entry.insert(0,self.lookup_record[:-1])
                return
            
        ItemsInTreeView = self.emp_tree.get_children()
        self.filteredOut = {}
        
        # Clear the Treeview
        for record in self.emp_tree.get_children():
            self.emp_tree.delete(record)
            
        for emp in EmpDat.emp_list:
            indexDict = {
                'ID': emp.id,
                'Last Name': emp.last_name.lower()
            }
            if self.lookup_record.lower() in str(indexDict[self.filterVar])[0:len(self.lookup_record)]:
                self.emp_tree.insert('', END, values=(emp.id, emp.first_name,
                                                      emp.last_name, emp.phone, emp.email,
                                                      emp.start_date, emp.end_date,
                                                      str(emp.classification), emp.title, emp.dept))
            
        
        # for eachItem in ItemsInTreeView:
        #     if search not in self.emp_tree.item(eachItem)['values'][indexDict[self.filterVar]][0:len(search)].lower():
        #         # search_var = self.emp_tree.item(eachItem)['values']
        #         # self.emp_tree.delete(eachItem)
        #         # self.emp_tree.insert("",0,values=search_var)
        #         self.filteredOut[eachItem] = self.emp_tree.item(eachItem)['values']
        #         self.emp_tree.delete(eachItem)
        #     else:
        #         for key, value in self.filteredOut.items():   
        #             if search in value[indexDict[self.filterVar]][0:len(search)].lower():
        #                 self.emp_tree.insert("",0,values=self.filteredOut[eachItem])
    
    def add_emp(self):
        max_id = 0
        for emp in EmpDat.emp_list + EmpDat.archived_list:
            if emp.id > max_id:
                max_id = emp.id
        new_id = max_id + 1

        new_id = max_id + 1
        EmpDat.archived_list
        temp_emp = Employee(new_id, '', '', 'MM/DD/YYYY', '', '', '', '', '')
        self.controller.frames['emp_page'].emp_page_entries(
            temp_emp, 'add employee')
        self.controller.frames['emp_page'].add_emp_innit()

    def treeview_sort_column(self, treeview, col, reverse):
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
            command=lambda c=col: self.treeview_sort_column(
                treeview, c, not reverse)
        )

    # Iterate through all employees to list them out.

    # initilizes employee tree, made function so it can be called later when needed for updates.
    def emp_tree_init(self):
        global COUNT
        COUNT = 0
        for emp in EmpDat.emp_list:
            if COUNT % 2 == 0:
                self.emp_tree.get_children()
                self.emp_tree.insert('', END, values=(emp.id, emp.first_name,
                                                      emp.last_name, emp.phone, emp.email,
                                                      emp.start_date, emp.end_date,
                                                      str(emp.classification), emp.title, emp.dept),
                                     tags=("evenrows",))
            else:
                self.emp_tree.insert('', END, values=(emp.id, emp.first_name,
                                                      emp.last_name, emp.phone, emp.email,
                                                      emp.start_date, emp.end_date,
                                                      str(emp.classification), emp.title,
                                                      emp.dept), tags=("oddrows",))
            COUNT += 1

    #########
    # Binds #
    #########

    def selected_employee(self, event):
        """Brings up an employee's information in a separate GUI window.
        Intended to be called with a double-click event handler, so that
        an employee's info shows up when you click on them.
        """
        # Bring up employee information after double-click
        for selected_emp_idx in self.emp_tree.selection():
            emp_data = self.emp_tree.item(selected_emp_idx)
            emp_id = emp_data["values"][0]
            emp = find_employee_by_id(emp_id, EmpDat.emp_list)
        self.controller.frames['emp_page'].emp_page_entries(emp, 'select')
        self.controller.show_frame("emp_page")


class add_employee_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="New Employee", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        self.sumbitBnt = tk.Button(self, text="Submit")
        self.sumbitBnt.pack()
