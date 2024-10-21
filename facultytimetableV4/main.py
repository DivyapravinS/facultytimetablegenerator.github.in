import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkbootstrap import Style  # Import the Bootstrap style from themed_tkinter
import os, sys
sys.path.insert(0, 'windows/')
import timetable_stud
import timetable_fac
import sqlite3
from timetable_fac import gen_doc

# Create an instance of the Bootstrap style
style = Style(theme='litera')  # Use a valid theme name, such as 'flatly'

def challenge():
    conn = sqlite3.connect(r'files/timetable.db')

    user = str(combo1.get())
    if user == "Student":
        cursor = conn.execute(f"SELECT PASSW, SECTION, NAME, ROLL FROM STUDENT WHERE SID='{id_entry.get()}'")
        cursor = list(cursor)
        if len(cursor) == 0:
            messagebox.showwarning('Bad id', 'No such user found!')
        elif passw_entry.get() != cursor[0][0]:
            messagebox.showerror('Bad pass', 'Incorrect Password!')
        else:
            nw = tk.Tk()
            tk.Label(
                nw,
                text=f'{cursor[0][2]}\tSection: {cursor[0][1]}\tRoll No.: {cursor[0][3]}',
                font=('Consolas', 12, 'italic'),
            ).pack()
            m.destroy()
            timetable_stud.student_tt_frame(nw, cursor[0][1])
            nw.mainloop()

    elif user == "Faculty":
        cursor = conn.execute(f"SELECT PASSW, INI, NAME, EMAIL FROM FACULTY WHERE FID='{id_entry.get()}'")
        cursor = list(cursor)
        if len(cursor) == 0:
            messagebox.showwarning('Bad id', 'No such user found!')
        elif passw_entry.get() != cursor[0][0]:
            messagebox.showerror('Bad pass', 'Incorrect Password!')
        else:
            nw = tk.Tk()
            tk.Label(
                nw,
                text=f'{cursor[0][2]} ({cursor[0][1]})\tEmail: {cursor[0][3]}',
                font=('Consolas', 12, 'italic'),
            ).pack()
            m.destroy()
            timetable_fac.fac_tt_frame(nw, cursor[0][1])
            b1= tk.Button(
                nw,
                text="Download",
                font=('Consolas', 12, 'bold'),
                padx=10,
                command=gen_doc
            )
            b1.pack(side=tk.LEFT, padx=10)
            nw.mainloop()

    elif user == "Admin":
        if id_entry.get() == 'admin' and passw_entry.get() == 'admin':
            m.destroy()
            os.system('python windows\\admin_screen.py')
        else:
            messagebox.showerror('Bad Input', 'Incorrect Username/Password!')


# Create the main window with Bootstrap style
m = style.master

# Set window properties
m.geometry('400x430')
m.title('Welcome')

# Labels
tk.Label(
    m,
    text='TIMETABLE MANAGEMENT SYSTEM',
    font=('Consolas', 20, 'bold'),
    wrap=400
).pack(pady=20)

tk.Label(
    m,
    text='Welcome!\nLogin to continue',
    font=('Consolas', 12, 'italic')
).pack(pady=10)

tk.Label(
    m,
    text='Username',
    font=('Consolas', 15)
).pack()

# Entry for Username
id_entry = ttk.Entry(
    m,
    width=21
)
id_entry.pack()

# Label for Password
tk.Label(
    m,
    text='Password:',
    font=('Consolas', 15)
).pack()

# Toggles between show/hide password
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

# Frame for Password Entry
pass_entry_f = tk.Frame()
pass_entry_f.pack()

# Entry for Password
passw_entry = ttk.Entry(
    pass_entry_f,
    width=15,
    show="●"
)
passw_entry.pack(side=tk.LEFT)

# Button to toggle password visibility
B1_show = ttk.Button(
    pass_entry_f,
    text='○',
    command=show_passw
)
B1_show.pack(side=tk.LEFT, padx=15)

# Combobox for User Type
combo1 = ttk.Combobox(
    m,
    values=['Student', 'Faculty', 'Admin']
)
combo1.pack(pady=15)
combo1.current(0)

# Button for Login
ttk.Button(
    m,
    text='Login',
    style='success.TButton',
    command=challenge
).pack(pady=10)

m.mainloop()
