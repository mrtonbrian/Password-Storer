import hashlib
try:
    from tkinter import *
    from tkMessageBox import *
    from tkSimpleDialog import *
    from Crypto.Random import random
    import pyaes
except ImportError:
    from Crypto.Random import random
    import pyaes
    from Tkinter import *
import warnings
warnings.filterwarnings('ignore')
#Startup Method
def startup(window):
    global salt
    global inp_pass
    global hashed
    #Hides Window
    window.withdraw()
    with open('my_data.dat','r') as f:
        lines = f.readlines()
        #Checking Inputted Password
        inp_pass = askstring("Password","Enter Your Password",show='*')
        salt = lines[1]
        salt = salt.strip('\n')
        hashed = lines[0]
        hashed = hashed.strip('\n')
        g = hashlib.sha256(inp_pass+salt).hexdigest() == hashed
        #Sees if User Inputted Correct Password First Time
        if g:
            b_inp = False
        elif g == None:
            window.destroy()
        else:
            b_inp = True
        while b_inp:
            g = hashlib.sha256(inp_pass+salt).hexdigest() == hashed
            inp_pass = askstring("Incorrect Password", "Incorrect Password!\nReenter Your Password\nOr Hit Cancel To Exit Menu",show='*')
            if g:
                b_inp = False
            elif g == None:
                window.destroy()
    window.deiconify()
    run(window)
def pre_add():
    #Sets Up Data / Checks Data before Adding
    global id_ent,user_ent,pass_ent
    if id_ent.get() == '' or user_ent.get() == '' or pass_ent.get() == '':
        showwarning("Not Filled Out","Please Fill Out Entire Form!")
        return None
    else:
        add_info()

#Gets Encrypted Text
def get_aes_crypto(key,text):
    encryptor = pyaes.AESModeOfOperationCTR(key)
    return encryptor.encrypt(text)
def add_info():
    global salt,inp_pass,hashed
    global id_ent,user_ent,pass_ent
    full_line = ""
    #Adds Tabs For Parsing Later
    full_line = full_line+id_ent.get()+'\t'
    full_line = full_line+user_ent.get()+'\t'
    #Gets The Key For AES, Uses Digest For 16 Char Key
    key = hashlib.sha256(salt+inp_pass+hashed).digest()
    p_to_enc = pass_ent.get()
    pass_aes = get_aes_crypto(key,p_to_enc)
    #Uses Repr to Avoid Using Unicode Char
    full_line = full_line+repr(pass_aes)+'\n'
    #Appends Data
    f = open('my_data.dat','a+')
    f.write(full_line)
    f.close()
    showinfo("Complete","Added New Info!")
    return None
def clear():
    #Clears Entries
    global id_ent, user_ent, pass_ent
    id_ent.delete(0,'end')
    user_ent.delete(0, 'end')
    pass_ent.delete(0, 'end')
def run(window):
    global root
    global id_ent,user_ent,pass_ent
    root = window
    window.title("Add Password")
    #ID
    Label(root,text="ID Or Website: ").grid(row=0,column=0)
    id_ent = Entry(root,width=10)
    id_ent.grid(row=0,column=1)
    #Username
    Label(root,text="Username: ").grid(row=1,column=0)
    user_ent = Entry(root,width=10)
    user_ent.grid(row=1,column=1)
    #Password
    Label(root,text="Password: ").grid(row=2,column=0)
    pass_ent = Entry(root,width=10)
    pass_ent.grid(row=2,column=1)
    #Button
    Button(root,text="Add Info!",command = pre_add).grid(row=3,column=0)
    Button(root,text="Clear All Boxes",command = clear).grid(row=3,column=1)
    window.mainloop()
if __name__ == '__main__':
    GUI = Tk()
    startup(GUI)
    GUI.mainloop()
