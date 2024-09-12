# College cutoff
# Prerequisites: right click and download the 5 csv files from drive (make sure they are in the same location in your computer as this python program.)
import csv
import tkinter
from tkinter import messagebox
import mysql.connector

con = mysql.connector.connect(host='localhost', password='root',
                              user='root')  # type your own host name password and user name in place of the strings in quotes.
cursor = con.cursor()


def ex(query):
    """
    Executes the mysql query that is passed.
    """
    cursor.execute(query)


ex('Drop database IF EXISTS Collegecutoff')
ex('Create database Collegecutoff')
ex('Use Collegecutoff')
ex(
    'Create table College(SerialNo int primary key,CollegeName char(10),CollegeBranch char(20),NIRFRanking int, Exam char(12), Max_marks_that_can_be_scored int)')
ex(
    'Create table Cutoffs_Male(SerialNo int references College(SerialNo), general float, ST float,OBC float,SC float,EWS float)')
ex(
    'Create table Cutoffs_Female(SerialNo int references College(SerialNo), general float, ST float,OBC float,SC float,EWS float)')
ex(
    'Create table College_contact_details(SerialNo int references College(SerialNo), City char(20), Address1 text, Address2 text, PhoneNo text,Email char(50),Website char(50))')
ex(
    'Create table Exam_info(SerialNo int references College(SerialNo),ExamName char(20),RegistrationDate date,ExamDate date)')

# The following five sections of code take data from the csv file and insert it into the respective table in mysql.Not required after initial run of program.

f = open('College.csv', 'r+', newline='')
readerobj = csv.reader(f)
for i in readerobj:
    ex("Insert into College values({},'{}','{}',{},'{}',{})".format(int(i[0]), i[1], i[2], int(i[3]), i[4], int(i[5])))
con.commit()

f1 = open('Cutoffs_Male.csv', 'r+', newline='')
readerobj = csv.reader(f1)
for i in readerobj:
    ex("Insert into Cutoffs_Male values({},{},{},{},{},{})".format(float(i[0]), float(i[1]), float(i[2]), float(i[3]),
                                                                   float(i[4]), float(i[5])))
con.commit()

f2 = open('Cutoffs_Female.csv', 'r+', newline='')
readerobj = csv.reader(f2)
for i in readerobj:
    ex("Insert into Cutoffs_Female values({},{},{},{},{},{})".format(float(i[0]), float(i[1]), float(i[2]), float(i[3]),
                                                                     float(i[4]), float(i[5])))
con.commit()

f3 = open('College_contact_details.csv', 'r+', newline='')
readerobj = csv.reader(f3)
for i in readerobj:
    ex("Insert into College_contact_details values({},'{}','{}','{}',{},'{}','{}')".format(int(i[0]), i[1], i[2], i[3],
                                                                                           int(i[4]), i[5], i[6]))
con.commit()

f4 = open('Exam_info.csv', 'r+', newline='')
readerobj = csv.reader(f4)
for i in readerobj:
    ex("Insert into Exam_info values('{}','{}','{}','{}')".format(i[0], i[1], i[2], i[3]))
con.commit()
f.close()
f1.close()
f2.close()
f3.close()
f4.close()

listCollege = []
ex('Select CollegeName from College group by collegename')
for i in cursor.fetchall():
    listCollege += i


def List(item):
    """
    Creates a list of college branches based on the college name passed.
    """
    List = []
    ex('select CollegeBranch from College where CollegeName="{}"'.format(item))
    for i in cursor.fetchall():
        List += i
    return List


# ------------Tkinter part---------

# creating the base and labels


def redirect():
    """
    Redirects to the selected window on clicking the button
    """
    opt = r.get()
    if opt == 1:
        open1()
    elif opt == 2:
        open2()
    else:
        open3()


