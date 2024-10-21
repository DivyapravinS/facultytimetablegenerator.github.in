import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkbootstrap import Frame, Label
from ttkbootstrap import Style
import sqlite3
from docxtpl import DocxTemplate
from docx2pdf import convert
import win32api
import os

days = 6
periods = 7
recess_break_aft = 4 # recess after 3rd Period
fini = None
butt_grid = []


period_names = list(map(lambda x: 'Period ' + str(x), range(1, 7+1)))
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thrusday', 'Friday','Saturday']

def gen_doc():
    #doc = DocxTemplate("invoicetemplate.docx")
    # Load the Word template
    doc = DocxTemplate("C:/Users/sriha/facultytimetableV3/windows/temp1.docx")
    cursor = conn.execute(f"SELECT EMAIL FROM FACULTY WHERE INI='{fini}'")
    cursor = list(cursor)
    em = cursor[0][0]
    
    cursor = conn.execute(f"SELECT NAME FROM FACULTY WHERE INI='{fini}'")
    cursor = list(cursor)
    nam = cursor[0][0]

    subjects_handled = set()
    # Prepare data to fill in the template
    data = {
        "fname": nam,  # Use the selected faculty's initials
        "email": em,  # Update with actual email if available
        # Add other data here for day/time slots based on the faculty's timetable
    }
    

    # Fetch timetable data from the database for the selected faculty
    for i in range(days):
        for j in range(periods):
            cursor = conn.execute(f"SELECT SECTION, SUBCODE FROM SCHEDULE\
                WHERE DAYID={i} AND PERIODID={j} AND FINI='{fini}'")
            cursor = list(cursor)
            if len(cursor) != 0:
                section = cursor[0][0]
                subcode = cursor[0][1]
                cur1 = conn.execute(f"SELECT SUBSHORT FROM SUBDISP WHERE SUBCODE='{subcode}'")
                cur1 = list(cur1)
                subshort = cur1[0][0]
                print(f"CLASS-{section}\n{subshort}")
                data[f"d{i}p{j}"] = f"CLASS-{section}\n{subshort}"
            else:
                data[f"d{i}p{j}"] = "-"

    # Fetch distinct subject codes handled by the faculty
    cursor = conn.execute(f"SELECT DISTINCT SUBCODE FROM SCHEDULE WHERE FINI='{fini}'")
    cursor = list(cursor)

    for i in range(len(cursor)):
        subcode = cursor[i][0]
    
        # Fetch subject short form
        cursor1 = conn.execute(f"SELECT SUBSHORT FROM SUBDISP WHERE SUBCODE='{subcode}'")
        cursor1 = list(cursor1)
        data[f'subshort{i+1}'] = cursor1[0][0]
    
        # Fetch subject name
        cursor1 = conn.execute(f"SELECT SUBNAME FROM SUBJECTS WHERE SUBCODE='{subcode}'")
        cursor1 = list(cursor1)
        data[f'subname{i+1}'] = cursor1[0][0]

    #data['subshort2'] = 
    #data['subname2'] = 
    # Render the template with the data
    print(data)
    doc.render(data)

    
    # Save the rendered document
    doc.save(f"{fini}.docx")

    # Convert the document to PDF
    convert(f"{fini}.docx")

    # Open the PDF document
    win32api.ShellExecute(0, "open", f"{fini}.pdf", None, None, 1)


def select_fac():
    global fini
    fini = str(combo1.get())
    print(fini)
    update_table(fini)



def update_table(fini):
    for i in range(days):
        for j in range(periods):
            cursor = conn.execute(f"SELECT SECTION, SUBCODE FROM SCHEDULE\
                WHERE DAYID={i} AND PERIODID={j} AND FINI='{fini}'")
            cursor = list(cursor)
            print(cursor)

            butt_grid[i][j]['bg'] = '#f8f9fa'  # Light gray background color
            if len(cursor) != 0:
                subcode = cursor[0][1]
                cur1 = conn.execute(f"SELECT SUBTYPE FROM SUBJECTS WHERE SUBCODE='{subcode}'")
                cur1 = list(cur1)
                subtype = cur1[0][0]
                butt_grid[i][j]['fg'] = '#333333'  # Dark gray text color
                if subtype == 'T':
                    butt_grid[i][j]['bg'] = '#007bff'  # Dark blue background color
                elif subtype == 'P':
                    butt_grid[i][j]['bg'] = '#28a745'  # Green background color

                sec_li = [x[0] for x in cursor]
                t = ', '.join(sec_li)
                butt_grid[i][j]['text'] = "Sections: " + t
                print(i, j, cursor[0][0])
            else:
                butt_grid[i][j]['fg'] = '#333333'  # Dark gray text color
                butt_grid[i][j]['text'] = "No Class"
                butt_grid[i][j].update()



