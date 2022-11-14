

import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import font  as tkfont


#test database will contain a key (employee id) with a value containing employee password and privileges. 
testDataBase = {
            '999999': ['password', 'admin'],
            '123456': ['password', 'employee'],
            '0': ['0', 'admin'],
            '1': ['1', 'employee']
            }


class EmpApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
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
        for F in (LoginPage, home_page, view_page, employee_directory_page, add_employee_page):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("LoginPage")
        
    def validateLogin(self):
        pass
    
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        
        if page_name != 'LoginPage':
            frame.logoutBtn = tk.Button(frame, text="Logout", command= lambda: self.show_frame("LoginPage"))
            frame.logoutBtn.pack()
            frame.logoutBtn.place(x=950,y=0)
        if page_name != 'LoginPage' and page_name != 'add_employee_page' and page_name != 'home_page':
            frame.home = tk.Button(frame, text="Home", command= lambda: self.show_frame("home_page"))
            frame.home.pack()
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
                    self.controller.frames['home_page'].addEmpBtn.pack()          # relitialize home page to include 'Add Employee Button' when user has admin privilege.
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
        label = tk.Label(self, text="Home Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.emp_view = tk.Button(self, text="Employee Info",
                               command= lambda: controller.show_frame("view_page"))
        self.emp_view.pack()

        self.employeeDirBtn = tk.Button(self, text="Employee Directory",
                               command= lambda: controller.show_frame("employee_directory_page"))
        self.employeeDirBtn.pack()

        self.addEmpBtn = tk.Button(self, text="Add New Employee",
                               command= lambda: controller.show_frame("add_employee_page"))
        self.addEmpBtn.pack()