def create_drop1(w, func):
    """
    Creates college and state drop downs
    """
    # Replace with the sql  -done.
    d = {'IIT': List('IIT'), 'BITS': List('BITS'), 'IIIT': List('IIIT'), 'NIT': List('NIT')}

    def create_drop2(x):
        """
        Changes the state drop down box according to the value in the first one
        """
        choice = college.get()
        if choice != '':
            global branch
            branch = tkinter.StringVar()
            branch.set('Choose an option')
            drop2 = tkinter.OptionMenu(w, branch, *d[choice], command=func)
            drop2.config(width=30, pady=10)
            drop2.grid(column=2, row=2)

    college_list = listCollege
    global college
    college = tkinter.StringVar()
    college.set('choose an option')
    drop1 = tkinter.OptionMenu(w, college, *college_list, command=create_drop2)
    drop1.config(width=30, pady=10)
    drop1.grid(column=2, row=1)


def open1():
    """
    Opens the 'Find colleges' Window
    Contains 2 drop downs , College and state, you can only select one
    """
    window2 = tkinter.Toplevel()
    window2.title('College Cutoffs')
    window2.minsize(width=400, height=200)
    window2.config(padx=10, pady=30)

    label1 = tkinter.Label(window2, text='Name of College')
    label1.grid(column=1, row=1, padx=10, pady=30)

    label2 = tkinter.Label(window2, text='State')
    label2.grid(column=1, row=2, padx=20, pady=30)

    def del1(x):  # Deletes second dropdown
        if college.get() != '':
            drop2.grid_remove()

    def del2(x):  # Deletes first dropdown
        if state.get() != '':
            drop1.grid_remove()

    def find():
        output = tkinter.Toplevel()
        output.title('College Cutoffs')
        output.minsize(width=400, height=200)
        output.config(padx=30, pady=30)
        if college.get() != '':  # prints the list of college branches in the selected college using sql commands
            state_label = tkinter.Label(output, text="States:")
            state_label.grid(column=1, row=1)
            ex("select CollegeBranch from College where CollegeName='{}'  ".format(college.get()))
            row = 2
            for i in cursor.fetchall():
                x = str(i)
                x = x[2:len(x) - 3]
                l = tkinter.Label(output, text="{}".format(x))
                l.grid(column=1, row=row)
                row += 1

        if state.get() != '':  # prints the list of colleges  in the selected college branch using sql commands
            college_label = tkinter.Label(output, text="College:")
            college_label.grid(column=1, row=1)
            ex("select CollegeName from College where CollegeBranch='{}'  ".format(state.get()))
            row = 2
            for i in cursor.fetchall():
                x = str(i)
                x = x[2:len(x) - 3]
                l = tkinter.Label(output, text="{}".format(x))
                l.grid(column=1, row=row)
                row += 1

    colleges = listCollege
    college = tkinter.StringVar()
    college.set('choose an option')
    drop1 = tkinter.OptionMenu(window2, college, *colleges, command=del1)
    drop1.config(width=30, pady=10)
    drop1.grid(column=2, row=1)

    states = []
    ex('select distinct CollegeBranch from College')
    for i in cursor.fetchall():
        states += i
    state = tkinter.StringVar()
    state.set('choose an option')
    drop2 = tkinter.OptionMenu(window2, state, *states, command=del2)
    drop2.config(width=30, pady=10)
    drop2.grid(column=2, row=2)

    button = tkinter.Button(window2, text='Search', command=find, padx=10)
    button.grid(column=3, row=4)

    window2.mainloop()


