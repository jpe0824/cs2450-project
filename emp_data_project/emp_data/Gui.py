

import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import font  as tkfont

testDataBase = {
            '999999': ['password', 'admin'],
            '123456': ['password', 'employee']
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
        container.grid_rowconfigure(0, weight=1, minsize = 500)
        container.grid_columnconfigure(0, weight=1, minsize = 800)
        self.frames = {}
        for F in (LoginPage, home_page, payroll_info_page, profile_page, employee_directory_page, add_employee_page):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("LoginPage")
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.employee = None

        username = StringVar()
        password = StringVar()
        
        
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
                self.focus() #removes focus on data fields
                if testDataBase[self.employee][1] != 'admin':
                    self.controller.frames['home_page'].addEmpBtn.pack_forget()
                elif testDataBase[self.employee][1] == 'admin':
                    self.controller.frames['home_page'].addEmpBtn.pack()
                self.controller.show_frame("home_page")
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

        self.payrollBtn = tk.Button(self, text="Payroll Info",
                               command= lambda: controller.show_frame("payroll_info_page"))
        self.payrollBtn.pack()

        self.profileBtn = tk.Button(self, text="Profile Page",
                               command= lambda: controller.show_frame("profile_page"))
        self.profileBtn.pack()

        self.employeeDirBtn = tk.Button(self, text="Employee Directory",
                               command= lambda: controller.show_frame("employee_directory_page"))
        self.employeeDirBtn.pack()

        self.addEmpBtn = tk.Button(self, text="Add New Employee",
                               command= lambda: controller.show_frame("add_employee_page"))
        self.addEmpBtn.pack()

        self.logoutBtn = tk.Button(self, text="Logout",
                               command= lambda: controller.show_frame("LoginPage"))
        self.logoutBtn.pack()
        self.logoutBtn.place(x=750,y=0)





class payroll_info_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Payroll Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Home",
                               command= lambda: controller.show_frame("home_page"))
        button.pack()

        logoutBtn = tk.Button(self, text="Logout",
                               command= lambda: controller.show_frame("LoginPage"))
        logoutBtn.pack()
        logoutBtn.place(x=750,y=0)

class profile_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Profile Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Home",
                               command= lambda: controller.show_frame("home_page"))
        button.pack()
        logoutBtn = tk.Button(self, text="Logout",
                               command= lambda: controller.show_frame("LoginPage"))
        logoutBtn.pack()
        logoutBtn.place(x=750,y=0)

class employee_directory_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Employee Directory Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Home",
                               command= lambda: controller.show_frame("home_page"))
        button.pack()
        logoutBtn = tk.Button(self, text="Logout",
                               command= lambda: controller.show_frame("LoginPage"))
        logoutBtn.pack()
        logoutBtn.place(x=750,y=0)

class add_employee_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="New Employee", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Cancel",
                               command= lambda: controller.show_frame("home_page"))
        button.pack()
        sumbitBnt = tk.Button(self, text="Submit")
        sumbitBnt.pack()
        logoutBtn = tk.Button(self, text="Logout",
                               command= lambda: controller.show_frame("LoginPage"))
        logoutBtn.pack()
        logoutBtn.place(x=750,y=0)





def main():
    app = EmpApp()
    app.mainloop()


if __name__ == '__main__':
    main()