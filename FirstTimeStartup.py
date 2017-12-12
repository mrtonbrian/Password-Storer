import os
from hashlib import sha256
from Crypto.Random import random
try:
    from tkinter import *
    from tkMessageBox import *
    from tkSimpleDialog import *
except ImportError:
    from Tkinter import *

def presetup_data():
    global root
    try:
        open('my_data.dat')
        #Means Data Is Present, Prompt For Overwrite
        overwrite_yes = askyesno('Overwrite?','Previous Data Found \n Overwrite it?')
        if overwrite_yes:
            #Deletes Data File
            os.remove('my_data.dat')
            setup_data()
        else:
            root.destroy()
            sys.exit()
    except:
        #Means Data Is Not Present
        setup_data()
def get_salt():
    #Chars To Use For Generating Salt
    alph = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()"
    chars = []
    #Gets A Random Char From Alph 16 Times
    for i in range(16):
        #Uses PyCrypto Random As Cryptographically Secure Random Chooser
        chars.append(random.choice(alph))
    return "".join(chars)
def setup_data():
    #Gets New Password
    global root
    master_pass = askstring('Password','Please Type In Your Master Password (It Cannot Be Recovered)',show='*')
    if master_pass != None:
        b_inp = True
        while b_inp:
            re_enter = askstring('Reenter Password','Please Re-Enter Your Password \n Note: If You Are Re-Seeing This Menu,\nYou Typed your Password In Wrong \n Hit Cancel To Reset Your Password',show='*')
            if re_enter == master_pass:
                break
            elif re_enter == None:
                master_pass = askstring('Password','Please Type In Your Master Password (It Cannot Be Recovered)',show='*')
    else:
        g = askyesno('Quit?',"Quit Setup?")
        if g:
           root.destroy()
           sys.exit()
        else:
            setup_data()
    #Salt To Be Used Later
    salt = get_salt()
    f = open('my_data.dat','w')
    #Writes Hashed Password and Salt
    f.write(sha256(master_pass+salt).hexdigest()+'\n')
    f.write(salt+'\n')
    f.close()
    #Tells User To Reopen PasswordStorer.py
    showinfo("Complete!","Setup Is Complete! Rerun PasswordStorer")
    root.destroy()
def run(window):
    global root
    root = window
    root.withdraw()
if __name__ == '__main__':
    GUI = Tk()
    run(GUI)
    presetup_data()
    GUI.mainloop()