def open2():
    """
    Opens the 'Find cutoffs' window
    Contains 4 drop downs: College, Branch, Gender and Category
    All need to be selected
    """
    window3 = tkinter.Toplevel()
    window3.title('College Cutoffs')
    window3.minsize(width=400, height=200)
    window3.config(padx=10, pady=30)

    label1 = tkinter.Label(window3, text='Name of College')
    label1.grid(column=1, row=1, padx=10, pady=30)

    label2 = tkinter.Label(window3, text='College branch')
    label2.grid(column=1, row=2, padx=20, pady=30)

    label3 = tkinter.Label(window3, text='Gender')
    label3.grid(column=1, row=3, padx=20, pady=30)

    label4 = tkinter.Label(window3, text='Category')
    label4.grid(column=1, row=4, padx=20, pady=30)

    def create_drop3(x):
        global gender
        gender = tkinter.StringVar()
        gender.set('Choose an option')
        drop3 = tkinter.OptionMenu(window3, gender, *['Male', 'Female'], command=create_drop4)
        drop3.config(width=30, pady=10)
        drop3.grid(column=2, row=3)

    def create_drop4(x):
        global category
        category = tkinter.StringVar()
        category.set('Choose an option')
        drop4 = tkinter.OptionMenu(window3, category, *['general', 'SC', 'ST', 'OBC', 'EWS'])
        drop4.config(width=30, pady=10)
        drop4.grid(column=2, row=4)

    def find1():
        """
        prints the cutoff using sql commands.
        """
        output = tkinter.Toplevel()
        output.title('College Cutoffs')
        output.minsize(width=400, height=200)
        output.config(padx=30, pady=30)
        cutoff_label = tkinter.Label(output, text="Cutoff:")
        cutoff_label.grid(column=1, row=1)
        if gender.get() == 'Male':
            ex(
                "select {} from Cutoffs_Male,College where College.SerialNo=Cutoffs_Male.SerialNo and CollegeName='{}' and CollegeBranch='{}'".format(
                    category.get(), college.get(), branch.get()))
            for i in cursor.fetchall():  # cursor.fetchall() returns list of tuples so we use for loop to get the value inside the tuple.
                for j in i:
                    output_label = tkinter.Label(output, text="{}".format(j))
                    output_label.grid(column=2, row=1)

        elif gender.get() == 'Female':
            ex(
                "select {} from Cutoffs_Female,College where College.SerialNo=Cutoffs_Female.SerialNo and CollegeName='{}' and CollegeBranch='{}'".format(
                    category.get(), college.get(), branch.get()))
            for i in cursor.fetchall():
                # cursor.fetchall() returns list of tuples so we use for loop to get the value inside the tuple
                for j in i:
                    output_label = tkinter.Label(output, text="{}".format(j))
                    output_label.grid(column=2, row=1)

    create_drop1(window3, create_drop3)
    button = tkinter.Button(window3, text='Search', command=find1, padx=10)
    button.grid(column=3, row=5)


def open3():
    window4 = tkinter.Toplevel()
    window4.title('College Cutoffs')
    window4.minsize(width=400, height=200)
    window4.config(padx=10, pady=30)

    label1 = tkinter.Label(window4, text='Name of College')
    label1.grid(column=1, row=1, padx=10, pady=30)

    label2 = tkinter.Label(window4, text='College branch')
    label2.grid(column=1, row=2, padx=20, pady=30)

    create_drop1(window4, None)

    def info():
        """
        Prints the college info by using sql commands on the tables College_contact_details and College.
        """

        output = tkinter.Toplevel()
        output.title('College Cutoffs')
        output.minsize(width=400, height=200)
        output.config(padx=30, pady=30)

        ex("select CollegeName,CollegeBranch,Address1,Address2,PhoneNo,Email,Website from College_contact_details,College where College_contact_details.SerialNo=College.SerialNo and CollegeName='{}' and CollegeBranch='{}'".format(
                college.get(), branch.get()))
        r = 1
        name1 = ['College Name', 'College Branch', 'Address', ' ', 'Phone No', 'Email', 'Website']
        for i in cursor.fetchall():
            for j in i:
                output_label1 = tkinter.Label(output, text="{}".format(name1[r - 1]))
                output_label1.grid(column=1, row=r)
                output_label2 = tkinter.Label(output, text="{}".format(j))
                output_label2.grid(column=2, row=r)
                r += 1
        ex(
            "select ExamName,RegistrationDate,ExamDate from Exam_info,College where College.SerialNo=Exam_info.SerialNo and CollegeName='{}' and CollegeBranch='{}'".format(
                college.get(), branch.get()))
        name2 = ['Exam Name', 'Tentative Registration date', 'Tentative Exam date']
        x = 1
        for i in cursor.fetchall():
            for j in i:
                output_label1 = tkinter.Label(output, text="{}".format(name2[x - 1]))
                output_label1.grid(column=1, row=r)
                output_label2 = tkinter.Label(output, text="{}".format(j))
                output_label2.grid(column=2, row=r)
                r += 1


    button = tkinter.Button(window4, text='Search', command=info, padx=10)
    button.grid(column=3, row=5)
    window4.mainloop()


