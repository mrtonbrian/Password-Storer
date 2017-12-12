try:
    from tkinter import *
    from tkMessageBox import *
except ImportError:
    from Tkinter import *
import Add_Pass
import FirstTimeStartup
import Displayer
try:
    open('my_data.dat','r')
except:
    showinfo("No Data Found","No Data Found \n Going Through First Time Setup")
    FirstTimeStartup.presetup_data()
def add_password():
    g = Toplevel()
    Add_Pass.startup(g)
def display():
    g = Toplevel()
    Displayer.startup(g)
def run(window):
    global master
    master = window
    Button(master,text='Add Info',command = add_password).pack()
    Button(master,text="Display Data",command=display).pack()
if __name__ == '__main__':
    root = Tk()
    run(root)
    root.mainloop()