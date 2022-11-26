from Gui import *
from Employee import *
# from Database import *



def main():
    app = EmpApp()
    app.after(1000, app.frames['emp_page'].emp_page_entries)
    app.mainloop()



if __name__ == '__main__':
    main()