def Guest():
    window = tkinter.Toplevel()
    window.title('College Cutoffs')
    window.minsize(width=400, height=200)
    window.config(padx=60, pady=30)
    global r
    r = tkinter.IntVar()
    tkinter.Radiobutton(window, text='Find colleges', variable=r, value=1, pady=10).grid(column=1, row=2)
    tkinter.Radiobutton(window, text='Find cutoffs  ', variable=r, value=2, pady=10).grid(column=1, row=3)
    tkinter.Radiobutton(window, text='College info  ', variable=r, value=3, pady=10).grid(column=1, row=4)

    label = tkinter.Label(window, text='College cutoffs', pady=10, font=('Arial', 11, 'bold', 'underline'))
    label.grid(column=1, row=1, columnspan=2)
    button = tkinter.Button(window, text="Next", command=redirect, padx=20)
    button.grid(column=2, row=5)
    window.mainloop()


# when Admin button is clicked
def Admin():
    window5 = tkinter.Toplevel()
    window5.title('College Cutoffs')
    window5.geometry("500x500")

    # textboxes
    SerialNo = tkinter.Entry(window5, width=30)
    SerialNo.grid(row=0, column=1, padx=20, pady=(10, 0))  

    CollegeName = tkinter.Entry(window5, width=30)
    CollegeName.grid(row=1, column=1)

    CollegeBranch = tkinter.Entry(window5, width=30)
    CollegeBranch.grid(row=2, column=1)

    NIRFRanking = tkinter.Entry(window5, width=30)
    NIRFRanking.grid(row=3, column=1)

    Exam = tkinter.Entry(window5, width=30)
    Exam.grid(row=4, column=1)

    Max_marks_that_can_be_scored = tkinter.Entry(window5, width=30)
    Max_marks_that_can_be_scored.grid(row=5, column=1)

    # labels
    sl = tkinter.Label(window5, text='Serial No').grid(row=0, column=0, pady=(10, 0))
    cnl = tkinter.Label(window5, text='College Name').grid(row=1, column=0)
    cbl = tkinter.Label(window5, text='College Branch').grid(row=2, column=0)
    nl = tkinter.Label(window5, text='NIRF Ranking').grid(row=3, column=0)
    el = tkinter.Label(window5, text='Exam').grid(row=4, column=0)
    ml = tkinter.Label(window5, text='Max marks that can be scored').grid(row=5, column=0)

    def insert(window5):
        while True:  # input validation
            try:
                SerialNo.get() == int(SerialNo.get())  # ***also make sure its unique and not already in table
                NIRFRanking.get() == int(NIRFRanking.get())
                Max_marks_that_can_be_scored.get() == int(Max_marks_that_can_be_scored.get())
                ex("Insert into College values({},'{}','{}',{},'{}',{})".format(SerialNo.get(), CollegeName.get(),
                                                                                CollegeBranch.get(), NIRFRanking.get(),
                                                                                Exam.get(),
                                                                                Max_marks_that_can_be_scored.get()))
                ex('commit;')
                # clear the textboxes
                SerialNo.delete(0, tkinter.END)
                CollegeName.delete(0, tkinter.END)
                CollegeBranch.delete(0, tkinter.END)
                NIRFRanking.delete(0, tkinter.END)
                Exam.delete(0, tkinter.END)
                Max_marks_that_can_be_scored.delete(0, tkinter.END)
            except:
                messagebox.showerror(title='Error', message='Please enter numbers for fields Serial No, NIRF Ranking and Max marks that can be scored.')
                continue
            break

    def write(table, result):
        with open(table, 'r+', newline='') as f:
            for item in result:
                csv.writer(f).writerow(item)

    def show(table):
        window6 = tkinter.Toplevel()
        window6.title('College Cutoffs')
        window6.geometry("800x500")
        if table == 'College.csv':
            sl = tkinter.Label(window6, text='Serial No').grid(row=0, column=1)
            cnl = tkinter.Label(window6, text='College Name').grid(row=0, column=2)
            cbl = tkinter.Label(window6, text='College Branch').grid(row=0, column=3)
            nl = tkinter.Label(window6, text='NIRF Ranking').grid(row=0, column=4)
            el = tkinter.Label(window6, text='Exam').grid(row=0, column=5)
            ml = tkinter.Label(window6, text='Max marks that can be scored').grid(row=0, column=6)
            ex('select * from college')
        elif table == 'Cutoffs_Male.csv':
            l1 = tkinter.Label(window6, text='Serial No').grid(row=0, column=1)
            l2 = tkinter.Label(window6, text='General Category Cut-off marks').grid(row=0, column=2)
            l3 = tkinter.Label(window6, text='ST ').grid(row=0, column=3)
            l4 = tkinter.Label(window6, text='OBC').grid(row=0, column=4)
            l5 = tkinter.Label(window6, text='SC ').grid(row=0, column=5)
            l6 = tkinter.Label(window6, text='EWS ').grid(row=0, column=6)
            ex('select * from Cutoffs_Male')
        elif table == 'Cutoffs_Female.csv':
            l1 = tkinter.Label(window6, text='Serial No').grid(row=0, column=1)
            l2 = tkinter.Label(window6, text='General Category Cut-off marks').grid(row=0, column=2)
            l3 = tkinter.Label(window6, text='ST ').grid(row=0, column=3)
            l4 = tkinter.Label(window6, text='OBC').grid(row=0, column=4)
            l5 = tkinter.Label(window6, text='SC ').grid(row=0, column=5)
            l6 = tkinter.Label(window6, text='EWS ').grid(row=0, column=6)
            ex('select * from Cutoffs_Female')

        result = cursor.fetchall()
        r = 1  # row counter
        for rec in result:
            c = 1  # column counter
            for item in rec:
                lbl = tkinter.Label(window6, text=item).grid(row=r, column=c)
                c += 1
            r += 1

        save = tkinter.Button(window6, text='Write all records to csv file', command=lambda: write(table,
                                                                                                   result))  # using lambda because we want to pass values. just using write(result) won't work
        save.grid(row=r + 1, column=0)

    # insert button
    s = tkinter.Button(window5, text="Insert record in College table in MYSql database",
                       command=lambda: insert(window5))
    s.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    # show colleges
    c = tkinter.Button(window5, text="Show all records in college table", command=lambda: show('College.csv')).grid(
        row=7, column=0)
    c1 = tkinter.Button(window5, text="Show all records in cutoffs_female table",
                        command=lambda: show('Cutoffs_Female.csv')).grid(row=7, column=2)
    c2 = tkinter.Button(window5, text="Show all records in cutoffs_male table",
                        command=lambda: show('Cutoffs_Male.csv')).grid(row=8, column=2)

    # delete button
    dlabel = tkinter.Label(window5, text="Enter Sno of record to be deleted:").grid(row=8, column=0)
    dbox = tkinter.Entry(window5, width=30)
    dbox.grid(row=8, column=1)
    d = tkinter.Button(window5, text='Delete',
                       command=lambda: delete('college', dbox.get()))  # using lambda because we want to pass values.
    d.grid(row=9, column=0)

    def delete(table, Sno):
        ex("delete from '{}' where SerialNo={}".format(table, Sno))
        ex('commit;')
        # clear the textbox
        dbox.delete(0, tkinter.END)

    # table cutoff_male/female
    SerialNo = tkinter.Entry(window5, width=30)
    SerialNo.grid(row=0, column=3, padx=20, pady=(10, 0))
    general = tkinter.Entry(window5, width=30)
    general.grid(row=1, column=3, padx=20, pady=(10, 0))
    ST = tkinter.Entry(window5, width=30)
    ST.grid(row=2, column=3, padx=20, pady=(10, 0))
    OBC = tkinter.Entry(window5, width=30)
    OBC.grid(row=3, column=3, padx=20, pady=(10, 0))
    SC = tkinter.Entry(window5, width=30)
    SC.grid(row=4, column=3, padx=20, pady=(10, 0))
    EWS = tkinter.Entry(window5, width=30)
    EWS.grid(row=5, column=3, padx=20, pady=(10, 0))

    l1 = tkinter.Label(window5, text='Serial No').grid(row=0, column=2, pady=(10, 0))
    l2 = tkinter.Label(window5, text='General Category Cut-off marks').grid(row=1, column=2)
    l3 = tkinter.Label(window5, text='ST Cut-off marks').grid(row=2, column=2)
    l4 = tkinter.Label(window5, text='OBC Cut-off marks').grid(row=3, column=2)
    l5 = tkinter.Label(window5, text='SC Cut-off marks').grid(row=4, column=2)
    l6 = tkinter.Label(window5, text='EWS Cut-off marks').grid(row=5, column=2)

    # contact details
    # exam

    window5.mainloop()

    # when admin button is clicked


