#TODO create class for gui code

#from curses import window
#from ipaddress import collapse_addresses
import tkinter as tk

class Gui:
    def __init__(self):
        self.window = tk.Tk()
        self.screen_height = self.window.winfo_screenheight()
        self.screen_width = self.window.winfo_screenwidth()
        
#test
    def loginScreen():
        window = tk.Tk()
        window.title("Login form")
        window.geometry('340x440')
        #window.configure(bg='#333333')


        #creating widgets for login page
        login_label = tk.Label(self.window, text="Login")
        username_label = tk.Label(self.window, text="Username")
        username_entry = tk.Entry(self.window)
        password_entry = tk.Entry(self.window, show='*')
        password_label = tk.Label(self.window, text='Password')
        login_button = tk.Button(self.window, text='Login')

        # Positioning widgets on the screen
        login_label.grid(row=0, column=0, columnspan=2)
        username_label.grid(row=1, column=0)
        username_entry.grid(row=1, column=1)
        password_label.grid(row=2, column=0)
        password_entry.grid(row=2, column=1)
        login_button.grid(row=3, column=0, columnspan=2)

        self.window.mainloop()