class view_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        label = tk.Label(self, text="Viewing Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        

        self.emp_ID_label = tk.Label(self, text="Employee ID:", font=('Arial', 10))
        self.emp_ID_label.pack()
        self.emp_ID_entry = tk.Entry(self, font=('Arial', 10))
        self.emp_ID_entry.pack()
        self.first_name_label = tk.Label(self, text="First Name:", font=('Arial', 10))
        self.first_name_label.pack()
        self.first_name_entry = tk.Entry(self, font=('Arial', 10))
        self.first_name_entry.pack()
        self.last_name_label = tk.Label(self, text="Last Name:", font=('Arial', 10))
        self.last_name_label.pack()
        self.last_name_entry = tk.Entry(self, font=('Arial', 10))
        self.last_name_entry.pack()
        self.address_label = tk.Label(self, text="Address:", font=('Arial', 10))
        self.address_label.pack()
        self.address_entry = tk.Entry(self, font=('Arial', 10))
        self.address_entry.pack()
        self.city_label = tk.Label(self, text="City:", font=('Arial', 10))
        self.city_label.pack()
        self.city_entry = tk.Entry(self, font=('Arial', 10))
        self.city_entry.pack()
        self.state_label = tk.Label(self, text="State:", font=('Arial', 10))
        self.state_label.pack()
        self.state_entry = tk.Entry(self, font=('Arial', 10))
        self.state_entry.pack()
        self.zip_label = tk.Label(self, text="Zip:", font=('Arial', 10))
        self.zip_label.pack()
        self.zip_entry = tk.Entry(self, font=('Arial', 10))
        self.zip_entry.pack()
        
        self.classification_label = tk.Label(self, text="Classification:", font=('Arial', 10))
        self.classification_label.pack()
        
        clicked = StringVar()
        clicked.set("- Select -")
        self.classification_dropdown = OptionMenu(self, clicked, "- Select -", "Salaried", "Commission", "Hourly")
        self.classification_dropdown.pack()
        
        
        self.office_phone_label = tk.Label(self, text="Office Phone:", font=('Arial', 10))
        self.office_phone_label.pack()
        self.office_phone_entry = tk.Entry(self, font=('Arial', 10))
        self.office_phone_entry.pack()
        self.office_email_label = tk.Label(self, text="Office Email:", font=('Arial', 10))
        self.office_email_label.pack()
        self.office_email_entry = tk.Entry(self, font=('Arial', 10))
        self.office_email_entry.pack()
        self.personal_phone_label = tk.Label(self, text="Personal Phone:", font=('Arial', 10))
        self.personal_phone_label.pack()
        self.personal_phone_entry = tk.Entry(self, font=('Arial', 10))
        self.personal_phone_entry.pack()
        self.personal_email_label = tk.Label(self, text="Personal Email:", font=('Arial', 10))
        self.personal_email_label.pack()
        self.personal_email_entry = tk.Entry(self, font=('Arial', 10))
        self.personal_email_entry.pack()
        self.DOB_label = tk.Label(self, text="Date of Birth:", font=('Arial', 10))
        self.DOB_label.pack()
        self.DOB_entry = tk.Entry(self, font=('Arial', 10))
        self.DOB_entry.pack()
        
        
        self.SSN_label = tk.Label(self, text="SSN:", font=('Arial', 10))
        self.SSN_label.pack()
        self.SSN_entry = tk.Entry(self, font=('Arial', 10))
        self.SSN_entry.pack()  
        self.routing_number_label = tk.Label(self, text="Routing Number:", font=('Arial', 10))
        self.routing_number_label.pack()
        self.routing_number_entry = tk.Entry(self, font=('Arial', 10))
        self.routing_number_entry.pack()
        self.account_number_label = tk.Label(self, text="Account Number:", font=('Arial', 10))
        self.account_number_label.pack()
        self.account_number_entry = tk.Entry(self, font=('Arial', 10))
        self.account_number_entry.pack()
        self.payment_method_label = tk.Label(self, text="Payment Method:", font=('Arial', 10))
        self.payment_method_label.pack()
        
        
        payment_method_clicked = StringVar()
        payment_method_clicked.set("- Select -")
        self.payment_method_dropdown = OptionMenu(self, payment_method_clicked, "- Select -", "Direct Deposit", "Mail")
        self.payment_method_dropdown.pack()
        
        
        self.permission_level_label = tk.Label(self, text="Permission Level:", font=('Arial', 10))
        self.permission_level_label.pack(pady=20)
        self.permission_level_entry = tk.Entry(self, font=('Arial', 10))
        self.permission_level_entry.pack(pady=20)
        self.job_title_label = tk.Label(self, text="Job Title:", font=('Arial', 10))
        self.job_title_label.pack(pady=20)
        self.job_title_entry = tk.Entry(self, font=('Arial', 10))
        self.job_title_entry.pack(pady=20)
        self.job_department_label = tk.Label(self, text="Department:", font=('Arial', 10))
        self.job_department_label.pack(pady=20)
        self.job_department_entry = tk.Entry(self, font=('Arial', 10))
        self.job_department_entry.pack(pady=20)
        self.start_date_label = tk.Label(self, text="Start Date:", font=('Arial', 10))
        self.start_date_label.pack(pady=20)
        self.start_date_entry = tk.Entry(self, font=('Arial', 10))
        self.start_date_entry.pack(pady=20)
        self.end_date_label = tk.Label(self, text="End Date:", font=('Arial', 10))
        self.end_date_label.pack(pady=20)
        self.end_date_entry = tk.Entry(self, font=('Arial', 10))
        self.end_date_entry.pack(pady=20)
        self.employment_status_label = tk.Label(self, text="Employment Status:", font=('Arial', 10))
        self.employment_status_label.pack(pady=20)
        self.employment_status_entry = tk.Entry(self, font=('Arial', 10))
        self.employment_status_entry.pack(pady=20)
        self.password_label = tk.Label(self, text="Password", font=('Arial', 10))
        self.password_label.pack(pady=20)
        self.password_entry = tk.Entry(self, font=('Arial', 10))
        self.password_entry.pack(pady=20)
        
        
        self.emp_ID_label.place(x=50, y=50)
        self.first_name_label.place(x=50, y=85)
        self.last_name_label.place(x=50, y=120)
        self.address_label.place(x=50, y=155)
        self.city_label.place(x=50, y=190)
        self.state_label.place(x=50, y=225)
        self.zip_label.place(x=50, y=260)
        self.classification_label.place(x=50, y=295)
        self.office_phone_label.place(x=50, y=330)
        self.office_email_label.place(x=50, y=365)
        self.personal_phone_label.place(x=50, y=400)
        self.personal_email_label.place(x=50, y=435)
        
        
        self.DOB_label.place(x=400, y=50)
        self.SSN_label.place(x=400, y=85)
        self.routing_number_label.place(x=400, y=120)
        self.account_number_label.place(x=400, y=155)
        self.payment_method_label.place(x=400, y=190)
        self.permission_level_label.place(x=400, y=225+15)
        self.job_title_label.place(x=400, y=260+15)
        self.job_department_label.place(x=400, y=295+15)
        self.start_date_label.place(x=400, y=330+15)
        self.end_date_label.place(x=400, y=365+15)
        self.employment_status_label.place(x=400, y=400+15)
        self.password_label.place(x=400, y=435+15)
        
  
        self.emp_ID_entry.place(x=220, y=50)
        self.first_name_entry.place(x=220, y=85)
        self.last_name_entry.place(x=220, y=120)
        self.address_entry.place(x=220, y=155)
        self.city_entry.place(x=220, y=190)
        self.state_entry.place(x=220, y=225)
        self.zip_entry.place(x=220, y=260)
        self.classification_dropdown.place(x=220, y=295)
        self.office_phone_entry.place(x=220, y=330+15)        
        self.office_email_entry.place(x=220, y=365+15)        
        self.personal_phone_entry.place(x=220, y=400+15)
        self.personal_email_entry.place(x=220, y=435+15)
    
        
        self.DOB_entry.place(x=550, y=50)
        self.SSN_entry.place(x=550, y=85)
        self.routing_number_entry.place(x=550, y=120)
        self.account_number_entry.place(x=550, y=155)
        self.payment_method_dropdown.place(x=550, y=190)
        self.permission_level_entry.place(x=550, y=225+15)
        self.job_title_entry.place(x=550, y=260+15)
        self.job_department_entry.place(x=550, y=295+15)
        self.start_date_entry.place(x=550, y=330+15)
        self.end_date_entry.place(x=550, y=365+15)
        self.employment_status_entry.place(x=550, y=400+15)
        self.password_entry.place(x=550, y=435+15)

        

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


