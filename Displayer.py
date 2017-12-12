#http://effbot.org/tkinterbook/scrollbar.htm
try:
    from tkinter import *
    from tkMessageBox import *
    import hashlib
    from tkSimpleDialog import *
    from ast import literal_eval
    import pyaes
    import clipboard
except:
    import hashlib
    from ast import literal_eval
    from Tkinter import *
    import pyaes
    import clipboard
import ttk
import warnings
warnings.filterwarnings('ignore')
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
def parse_data():
    f = open('my_data.dat','r')
    lines = f.readlines()
    f.close()
    pswdhsh = lines[0].strip('\n')
    salt = lines[1].strip('\n')
    good_l = lines[2:]
    for i in good_l:
        parse_line(i,pswdhsh,salt)

def parse_line(l,hsh,salt):
    global inp_pass
    global tree
    global id,username
    id,username,password_enc = l.split('\t')
    password_enc = password_enc.strip('\n')
    key = hashlib.sha256(salt+inp_pass+hsh).digest()
    aes = pyaes.AESModeOfOperationCTR(key)
    pswd = aes.decrypt(literal_eval(password_enc))
    tree.insert('','end',text='',values=(id,username,pswd))

def update_table():
    if checked.get():
        tree['displaycolumns'] = ('id','user','pswd')
    else:
        tree['displaycolumns'] = ('id','user')

def copy_data(event):
    global tree
    item = tree.selection()[0]
    its = tree.item(item)
    vals = its['values']
    pswd = vals[2]
    clipboard.copy(pswd)
def show_remove(event):
    global tree
    global root
    root.update()
    #Supresses Warnings
    try:
        item = tree.selection()[0]
        if len(item) >= 2:
            r_butt.config(state='normal')
    except:
        r_butt.config(state='disabled')
def get_aes_crypto(key,text):
    encryptor = pyaes.AESModeOfOperationCTR(key)
    return encryptor.encrypt(text)
def r():
    item = tree.selection()[0]
    its = tree.item(item)
    vals = its['values']
    id_val,u,p = str(vals[0]).strip('\n'),str(vals[1]).strip('\n'),str(vals[2]).strip('\n')
    with open('my_data.dat','r') as f:
        l = f.readlines()
    lines = []
    for i in l:
        lines.append(i.strip('\n'))
    key = hashlib.sha256(salt + inp_pass + hashed).digest()
    pass_aes = get_aes_crypto(key, p)
    for i in lines:
        if i.split('\t') == ([id_val,u,repr(pass_aes)]):
            ind = lines.index(i)
    with open("my_data.dat", "r+") as f:
        lines = f.readlines()
        del lines[ind]
        f.seek(0)
        f.truncate()
        f.writelines(lines)
    for i in tree.get_children():
        tree.delete(i)
    parse_data()
import Add_Pass
def add_password():
    g = Toplevel()
    Add_Pass.startup(g)
def run(window):
    global root
    root = window
    global checked
    Button(root,text='Add Info',command = add_password).grid(row=1)
    Label(window,text="Double Click To Copy Password / Single Click + Remove Button To Remove Data").grid(row=0)
    checked = BooleanVar()
    global r_butt
    r_butt = Button(window,text='Remove Selected Info',command = r,state=DISABLED)
    r_butt.grid(row=2)
    c = Checkbutton(window,text="Show Password",variable=checked,command=update_table)
    c.grid(row=3)
    global tree
    tree = ttk.Treeview(window)
    tree['columns'] = ('id','user','pswd')
    tree.heading("id",text="ID / Website")
    tree.heading('user',text='Username')
    tree.heading('pswd',text='Password')
    tree['displaycolumns']=('id','user')
    tree['show'] = 'headings'
    tree.bind("<Double-1>",copy_data)
    window.bind('<Button-1>',show_remove)
    parse_data()
    tree.grid(row=3)
if __name__ == '__main__':
    root = Tk()
    startup(root)
    root.mainloop()