def table1():
    window5 = tkinter.Toplevel()
    window5.title('College Cutoffs')
    window5.geometry("1200x600")
    row = 0
    # textboxes
    SerialNo = tkinter.Entry(window5, width=30)
    SerialNo.grid(row=0, column=1, padx=20, pady=(10, 0))  # https://automatetheboringstuff.com/2e/chapter8/

    CollegeName = tkinter.Entry(window5, width=30)
    CollegeName.grid(row=1, column=1)

    CollegeBranch = tkinter.Entry(window5, width=30)
    CollegeBranch.grid(row=2, column=1)

    NIRFRanking = tkinter.Entry(window5, width=30)
    NIRFRanking.grid(row=3, column=1)

    Exam = tkinter.Entry(window5, width=30)
    Exam.grid(row=4, column=1)

    Max_marks_that_can_be_scored = tkinter.Entry(window5, width=30)
    Max_marks_that_can_be_scored.grid(row=5, column=1)
    # labels
    sl = tkinter.Label(window5, text='Serial No').grid(row=0, column=0, pady=(10, 0))
    cnl = tkinter.Label(window5, text='College Name').grid(row=1, column=0)
    cbl = tkinter.Label(window5, text='College Branch').grid(row=2, column=0)
    nl = tkinter.Label(window5, text='NIRF Ranking').grid(row=3, column=0)
    el = tkinter.Label(window5, text='Exam').grid(row=4, column=0)
    ml = tkinter.Label(window5, text='Max marks that can be scored').grid(row=5, column=0)

    def insert():
        while True:  # input validation
            try:
                SerialNo.get() == int(SerialNo.get())  # ***also make sure its unique and not already in table
                NIRFRanking.get() == int(NIRFRanking.get())
                Max_marks_that_can_be_scored.get() == int(Max_marks_that_can_be_scored.get())
                ex("Insert into College values({},'{}','{}',{},'{}',{})".format(SerialNo.get(), CollegeName.get(),
                                                                                CollegeBranch.get(), NIRFRanking.get(),
                                                                                Exam.get(),
                                                                                Max_marks_that_can_be_scored.get()))
                ex('commit;')
                # clear the textboxes
                SerialNo.delete(0, tkinter.END)
                CollegeName.delete(0, tkinter.END)
                CollegeBranch.delete(0, tkinter.END)
                NIRFRanking.delete(0, tkinter.END)
                Exam.delete(0, tkinter.END)
                Max_marks_that_can_be_scored.delete(0, tkinter.END)
            except:
                messagebox.showerror(title='Error', message='Please enter numbers for fields Serial No, NIRF Ranking and Max marks that can be scored.')
                continue
            break

    def show(file, table, fields):
        window6 = tkinter.Toplevel()
        window6.title('College Cutoffs')
        window6.geometry("800x500")
        col = 1  # column counter
        for i in fields:
            l = tkinter.Label(window6, text=i).grid(row=0, column=col)
            col += 1

        ex('select * from {}'.format(table))
        result = cursor.fetchall()
        r = 1  # row counter
        for rec in result:
            c = 1  # column counter
            for item in rec:
                lbl = tkinter.Label(window6, text=item).grid(row=r, column=c)
                c += 1
            r += 1

        save = tkinter.Button(window6, text='Write all records to csv file', command=lambda: write(file,
                                                                                                   result))  # using lambda because we want to pass values. just using write(result) won't work
        save.grid(row=r + 1, column=0)

    # insert button
    s = tkinter.Button(window5, text="Insert record in College table in MYSql database", command=lambda: insert)
    s.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    # show colleges
    c = tkinter.Button(window5, text="Show all records in college table", command=lambda: show('College.csv', 'College',
                                                                                               ['Serial No',
                                                                                                'College Name',
                                                                                                'College Branch',
                                                                                                'NIRF Ranking', 'Exam',
                                                                                                'Max marks that can be scored'])).grid(
        row=7, column=0)

    # delete button
    dlabel = tkinter.Label(window5, text="Enter Sno of record to be deleted:").grid(row=8, column=0)
    dbox = tkinter.Entry(window5, width=30)
    dbox.grid(row=8, column=1)
    d = tkinter.Button(window5, text='Delete',
                       command=lambda: delete('college', dbox.get()))  # using lambda because we want to pass values.
    d.grid(row=9, column=0)

    def delete(table, Sno):
        ex("delete from '{}' where SerialNo={}".format(table, Sno))
        ex('commit;')
        # clear the textbox
        dbox.delete(0, tkinter.END)

    window5.mainloop()


