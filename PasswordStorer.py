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
import FirstTimeStartup

try:
    open('my_data.dat','r')
except:
    showinfo("No Data Found","No Data Found \n Going Through First Time Setup")
    FirstTimeStartup.presetup_data()
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
        #User Hit Cancel
        elif g == None:
            window.destroy()
        #Incorrect Password
        else:
            b_inp = True
        #Loop Until Good or Cancel
        while b_inp:
            g = hashlib.sha256(inp_pass+salt).hexdigest() == hashed
            inp_pass = askstring("Incorrect Password", "Incorrect Password!\nReenter Your Password\nOr Hit Cancel To Exit Menu",show='*')
            if g:
                b_inp = False
            elif g == None:
                window.destroy()
                sys.exit()
    window.deiconify()
    run(window)
def parse_data():
    global tree
    #Clears Tree
    tree.delete(*tree.get_children())
    #Opens Data File
    f = open('my_data.dat','r')
    lines = f.readlines()
    f.close()
    #Gets Hashed Password and Salt
    pswdhsh = lines[0].strip('\n')
    salt = lines[1].strip('\n')
    #Lines That Have Data
    good_l = lines[2:]
    for i in good_l:
        parse_line(i,pswdhsh,salt)

def parse_line(l,hsh,salt):
    global inp_pass
    global tree
    #Gets ID, Username, Encoded Password
    id,username,password_enc = l.split('\t')
    #Removes Newline From Encoded Password
    password_enc = password_enc.strip('\n')
    #Decodes Password
    key = hashlib.sha256(salt+inp_pass+hsh).digest()
    aes = pyaes.AESModeOfOperationCTR(key)
    pswd = aes.decrypt(literal_eval(password_enc))
    #Adds To Table
    tree.insert('','end',text='',values=(id,username,pswd))

def update_table():
    #If CheckBox is Checked: Show Password Columns
    if checked.get():
        tree['displaycolumns'] = ('id','user','pswd')
    else:
        #If Not: Hide Password
        tree['displaycolumns'] = ('id','user')

def copy_data(event):
    global tree
    #Gets Selection
    item = tree.selection()[0]
    its = tree.item(item)
    #Gets Values Of Selection
    vals = its['values']
    #Gets 2nd Index (Password Column)
    pswd = vals[2]
    clipboard.copy(pswd)
def show_remove(event):
    global tree
    global root
    root.update()
    #Supresses Any Errors
    try:
        #Checks To See If Any Lines Are Selected
        item = tree.selection()[0]
        if len(item) >= 2:
            """
            If So: Set To Normal . . . 
            Once One Is Selected, At Least One Will Always Be Selected
            So: Don't Need To Check For No Selection
            """
            r_butt.config(state='normal')
    except:
        r_butt.config(state='disabled')

#Encrypts Input Text
def get_aes_crypto(key,text):
    encryptor = pyaes.AESModeOfOperationCTR(key)
    return encryptor.encrypt(text)
def r():
    #Gets Selection
    item = tree.selection()[0]
    its = tree.item(item)
    #Gets Values
    vals = its['values']
    #Strips Newlines / Assigns Variables
    id_val,u,p = str(vals[0]).strip('\n'),str(vals[1]).strip('\n'),str(vals[2]).strip('\n')
    with open('my_data.dat','r') as f:
        l = f.readlines()
    lines = []
    #Iterates Through Each Line
    for i in l:
        lines.append(i.strip('\n'))
    #Rebuilds Encrypted Password
    key = hashlib.sha256(salt + inp_pass + hashed).digest()
    pass_aes = get_aes_crypto(key, p)
    for i in lines:
        #Rebuilds Line To Find Index Of Selected Line In Table Corresponding To File
        if i.split('\t') == ([id_val,u,repr(pass_aes)]):
            ind = lines.index(i)
    with open("my_data.dat", "r+") as f:
        #Grabs All Lines
        lines = f.readlines()
        #Deletes Proper Line
        del lines[ind]
        #Clears File
        f.seek(0)
        f.truncate()
        #Wries Data W/O Line
        f.writelines(lines)
    #Rebuilds Table
    for i in tree.get_children():
        tree.delete(i)
    parse_data()

#Runs Add Password Program
import Add_Pass
def add_password():
    g = Toplevel()
    Add_Pass.startup(g)

def run(window):
    global root
    root = window
    global checked
    #Refresh Table / Add Info Button
    #Info Label
    Button(root,text='Refresh Table',command=parse_data).grid(row=0)
    Button(root,text='Add Info',command = add_password).grid(row=2)
    Label(window,text="Double Click To Copy Password / Single Click + Remove Button To Remove Data").grid(row=1)
    #CheckBox
    checked = BooleanVar()
    c = Checkbutton(window, text="Show Password", variable=checked, command=update_table)
    c.grid(row=4)
    #Remove Button
    global r_butt
    r_butt = Button(window,text='Remove Selected Info',command = r,state=DISABLED)
    r_butt.grid(row=3)
    #Treeview
    global tree
    tree = ttk.Treeview(window)
    tree['columns'] = ('id','user','pswd')
    tree.heading("id",text="ID / Website")
    tree.heading('user',text='Username')
    tree.heading('pswd',text='Password')
    tree['displaycolumns']=('id','user')
    tree['show'] = 'headings'
    #Bindings To Copy / Remove
    tree.bind("<Double-1>",copy_data)
    window.bind('<Button-1>',show_remove)
    #First Time Parse Data
    parse_data()
    tree.grid(row=5)
    #Scrollbar
    tree_scroller = Scrollbar(window)
    tree_scroller.configure(command=tree.yview)
    tree.configure(yscrollcommand=tree_scroller.set)
    tree_scroller.grid(row=5,column=1,sticky='NSW')

if __name__ == '__main__':
    root = Tk()
    startup(root)
    root.mainloop()
