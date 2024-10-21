import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style

# inputs in this window
subcode = subname = subtype = None

# create treeview (call this function once)
def create_treeview():
    tree['columns'] = ('one', 'two', 'three')
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("one", width=70, stretch=tk.NO)
    tree.column("two", width=300, stretch=tk.NO)
    tree.column("three", width=60, stretch=tk.NO)
    tree.heading('#0', text="")
    tree.heading('one', text="Code")
    tree.heading('two', text="Name")
    tree.heading('three', text="Type")

# update treeview (call this function after each update)
def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.execute("SELECT * FROM SUBJECTS")
    for row in cursor:
        if row[2] == 'T':
            t = 'Theory'
        elif row[2] == 'P':
            t = 'Practical'
        tree.insert("", 0, values=(row[0], row[1], t))

# Parse and store data into database and treeview upon clicking of the add button
def parse_data():
    subcode = str(subcode_entry.get())
    subname = str(subname_entry.get("1.0", tk.END)).upper().rstrip()
    subtype = str(radio_var.get()).upper()

    if subcode=="" or subname=="":
        messagebox.showerror("Bad Input", "Please fill up Subject Code and/or Subject Name!")
        return

    conn.execute(f"REPLACE INTO SUBJECTS (SUBCODE, SUBNAME, SUBTYPE) VALUES ('{subcode}','{subname}','{subtype}')")
    conn.commit()
    update_treeview()

    subcode_entry.delete(0, tk.END)
    subname_entry.delete("1.0", tk.END)

# update a row in the database
def update_data():
    try:
        if len(tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Select one subject at a time to update!")
            return

        row = tree.item(tree.selection()[0])['values']
        subcode_entry.insert(0, row[0])
        subname_entry.insert("1.0", row[1])
        if row[2][0] == "T":
            R1.invoke()
        elif row[2][0] == "P":
            R2.invoke()

        conn.execute(f"DELETE FROM SUBJECTS WHERE SUBCODE = '{row[0]}'")
        conn.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror("Bad Select", "Please select a subject from the list first!")
        return

# remove selected data from database and treeview
def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror("Bad Select", "Please select a subject from the list first!")
        return
    for i in tree.selection():
        conn.execute(f"DELETE FROM SUBJECTS WHERE SUBCODE = '{tree.item(i)['values'][0]}'")
        conn.commit()
        tree.delete(i)
        update_treeview()

# main
if __name__ == "__main__":  

    # connecting database
    conn = sqlite3.connect(r'files/timetable.db')
    conn.execute('CREATE TABLE IF NOT EXISTS SUBJECTS\
        (SUBCODE CHAR(10) NOT NULL PRIMARY KEY,\
        SUBNAME CHAR(50) NOT NULL,\
        SUBTYPE CHAR(1) NOT NULL)')

    # TKinter Window
    subtk = tk.Tk()
    subtk.geometry('800x600')
    subtk.title('Add/Update/Delete Subjects')

    # ttkbootstrap Style
    style = Style(theme='pulse')

    # Frame for left column
    left_frame = ttk.Frame(subtk)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10)

    # Label1 (Add/Update/Delete Subjects)
    ttk.Label(
        left_frame,
        text='Add/Update/Delete Subjects',
        font=('Helvetica', 20, 'bold')
    ).pack(pady=10)

    # Subject Code Label and Entry
    ttk.Label(left_frame, text='Subject Code:').pack(pady=5)
    subcode_entry = ttk.Entry(left_frame)
    subcode_entry.pack(pady=5)

    # Subject Name Label and Text
    ttk.Label(left_frame, text='Subject Name:').pack(pady=5)
    subname_entry = tk.Text(left_frame, height=3, width=30)
    subname_entry.pack(pady=5)

    # Subject Type Label and Radiobuttons
    ttk.Label(left_frame, text='Subject Type:').pack(pady=5)
    radio_var = tk.StringVar()
    R1 = ttk.Radiobutton(left_frame, text='Theory', variable=radio_var, value='T')
    R1.pack(side=tk.LEFT, padx=5)
    R2 = ttk.Radiobutton(left_frame, text='Practical', variable=radio_var, value='P')
    R2.pack(side=tk.LEFT, padx=5)

    # Add/Update/Delete Buttons
    ttk.Button(left_frame, text='Add Subject', command=parse_data).pack(pady=10)
    ttk.Button(left_frame, text='Update Subject', command=update_data).pack(pady=10)
    ttk.Button(left_frame, text='Delete Subject', command=remove_data).pack(pady=10)

    # Frame for right column (Treeview)
    right_frame = ttk.Frame(subtk)
    right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    # List of Subjects
    ttk.Label(right_frame, text='List of Subjects', font=('Helvetica', 16, 'bold')).pack()
    tree = ttk.Treeview(right_frame)
    create_treeview()
    update_treeview()
    tree.pack()

    subtk.mainloop()
    conn.close()  # Close