def admin():
    root = tkinter.Tk()
    root.title("College cutoff")
    root.configure(width=500, height=300)
    root.configure(bg="green")
    v = tkinter.IntVar()
    common_bg = '#' + ''.join([hex(x)[2:].zfill(2) for x in (181, 26, 18)])  # RGB in dec
    common_fg = '#ffffff'  # pure white
    tkinter.Label(root, text="""WHICH TABLE DO YOU WISH TO UPDATE""", justify=tkinter.CENTER, padx=20).pack()
    tkinter.Radiobutton(root, text="COLLEGE", variable=v, value=1, padx=20, command=table1, fg=common_fg, bg=common_bg,
                        activebackground=common_bg, activeforeground=common_fg, selectcolor=common_bg).pack(
        anchor=tkinter.W)
    tkinter.Radiobutton(root, text="CUTOFF-MALE", variable=v, value=2, padx=20, command=Guest).pack(anchor=tkinter.W)
    tkinter.Radiobutton(root, text="CUTOFF-FEMALE", variable=v, value=1, padx=20, command=Guest).pack(anchor=tkinter.W)
    tkinter.Radiobutton(root, text="COLLEGE CONTACT DETAILS", variable=v, value=1, padx=20, command=Guest).pack(
        anchor=tkinter.W)
    tkinter.Radiobutton(root, text="EXAM-DETAILS", variable=v, value=1, padx=20, command=Guest).pack(anchor=tkinter.W)
    root.mainloop()


# checks if user is admin or guest
# __main__
root = tkinter.Tk()
root.title("Login")
v = tkinter.IntVar()
tkinter.Label(root, text="""ARE YOU AN ADMIN OR A GUEST?""", justify=tkinter.LEFT, padx=20).pack()
tkinter.Radiobutton(root, text="Guest", variable=v, value=1, padx=20, command=Guest).pack(anchor=tkinter.W)
tkinter.Radiobutton(root, text="Admin", variable=v, value=2, padx=20, command=admin).pack(anchor=tkinter.W)
root.mainloop()
