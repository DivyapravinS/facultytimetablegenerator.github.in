import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style

fid = passw = conf_passw = name = ini = email = subcode1 = subcode2 = None


'''
    LIST OF FUNCTIONS USED FOR VARIOUS FUNCTIONS THROUGH TKinter INTERFACE
        * create_treeview()
        * update_treeview()
        * parse_data()
        * update data()
        * remove_data()
        * show_passw()
'''

# create treeview (call this function once)
def create_treeview():
    tree['columns'] = ('Fid', 'Name', 'Subject 1', 'Subject 2')
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Fid", width=70, stretch=tk.NO)
    tree.column("Name", width=200, stretch=tk.NO)
    tree.column("Subject 1", width=80, stretch=tk.NO)
    tree.column("Subject 2", width=80, stretch=tk.NO)
    tree.heading('#0', text="")
    tree.heading('Fid', text="Fid")
    tree.heading('Name', text="Name")
    tree.heading('Subject 1', text="Subject 1")
    tree.heading('Subject 2', text="Subject 2")
    tree['height'] = 15


# update treeview (call this function after each update)
def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.execute("SELECT FID, NAME, SUBCODE1, SUBCODE2 FROM FACULTY")
    for row in cursor:
        tree.insert(
            "",
            0,
            values=(row[0], row[1], row[2], row[3])
        )
    tree.place(x=530, y=100)


# Parse and store data into database and treeview upon clicking of the add button
def parse_data():
    global fid, passw, conf_passw, name, ini, email, subcode1, subcode2
    fid = str(fid_entry.get())
    passw = str(passw_entry.get())
    conf_passw = str(conf_passw_entry.get())
    name = str(name_entry.get()).upper()
    ini = str(ini_entry.get()).upper()
    email = str(email_entry.get())
    subcode1 = str(combo1.get())
    subcode2 = str(combo2.get())

    if fid == "" or passw == "" or \
        conf_passw == "" or name == "":
        messagebox.showwarning("Bad Input", "Some fields are empty! Please fill them out!")
        return

    if passw != conf_passw:
        messagebox.showerror("Passwords mismatch", "Password and confirm password didn't match. Try again!")
        passw_entry.delete(0, tk.END)
        conf_passw_entry.delete(0, tk.END)
        return

    if subcode1 == "NULL":
        messagebox.showwarning("Bad Input", "Subject 1 can't be NULL")
        return

    conn.execute(f"REPLACE INTO FACULTY (FID, PASSW, NAME, INI, EMAIL, SUBCODE1, SUBCODE2)\
        VALUES ('{fid}','{passw}','{name}', '{ini}', '{email}', '{subcode1}', '{subcode2}')")
    conn.commit()
    update_treeview()

    fid_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    conf_passw_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    ini_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    combo1.current(0)
    combo2.current(0)


