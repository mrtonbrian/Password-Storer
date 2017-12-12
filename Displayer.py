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
#Supresses Warnings (Not Necessary)
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
#Parses Data File
def parse_data():
    f = open('my_data.dat','r')
    lines = f.readlines()
    f.close()
    pswdhsh = lines[0].strip('\n')
    salt = lines[1].strip('\n')
    good_l = lines[2:]
    #Iterates Through Lines After Salt / Password Hash
    for i in good_l:
        #Params: Line, Password Hash, Salt
        parse_line(i,pswdhsh,salt)

def parse_line(l,hsh,salt):
    global inp_pass
    global tree
    #Gets Line, Separates By Tab
    id,username,password_enc = l.split('\t')
    #Removes NewLine From Encoded Password
    password_enc = password_enc.strip('\n')
    #Decodes Password
    key = hashlib.sha256(salt+inp_pass+hsh).digest()
    aes = pyaes.AESModeOfOperationCTR(key)
    pswd = aes.decrypt(literal_eval(password_enc))
    #Inserts Data Into Table
    tree.insert('','end',text='',values=(id,username,pswd))

def update_table():
    #Checks If Checkbox Is Checked
    if checked.get():
        #If So: Display Password Column
        tree['displaycolumns'] = ('id','user','pswd')
    else:
        #If Not: Only Display ID and User Column
        tree['displaycolumns'] = ('id','user')

def copy_data(event):
    global tree
    #Gets Selected Item From Table
    item = tree.selection()[0]
    its = tree.item(item)
    #Gets Values Of Selections From Dict
    vals = its['values']
    #Gets 2nd Index (Password Column)
    pswd = vals[2]
    clipboard.copy(pswd)

def show_remove(event):
    global tree
    global root
    root.update()
    #Supresses Warnings
    try:
        item = tree.selection()[0]
        #Checks To See If Any Lines Are Selected
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
    #Strips Newlines From Values
    id_val,u,p = str(vals[0]).strip('\n'),str(vals[1]).strip('\n'),str(vals[2]).strip('\n')
    #Gets Lines From File
    with open('my_data.dat','r') as f:
        l = f.readlines()
    lines = []
    #Iterates Through Lines
    for i in l:
        lines.append(i.strip('\n'))
    #Rebuilds Encrypted Password
    key = hashlib.sha256(salt + inp_pass + hashed).digest()
    pass_aes = get_aes_crypto(key, p)
    for i in lines:
        #Rebuilds Line To Find Index Of Selected Line in Table To Corresponding In File
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
        #Rewrites Data W/O Line
        f.writelines(lines)
    #Rebuilds Data Table
    for i in tree.get_children():
        tree.delete(i)
    parse_data()
def run(window):
    global root
    root = window
    global checked
    #Label
    Label(window,text="Double Click To Copy Password / Single Click + Remove Button To Remove Data").grid(row=0)
    #Remove Button
    global r_butt
    r_butt = Button(window,text='Remove Selected Info',command = r,state=DISABLED)
    r_butt.grid(row=2)
    #Checkbox
    checked = BooleanVar()
    c = Checkbutton(window,text="Show Password",variable=checked,command=update_table)
    c.grid(row=3)
    #Treeview
    global tree
    tree = ttk.Treeview(window)
    tree['columns'] = ('id','user','pswd')
    tree.heading("id",text="ID / Website")
    tree.heading('user',text='Username')
    tree.heading('pswd',text='Password')
    tree['displaycolumns']=('id','user')
    tree['show'] = 'headings'
    #Tree Bindings To Copy / Remove
    tree.bind("<Double-1>",copy_data)
    window.bind('<Button-1>',show_remove)
    parse_data()
    tree.grid(row=3)
if __name__ == '__main__':
    root = Tk()
    startup(root)
    root.mainloop()
