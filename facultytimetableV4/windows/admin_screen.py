import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style  # Import the Bootstrap style from themed_tkinter
import os
import threading
import sys

def run_sub(): 
    os.system('pythonw windows\\subjects.py')
def run_fac(): 
    os.system('pythonw windows\\faculty.py')
def run_sch(): os.system('pythonw windows\\scheduler.py')
def run_tt_s(): os.system('pythonw windows\\timetable_stud.py')
def run_tt_f(): os.system('pythonw windows\\timetable_fac.py')

# Create an instance of the Bootstrap style
style = Style(theme='litera')

ad = style.master
ad.geometry('500x430')
ad.title('Administrator')

tk.Label(
    ad,
    text='A D M I N I S T R A T O R',
    font=('Georgia', 20, 'bold'),
    pady=10
).pack()

tk.Label(
    ad,
    text='You are the Administrator',
    font=('Georgia', 12, 'italic'),
).pack(pady=9)

modify_frame = ttk.LabelFrame(ad, text='Modify', padding=20)
modify_frame.place(x=50, y=100)

tt_frame = ttk.LabelFrame(ad, text='Timetable', padding=20)
tt_frame.place(x=250, y=100)

# Use ttk.Button for better style
ttk.Button(
    modify_frame,
    text='Subjects',
    command=run_sub
).pack(pady=20)

ttk.Button(
    modify_frame,
    text='Faculties',
    command=run_fac
).pack(pady=20)

ttk.Button(
    tt_frame,
    text='Schedule Periods',
    command=run_sch
).pack(pady=20)

ttk.Button(
    tt_frame,
    text='View Section-Wise',
    command=run_tt_s
).pack(pady=20)

ttk.Button(
    tt_frame,
    text='View Faculty-wise',
    command=run_tt_f
).pack(pady=20)

ttk.Button(
    ad,
    text='Quit',
    command=ad.destroy
).place(x=220, y=360)

ad.mainloop()
