import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkbootstrap import Frame, Label
from ttkbootstrap import Style
import sqlite3

days = 6
periods = 7
recess_break_aft = 4 # recess after 4th Period
section = None
butt_grid = []


period_names = list(map(lambda x: 'Period ' + str(x), range(1, 7+1)))
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thrusday', 'Friday', 'Saturday']



def select_sec():
    global section
    section = str(combo1.get())
    print(section)
    update_table(section)



def update_table(sec):
    for i in range(days):
        for j in range(periods):
            cursor = conn.execute(f"SELECT SUBCODE, FINI FROM SCHEDULE\
                WHERE DAYID={i} AND PERIODID={j} AND SECTION='{sec}'")
            cursor = list(cursor)
            print(cursor)
            
            butt_grid[i][j]['bg'] = '#f8f9fa'
            if len(cursor) != 0:
                subcode = cursor[0][0]
                cur1 = conn.execute(F"SELECT SUBTYPE FROM SUBJECTS WHERE SUBCODE='{subcode}'")
                cur1 = list(cur1)
                subtype = cur1[0][0]
                butt_grid[i][j]['fg'] = '#333333'
                if subtype == 'T':
                    butt_grid[i][j]['bg'] = '#007bff'
                elif subtype == 'P':
                    butt_grid[i][j]['bg'] = '#28a745'

                butt_grid[i][j]['text'] = str(cursor[0][0]) + '\n' + str(cursor[0][1])
                butt_grid[i][j].update()
                print(i, j, cursor[0][0])
            else:
                butt_grid[i][j]['fg'] = '#333333'
                butt_grid[i][j]['text'] = "No Class"
                butt_grid[i][j].update()