def process_button(d, p):
    print(d, p, fini)
    details = tk.Tk()
    cursor = conn.execute(f"SELECT SECTION, SUBCODE FROM SCHEDULE\
                WHERE DAYID={d} AND PERIODID={p} AND FINI='{fini}'")
    cursor = list(cursor)
    print("section", cursor)
    if len(cursor) != 0:
        sec_li = [x[0] for x in cursor]
        t = ', '.join(sec_li)
        subcode = cursor[0][1]
        cur1 = conn.execute(f"SELECT SUBNAME, SUBTYPE FROM SUBJECTS\
            WHERE SUBCODE='{subcode}'")
        cur1 = list(cur1)
        subname = str(cur1[0][0])
        subtype = str(cur1[0][1])

        if subtype == 'T':
            subtype = 'Theory'
        elif subtype == 'P':
            subtype = 'Practical'

    else:
        sec_li = subcode = subname = subtype = t = 'None'

    tk.Label(details, text='Class Details', font=('Arial', 15, 'bold')).pack(pady=15)
    
    tk.Label(
        details, 
        text='Day: ' + day_names[d], 
        font=('Arial', 12), 
        #anchor="w",
        background='white',
        foreground='#333333',
        padx=10,
        pady=5).pack()
    tk.Label(details, text='Period: ' + str(p + 1), font=('Arial'), anchor="w").pack()
    tk.Label(details, text='Subject Code: ' + subcode, font=('Arial'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Subect Name: ' + subname, font=('Arial'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Subject Type: ' + subtype, font=('Arial'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Faculty Initials: ' + fini, font=('Arial'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Sections: ' + t, font=('Arial'), anchor="w").pack(expand=1, fill=tk.X, padx=20)

    tk.Button(
        details,
        text="OK",
        font=('Arial'),
        width=10,
        command=details.destroy
    ).pack(pady=10)

    details.mainloop()



def fac_tt_frame(tt, f):
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
    global fini
    fini = f

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
        b.grid(row=i + 1, column=0)

    for i in range(periods):
        if i < recess_break_aft:
            b = tk.Label(first_half)
            b.grid(row=0, column=i + 1)
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
                bb.grid(row=i + 1, column=j + 1)
            else:
                bb = tk.Button(second_half)
                bb.grid(row=i + 1, column=j)

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
                command=lambda x=i, y=j: process_button(x, y)
            )
            b.append(bb)

        butt_grid.append(b)
        # print(b)
        b = []

    print(butt_grid[0][1], butt_grid[1][1])
    update_table(fini)



conn = sqlite3.connect(r'files/timetable.db')
if __name__ == "__main__":
    
    # connecting database


    style = Style(theme='flatly')  # Changed theme to flatly for a modern look

    tt = style.master
    
    tt.title('Faculty Timetable')
    
    fac_tt_frame(tt, fini)

    fac_select_f = tk.Frame(tt, pady=15)
    fac_select_f.pack()

    tk.Label(
        fac_select_f,
        text='Select Faculty:  ',
        font=('Arial', 12, 'bold'),
        background='#f8f9fa',  # Light gray background color
        foreground='#333333',  # Dark gray text color
    ).pack(side=tk.LEFT)

    cursor = conn.execute("SELECT DISTINCT INI FROM FACULTY")
    fac_li = [row[0] for row in cursor]
    print(fac_li)
    combo1 = ttk.Combobox(
        fac_select_f,
        values=fac_li,
    )
    combo1.pack(side=tk.LEFT)
    combo1.current(0)

    b = tk.Button(
        fac_select_f,
        text="OK",
        font=('Arial', 12, 'bold'),
        padx=10,
        command=select_fac
    )
    b.pack(side=tk.LEFT, padx=10)
    b.invoke()
    
    b1= tk.Button(
        fac_select_f,
        text="Download",
        font=('Arial', 12, 'bold'),
        padx=10,
        command=gen_doc
    )
    b1.pack(side=tk.LEFT, padx=10)

    tt.mainloop()