# update a row in the database
def update_data():
    fid_entry.delete(0, tk.END)
    passw_entry.delete(0, tk.END)
    conf_passw_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    ini_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    combo1.current(0)
    combo2.current(0)
    try:
        if len(tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Select one faculty at a time to update!")
            return

        q_fid = tree.item(tree.selection()[0])['values'][0]
        cursor = conn.execute(f"SELECT * FROM FACULTY WHERE FID = '{q_fid}'")

        cursor = list(cursor)
        fid_entry.insert(0, cursor[0][0])
        passw_entry.insert(0, cursor[0][1])
        conf_passw_entry.insert(0, cursor[0][1])
        name_entry.insert(0, cursor[0][2])
        ini_entry.insert(0, cursor[0][3])
        email_entry.insert(0, cursor[0][4])
        combo1.current(subcode_li.index(cursor[0][5]))
        combo2.current(subcode_li.index(cursor[0][6]))

        conn.execute(f"DELETE FROM FACULTY WHERE FID = '{cursor[0][0]}'")
        conn.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror("Bad Select", "Please select a faculty from the list first!")
        return


# remove selected data from database and treeview
def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror("Bad Select", "Please select a faculty from the list first!")
        return
    for i in tree.selection():
        conn.execute(f"DELETE FROM FACULTY WHERE FID = '{tree.item(i)['values'][0]}'")
        conn.commit()
        tree.delete(i)
        update_treeview()


# toggles between show/hide password
def show_passw():
    if passw_entry['show'] == "●":
        passw_entry['show'] = ""
        B1_show['text'] = '●'
        B1_show.update()
    elif passw_entry['show'] == "":
        passw_entry['show'] = "●"
        B1_show['text'] = '○'
        B1_show.update()
    passw_entry.update()


# main
if __name__ == "__main__":
    # DATABASE CONNECTIONS AND SETUP
    conn = sqlite3.connect(r'files/timetable.db')
    conn.execute('CREATE TABLE IF NOT EXISTS FACULTY\
    (FID CHAR(10) NOT NULL PRIMARY KEY,\
    PASSW CHAR(50) NOT NULL,\
    NAME CHAR(50) NOT NULL,\
    INI CHAR(5) NOT NULL,\
    EMAIL CHAR(50) NOT NULL,\
    SUBCODE1 CHAR(10) NOT NULL,\
    SUBCODE2 CHAR(10)    )')

    # TKinter Window with ttkbootstrap style
    subtk = tk.Tk()
    subtk.geometry('1000x550')
    subtk.title('Add/Update Faculties')

    style = Style(theme='litera')  # Change the theme as needed

    # Label widgets
    tk.Label(subtk, text='List of Faculties', font=('Georgia', 20, 'bold')).place(x=600, y=50)
    tk.Label(subtk, text='Add/Update Faculties', font=('Georgia', 20, 'bold')).place(x=90, y=50)
    tk.Label(subtk, text='Add information in the following prompt!', font=('Georgia', 10, 'italic')).place(x=100, y=85)
    tk.Label(subtk, text='Faculty id:', font=('Georgia', 12)).place(x=100, y=130)
    tk.Label(subtk, text='Password:', font=('Georgia', 12)).place(x=100, y=170)
    tk.Label(subtk, text='Confirm Password:', font=('Georgia', 12)).place(x=100, y=210)
    tk.Label(subtk, text='Faculty Name:', font=('Georgia', 12)).place(x=100, y=250)
    tk.Label(subtk, text='Initials:', font=('Georgia', 12)).place(x=100, y=290)
    tk.Label(subtk, text='Email:', font=('Georgia', 12)).place(x=100, y=330)
    tk.Label(subtk, text='Subject 1:', font=('Georgia', 12)).place(x=100, y=370)
    tk.Label(subtk, text='Subject 2:', font=('Georgia', 12)).place(x=100, y=410)
    
    
    # get subject code list from the database
    cursor = conn.execute("SELECT SUBCODE FROM SUBJECTS")
    subcode_li = [row[0] for row in cursor]
    subcode_li.insert(0, 'NULL')

    # Entry and Combobox widgets
    fid_entry = tk.Entry(subtk, font=('Georgia', 12), width=20)
    fid_entry.place(x=260, y=130)
    passw_entry = tk.Entry(subtk, font=('Georgia', 12), width=20, show="●")
    passw_entry.place(x=260, y=170)
    conf_passw_entry = tk.Entry(subtk, font=('Georgia', 12), width=20, show="●")
    conf_passw_entry.place(x=260, y=210)
    name_entry = tk.Entry(subtk, font=('Georgia', 12), width=25)
    name_entry.place(x=260, y=250)
    ini_entry = tk.Entry(subtk, font=('Georgia', 12), width=5)
    ini_entry.place(x=260, y=290)
    email_entry = tk.Entry(subtk, font=('Georgia', 12), width=25)
    email_entry.place(x=260, y=330)
    combo1 = ttk.Combobox(subtk, values=subcode_li)
    combo1.place(x=260, y=370)
    combo1.current(0)
    combo2 = ttk.Combobox(subtk, values=subcode_li)
    combo2.place(x=260, y=410)
    combo2.current(0)

    # Button widgets
    B1 = tk.Button(subtk, text='Add Faculty', font=('Georgia', 18), command=parse_data)
    B1.place(x=150, y=465)
    B2 = tk.Button(subtk, text='Update Faculty', font=('Georgia', 18), command=update_data)
    B2.place(x=410, y=465)
    B3 = tk.Button(subtk, text='Delete Faculty(s)', font=('Georgia', 18), command=remove_data)
    B3.place(x=650, y=465)
    B1_show = tk.Button(subtk, text='●', font=('Georgia', 9, 'bold'), command=show_passw)
    B1_show.place(x=460, y=170)

    # Treeview widget
    tree = ttk.Treeview(subtk)
    create_treeview()
    update_treeview()

    subtk.mainloop()
    conn.close()  # close database after all operations