def process_button(d, p, sec):
    details = tk.Tk()
    cursor = conn.execute(f"SELECT SUBCODE, FINI FROM SCHEDULE\
                WHERE ID='{section+str((d*periods)+p)}'")
    cursor = list(cursor)
    if len(cursor) != 0:
        subcode = str(cursor[0][0]) 
        fini =  str(cursor[0][1])

        cur1 = conn.execute(f"SELECT SUBNAME, SUBTYPE FROM SUBJECTS\
            WHERE SUBCODE='{subcode}'")
        cur1 = list(cur1)
        subname = str(cur1[0][0])
        subtype = str(cur1[0][1])

        cur2 = conn.execute(f"SELECT NAME, EMAIL FROM FACULTY\
            WHERE INI='{fini}'")
        cur2 = list(cur2)
        fname = str(cur2[0][0])
        femail = str(cur2[0][1]) 

        if subtype == 'T':
            subtype = 'Theory'
        elif subtype == 'P':
            subtype = 'Practical'

    else:
        subcode = fini = subname = subtype = fname = femail = 'None'

    print(subcode, fini, subname, subtype, fname, femail)
    tk.Label(details, text='Class Details', font=('Consolas', 15, 'bold')).pack(pady=15)
    tk.Label(details, text='Day: '+day_names[d], font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Period: '+str(p+1), font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Subject Code: '+subcode, font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Subect Name: '+subname, font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Subject Type: '+subtype, font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Faculty Initials: '+fini, font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Faculty Name: '+fname, font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Faculty Email: '+femail, font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)

    tk.Button(
        details,
        text="OK",
        font=('Arial'),
        width=10,
        command=details.destroy
    ).pack(pady=10)

    details.mainloop()



def student_tt_frame(tt, sec):
    title_lab = tk.Label(
        tt,
        text='T  I  M  E  T  A  B  L  E',
        font=('Arial', 24, 'bold'),
        pady=10,
        background='#007bff',  # Dark blue background color
        foreground='white',  # White text color
    )
    title_lab.pack(fill='x')

    legend_f = Frame(tt)
    legend_f.pack(pady=15)
    
    Label(
        legend_f,
        text='Legend: ',
        font=('Arial', 10, 'italic'),
        foreground='#333333',  # Dark gray text color
        #background='#f8f9fa',  # Light gray background color
    ).pack(side=tk.LEFT)
    
    theory_label = Label(
        legend_f,
        text='Theory Classes',
        font=('Arial', 10, 'italic'),
        #width=12,
        #height=2,
        relief='raised',
        background='#007bff',  # Dark blue background color
        foreground='white',  # White text color
    )
    theory_label.pack(side=tk.LEFT, padx=10)
    
    practical_label = Label(
        legend_f,
        text='Practical Classes',
        relief='raised',
        font=('Arial', 10, 'italic'),
        #height=2,
        background='#28a745',  # Green background color
        foreground='white',  # White text color
        style='success.TLabel'  # Applying success style for green color
    )
    practical_label.pack(side=tk.LEFT, padx=10)

    global butt_grid
    global section
    section = sec

    table = tk.Frame(tt)
    table.pack()

    first_half = tk.Frame(table)
    first_half.pack(side='left')

    recess_frame = tk.Frame(table)
    recess_frame.pack(side='left')

    second_half = tk.Frame(table)
    second_half.pack(side='left')

    recess = tk.Label(
        recess_frame,
        text='R\n\nE\n\nC\n\nE\n\nS\n\nS',
        font=('Arial', 18, 'italic'),
        width=3,
        relief='sunken',
        background='#f8f9fa',  # Light gray background color
    )
    recess.pack()

    for i in range(days):
        b = tk.Label(
            first_half,
            text=day_names[i],
            font=('Arial', 12, 'bold'),
            width=9,
            height=2,
            bd=1,
            relief='solid',
            background='#007bff',
            foreground='white',
        )
        b.grid(row=i+1, column=0)

    for i in range(periods):
        if i < recess_break_aft:
            b = tk.Label(first_half)
            b.grid(row=0, column=i+1)
        else:
            b = tk.Label(second_half)
            b.grid(row=0, column=i)

        b.config(
            text=period_names[i],
            font=('Arial', 12, 'bold'),
            width=9,
            height=1,
            bd=1,
            relief='solid',
            background='#007bff',
            foreground='white',
        )

    for i in range(days):
        b = []
        for j in range(periods):
            if j < recess_break_aft:
                bb = tk.Button(first_half)
                bb.grid(row=i+1, column=j+1)
            else:
                bb = tk.Button(second_half)
                bb.grid(row=i+1, column=j)

            bb.config(
                text='Hello World!',
                font=('Arial', 10),
                width=13,
                height=3,
                bd=1,
                relief='solid',
                background='#f8f9fa',
                foreground='#333333',
                wraplength=80,
                justify='center', 
                command=lambda x=i, y=j, z=sec: process_button(x, y, z)
            )
            b.append(bb)

        butt_grid.append(b)
        # print(b)
        b = []

    print(butt_grid[0][1], butt_grid[1][1])
    update_table(sec)



conn = sqlite3.connect(r'files/timetable.db')
if __name__ == "__main__":
    
    # connecting database

    style = Style(theme='flatly')  # Changed theme to flatly for a modern look

    tt = style.master

    tt.title('Student Timetable')

    student_tt_frame(tt, section)

    sec_select_f = tk.Frame(tt, pady=15)
    sec_select_f.pack()

    tk.Label(
        sec_select_f,
        text='Select section:  ',
        font=('Consolas', 12, 'bold')
    ).pack(side=tk.LEFT)

    cursor = conn.execute("SELECT DISTINCT SECTION FROM STUDENT")
    sec_li = [row[0] for row in cursor]
    # sec_li.insert(0, 'NULL')
    print(sec_li)
    combo1 = ttk.Combobox(
        sec_select_f,
        values=sec_li,
    )
    combo1.pack(side=tk.LEFT)
    combo1.current(0)

    b = tk.Button(
        sec_select_f,
        text="OK",
        font=('Consolas', 12, 'bold'),
        padx=10,
        command=select_sec
    )
    b.pack(side=tk.LEFT, padx=10)
    b.invoke()


    tt.mainloop()