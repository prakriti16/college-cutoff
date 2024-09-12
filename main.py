#College cutoff
#Prerequisites: right click and download the 5 csv files from drive (make sure they are in the same location in your computer as this python program.)
import csv
import tkinter
from tkinter import messagebox
import mysql.connector


con = mysql.connector.connect(
    host='localhost', password='root', user='root'
)  #type your own host name, password and user name in place of the strings in quotes.
cursor = con.cursor()


def ex(query):
    """
  Executes the mysql query that is passed.
  """
    cursor.execute(query)


ex('Drop database IF EXISTS Collegecutoff')
ex('Create database Collegecutoff')
ex('Use Collegecutoff')
ex('Create table College(SerialNo int primary key,CollegeName char(30),CollegeBranch char(30),NIRFRanking int, Exam char(20), Max_marks_that_can_be_scored int)'
   )
ex('Create table Cutoffs_Male(SerialNo int references College(SerialNo), general float, ST float,OBC float,SC float,EWS float)'
   )
ex('Create table Cutoffs_Female(SerialNo int references College(SerialNo), general float, ST float,OBC float,SC float,EWS float)'
   )
ex('Create table College_contact_details(SerialNo int references College(SerialNo), City char(40), Address1 text,Address2 text,PhoneNo text,Email char(50),Website char(50))'
   )
ex('Create table Exam_info(SerialNo int references College(SerialNo),ExamName char(30),RegistrationDate date,ExamDate date)'
   )

#The following five sections of code take data from the csv file and insert it into the respective table in mysql.Not required after initial run of program.

f = open('College.csv', 'r+', newline='')
readerobj = csv.reader(f)
for i in readerobj:
    ex("Insert into College values({},'{}','{}',{},'{}',{})".format(
        int(i[0]), i[1], i[2], int(i[3]), i[4], int(i[5])))
con.commit()

f1 = open('Cutoffs_Male.csv', 'r+', newline='')
readerobj = csv.reader(f1)
for i in readerobj:
    ex("Insert into Cutoffs_Male values({},{},{},{},{},{})".format(
        float(i[0]), float(i[1]), float(i[2]), float(i[3]), float(i[4]),
        float(i[5])))
con.commit()

f2 = open('Cutoffs_Female.csv', 'r+', newline='')
readerobj = csv.reader(f2)
for i in readerobj:
    ex("Insert into Cutoffs_Female values({},{},{},{},{},{})".format(
        float(i[0]), float(i[1]), float(i[2]), float(i[3]), float(i[4]),
        float(i[5])))
con.commit()

f3 = open('College_contact_details.csv', 'r+', newline='')
readerobj = csv.reader(f3)
for i in readerobj:
    ex("Insert into College_contact_details values({},'{}','{}','{}','{}','{}','{}')"
       .format(int(i[0]), i[1], i[2], i[3], i[4], i[5], i[6]))
con.commit()

f4 = open('Exam_info.csv', 'r+', newline='')
readerobj = csv.reader(f4)
for i in readerobj:
    ex("Insert into Exam_info values('{}','{}','{}','{}')".format(
        i[0], i[1], i[2], i[3]))
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


#------------Tkinter part---------
BLACK = '#121212'
WHITE = '#FFFFFF'
PURP = '#BB86FC'
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
            drop2.config(width=30, pady=10, bg=PURP, activebackground=PURP)
            drop2.grid(column=2, row=2)

    college_list = listCollege
    global college
    college = tkinter.StringVar()
    college.set('choose an option')
    drop1 = tkinter.OptionMenu(w, college, *college_list, command=create_drop2)
    drop1.config(width=30, pady=10, bg=PURP, activebackground=PURP)
    drop1.grid(column=2, row=1)

def open1():
    """
    Opens the 'Find colleges' Window
    Contains 2 drop downs , College and state, you can only select one
    """
    window2 = tkinter.Toplevel()
    window2.title('College Cutoffs')
    window2.minsize(width=400, height=200)
    window2.config(padx=10, pady=30, bg=BLACK)

    label1 = tkinter.Label(window2, text='Name of College', bg=BLACK, fg=WHITE)
    label1.grid(column=1, row=1, padx=10, pady=30)

    label2 = tkinter.Label(window2, text='State/City', bg=BLACK, fg=WHITE)
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
        output.config(padx=30, pady=30, bg=BLACK)
        if college.get() != 'choose an option':  # prints the list of college branches in the selected college using sql commands
            state_label = tkinter.Label(output, text="States:", font=('Arial', 11, 'bold', 'underline'))
            state_label.config(bg=BLACK, fg=PURP)
            state_label.grid(column=1, row=1)
            ex("select CollegeBranch from College where CollegeName='{}'  ".format(college.get()))
            row = 2
            for i in cursor.fetchall():
                x = str(i)
                x = x[2:len(x) - 3]
                l = tkinter.Label(output, text="{}".format(x))
                l.config(bg=BLACK, fg=WHITE)
                l.grid(column=1, row=row)
                row += 1

        if state.get() != 'choose an option':  # prints the list of colleges  in the selected college branch using sql commands
            college_label = tkinter.Label(output, text="Colleges:", font=('Arial', 11, 'bold', 'underline'))
            college_label.config(bg=BLACK, fg=PURP)
            college_label.grid(column=1, row=1)
            ex("select CollegeName from College where CollegeBranch='{}'  ".format(state.get()))
            row = 2
            for i in cursor.fetchall():
                x = str(i)
                x = x[2:len(x) - 3]
                l = tkinter.Label(output, text="{}".format(x))
                l.config(bg=BLACK, fg=WHITE)
                l.grid(column=1, row=row)
                row += 1

    colleges = listCollege
    college = tkinter.StringVar()
    college.set('choose an option')
    drop1 = tkinter.OptionMenu(window2, college, *colleges, command=del1)
    drop1.config(width=30, pady=10, bg=PURP, activebackground=PURP)
    drop1.grid(column=2, row=1)

    states = []
    ex('select distinct CollegeBranch from College')
    for i in cursor.fetchall():
        states += i
    state = tkinter.StringVar()
    state.set('choose an option')
    drop2 = tkinter.OptionMenu(window2, state, *states, command=del2)
    drop2.config(width=30, pady=10, bg=PURP, activebackground=PURP)
    drop2.grid(column=2, row=2)

    button = tkinter.Button(window2, text='Search', command=find, padx=10, bg=PURP, activebackground=PURP)
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
    window3.config(padx=10, pady=30, bg=BLACK)

    label1 = tkinter.Label(window3, text='Name of College')
    label1.config(padx=10, pady=30, bg=BLACK, fg=WHITE)
    label1.grid(column=1, row=1)

    label2 = tkinter.Label(window3, text='College branch')
    label2.config(padx=20, pady=30, bg=BLACK, fg=WHITE)
    label2.grid(column=1, row=2)

    label3 = tkinter.Label(window3, text='Gender')
    label3.config(padx=20, pady=30, bg=BLACK, fg=WHITE)
    label3.grid(column=1, row=3)

    label4 = tkinter.Label(window3, text='Category')
    label4.config(padx=20, pady=30, bg=BLACK, fg=WHITE)
    label4.grid(column=1, row=4)


    def create_drop3(x):
        global gender
        gender = tkinter.StringVar()
        gender.set('Choose an option')
        drop3 = tkinter.OptionMenu(window3, gender, *['Male', 'Female'], command=create_drop4)
        drop3.config(width=30, pady=10, bg=PURP, activebackground=PURP)
        drop3.grid(column=2, row=3)

    def create_drop4(x):
        global category
        category = tkinter.StringVar()
        category.set('Choose an option')
        drop4 = tkinter.OptionMenu(window3, category, *['General', 'SC', 'ST', 'OBC', 'EWS'])
        drop4.config(width=30, pady=10, bg=PURP, activebackground=PURP)
        drop4.grid(column=2, row=4)

    def find1():
        """
        prints the cutoff using sql commands.
        """
        output = tkinter.Toplevel()
        output.title('College Cutoffs')
        output.minsize(width=400, height=200)
        output.config(padx=30, pady=30, bg=BLACK)
        cutoff_label = tkinter.Label(output, text="Cutoff:")
        cutoff_label.config(bg=BLACK, fg=PURP)
        cutoff_label.grid(column=1, row=2)

        header_Label = tkinter.Label(output, text="{}\t|\t{}\t|\t{}\t|\t{}".format(college.get(), branch.get(), gender.get(), category.get()))
        header_Label.config(bg=BLACK, fg=PURP, pady=20)
        header_Label.grid(column=1, columnspan=2, row=1)

        if gender.get() == 'Male':
            ex(
                "select {} from Cutoffs_Male,College where College.SerialNo=Cutoffs_Male.SerialNo and CollegeName='{}' and CollegeBranch='{}'".format(
                    category.get(), college.get(), branch.get()))
            for i in cursor.fetchall():  # cursor.fetchall() returns list of tuples so we use for loop to get the value inside the tuple.
                for j in i:
                    output_label = tkinter.Label(output, text="{}".format(j))
                    output_label.config(bg=BLACK, fg=WHITE)
                    output_label.grid(column=2, row=2)

        elif gender.get() == 'Female':
            ex(
                "select {} from Cutoffs_Female,College where College.SerialNo=Cutoffs_Female.SerialNo and CollegeName='{}' and CollegeBranch='{}'".format(
                    category.get(), college.get(), branch.get()))
            for i in cursor.fetchall():
                # cursor.fetchall() returns list of tuples so we use for loop to get the value inside the tuple
                for j in i:
                    output_label = tkinter.Label(output, text="{}".format(j))
                    output_label.config(bg=BLACK, fg=WHITE)
                    output_label.grid(column=2, row=2)

    create_drop1(window3, create_drop3)
    button = tkinter.Button(window3, text='Search', command=find1, padx=10, bg=PURP, activebackground=PURP)
    button.grid(column=3, row=5)


def open3():
    window4 = tkinter.Toplevel()
    window4.title('College Cutoffs')
    window4.minsize(width=400, height=200)
    window4.config(padx=10, pady=30, bg=BLACK)

    label1 = tkinter.Label(window4, text='Name of College')
    label1.config(padx=10, pady=30, bg=BLACK, fg=WHITE)
    label1.grid(column=1, row=1)

    label2 = tkinter.Label(window4, text='College branch')
    label2.config(padx=20, pady=30, bg=BLACK, fg=WHITE)
    label2.grid(column=1, row=2)

    create_drop1(window4, None)

    def info():
        """
        Prints the college info by using sql commands on the tables College_contact_details and College.
        """

        output = tkinter.Toplevel()
        output.title('College Cutoffs')
        output.minsize(width=400, height=200)
        output.config(padx=30, pady=30, bg=BLACK)

        ex(
            "select CollegeName,CollegeBranch,Address1,Address2,PhoneNo,Email,Website from College_contact_details,College where College_contact_details.SerialNo=College.SerialNo and CollegeName='{}' and CollegeBranch='{}'".format(
                college.get(), branch.get()))
        r = 1
        name1 = ['College Name', 'College Branch', 'Address', ' ', 'Phone No', 'Email', 'Website']
        for i in cursor.fetchall():
            for j in i:
                output_label1 = tkinter.Label(output, text="{}".format(name1[r - 1]))
                output_label1.config(bg=BLACK, fg=PURP)
                output_label1.grid(column=1, row=r)
                output_label2 = tkinter.Label(output, text="{}".format(j))
                output_label2.config(bg=BLACK, fg=WHITE)
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
                output_label1.config(bg=BLACK, fg=PURP)
                output_label1.grid(column=1, row=r)
                output_label2 = tkinter.Label(output, text="{}".format(j))
                output_label2.config(bg=BLACK, fg=WHITE)
                output_label2.grid(column=2, row=r)
                r += 1
                x += 1

    button = tkinter.Button(window4, text='Search', command=info, padx=10, bg=PURP, activebackground=PURP)
    button.grid(column=3, row=5)
    window4.mainloop()


def Guest():
    window = tkinter.Toplevel()
    window.title('College Cutoffs')
    window.minsize(width=400, height=200)
    window.config(padx=60, pady=30, bg=BLACK)
    global r
    r = tkinter.IntVar()
    tkinter.Radiobutton(window, text='Find colleges', variable=r, value=1, pady=10, bg=BLACK, fg=WHITE,command=redirect, activebackground=BLACK, activeforeground=PURP).grid(column=1, row=2)
    tkinter.Radiobutton(window, text='Find cutoffs  ', variable=r, value=2, pady=10, bg=BLACK, fg=WHITE,command=redirect, activebackground=BLACK, activeforeground=PURP).grid(column=1, row=3)
    tkinter.Radiobutton(window, text='College info  ', variable=r, value=3, pady=10, bg=BLACK, fg=WHITE,command=redirect, activebackground=BLACK, activeforeground=PURP).grid(column=1, row=4)

    label = tkinter.Label(window, text='College cutoffs', pady=10, font=('Arial', 11, 'bold', 'underline'), bg=BLACK, fg=PURP)
    label.grid(column=1, row=1, columnspan=2)
    #button = tkinter.Button(window, text="Next", command=redirect, padx=20, bg=PURP, fg=BLACK, activebackground=PURP)
    #button.grid(column=2, row=5)
    window.mainloop()


#------------------------------Admin part----------------------------------

def show(file, table, fields):
    window6 = tkinter.Toplevel()
    window6.title('College Cutoffs')
    window6.geometry("1200x500")
    window6.config(bg=BLACK)
    col = 1  # column counter
    for i in fields:
        l = tkinter.Label(window6, text=i)
        l.config(bg=BLACK, fg=PURP)
        l.grid(row=0, column=col)
        col += 1

    ex('select * from {}'.format(table))
    result = cursor.fetchall()
    r = 1  # row counter
    for rec in result:
        c = 1  # column counter
        for item in rec:
            lbl = tkinter.Label(window6, text=item)
            lbl.config(bg=BLACK, fg=WHITE)
            lbl.grid(row=r, column=c)
            c += 1
        r += 1

    
def validnum(inp):  #validates input to only allow numbers
    if inp.isdigit():
        return True
    else:
        return False



def delete(dbox,table,Sno):
      ex('select SerialNo from {}'.format(table))
      l=''
      for i in cursor.fetchall():
        for j in i:
          l+=str(i)
      if dbox.get()=='':
        messagebox.showerror(title='Error',message='Enter a value!')
      else:    
        ex("delete from {} where SerialNo={}".format(table,Sno))
        ex('commit;')
        if str(Sno) not in l:
          messagebox.showerror(title='Error',message='Serial number not found!')
        else:
          messagebox.showinfo("Success!", "Record deleted!")

#when Admin button is clicked
def table1():
    window5 = tkinter.Toplevel()
    window5.title('COLLEGE')
    window5.geometry("500x400")
    window5.config(bg=BLACK)

    reg = window5.register(validnum)
    # textboxes
    SerialNo = tkinter.Entry(window5, width=30)
    SerialNo.grid(row=0, column=1, padx=20, pady=(10, 0))
    SerialNo.config(validate='key', validatecommand=(reg, '%P'))

    CollegeName = tkinter.Entry(window5, width=30)
    CollegeName.grid(row=1, column=1)

    CollegeBranch = tkinter.Entry(window5, width=30)
    CollegeBranch.grid(row=2, column=1)

    NIRFRanking = tkinter.Entry(window5, width=30)
    NIRFRanking.grid(row=3, column=1)
    NIRFRanking.config(validate='key', validatecommand=(reg, '%P'))

    Exam = tkinter.Entry(window5, width=30)
    Exam.grid(row=4, column=1)

    Max_marks_that_can_be_scored = tkinter.Entry(window5, width=30)
    Max_marks_that_can_be_scored.grid(row=5, column=1)
    Max_marks_that_can_be_scored.config(validate='key', validatecommand=(reg, '%P'))
    # labels
    sl = tkinter.Label(window5, text='Serial No', bg=BLACK, fg=WHITE).grid(row=0, column=0, pady=(10, 0))
    cnl = tkinter.Label(window5, text='College Name', bg=BLACK, fg=WHITE).grid(row=1, column=0)
    cbl = tkinter.Label(window5, text='College Branch', bg=BLACK, fg=WHITE).grid(row=2, column=0)
    nl = tkinter.Label(window5, text='NIRF Ranking', bg=BLACK, fg=WHITE).grid(row=3, column=0)
    el = tkinter.Label(window5, text='Exam', bg=BLACK, fg=WHITE).grid(row=4, column=0)
    ml = tkinter.Label(window5, text='Max marks that can be scored', bg=BLACK, fg=WHITE).grid(row=5, column=0)

    def insert():
        done = True
        ex('select SerialNo from college')
        l = cursor.fetchall()
        if SerialNo.get() == '' or CollegeName.get() == '' or CollegeBranch.get() == '' or NIRFRanking.get() == '' or Exam.get() == '' or Max_marks_that_can_be_scored.get() == '':
            messagebox.showerror(title='Error', message='Enter values in all fields!')
            done = False
        else:
            for j in l:  # fetching int from tuple from list returned by fetchall
                for i in j:
                    if int(SerialNo.get()) == i:
                        messagebox.showerror(title='Error', message='Sorry that serial number is taken!')
                        done = False
        if done == True:
            ex("Insert into College values({},'{}','{}',{},'{}',{})".format(SerialNo.get(), CollegeName.get(),CollegeBranch.get(), NIRFRanking.get(),Exam.get(),Max_marks_that_can_be_scored.get()))
            ex('commit;')
            messagebox.showinfo("Success!", "Record added!")

    # insert button
    s = tkinter.Button(window5, text="Add record", command=insert)
    s.config(bg=PURP, activebackground=PURP)
    s.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    # show colleges
    c = tkinter.Button(window5, text="Show all records", command=lambda: show('College.csv', 'College',
                                                                                               ['Serial No',
                                                                                                'College Name',
                                                                                                'College Branch',
                                                                                                'NIRF Ranking', 'Exam',
                                                                                                'Max marks that can be scored']))
    c.config(bg=PURP, activebackground=PURP)
    c.grid(row=7, column=0)

    # delete button
    dlabel = tkinter.Label(window5, text="Enter Sno of record to be deleted:")
    dlabel.config(bg=BLACK, fg=WHITE)
    dlabel.grid(row=8, column=0)
    dbox = tkinter.Entry(window5, width=30)
    dbox.grid(row=8, column=1)
    dbox.config(validate='key', validatecommand=(reg, '%P'))

    d = tkinter.Button(window5, text='Delete', command=lambda: delete(dbox, 'college',
                                                                      dbox.get()))  # using lambda because we want to pass values.
    d.config(bg=PURP, activebackground=PURP)
    d.grid(row=9, column=0)

    window5.mainloop()


def table2():  # table cutoffs_male
    window5 = tkinter.Toplevel()
    window5.title('CUTOFFS-MALE')
    window5.geometry("500x500")
    window5.config(bg=BLACK)

    # textboxes
    SerialNo = tkinter.Entry(window5, width=30)
    SerialNo.grid(row=0, column=1, padx=20, pady=(10, 0))
    reg = window5.register(validnum)  # validation
    SerialNo.config(validate='key', validatecommand=(reg, '%P'))
    general = tkinter.Entry(window5, width=30)
    general.grid(row=1, column=1, padx=20, pady=(10, 0))
    ST = tkinter.Entry(window5, width=30)
    ST.grid(row=2, column=1, padx=20, pady=(10, 0))
    OBC = tkinter.Entry(window5, width=30)
    OBC.grid(row=3, column=1, padx=20, pady=(10, 0))
    SC = tkinter.Entry(window5, width=30)
    SC.grid(row=4, column=1, padx=20, pady=(10, 0))
    EWS = tkinter.Entry(window5, width=30)
    EWS.grid(row=5, column=1, padx=20, pady=(10, 0))
    # labels
    l1 = tkinter.Label(window5, text='Serial No', bg=BLACK, fg=WHITE).grid(row=0, column=0, pady=(10, 0))
    l2 = tkinter.Label(window5, text='General', bg=BLACK, fg=WHITE).grid(row=1, column=0)
    l3 = tkinter.Label(window5, text='ST ', bg=BLACK, fg=WHITE).grid(row=2, column=0)
    l4 = tkinter.Label(window5, text='OBC', bg=BLACK, fg=WHITE).grid(row=3, column=0)
    l5 = tkinter.Label(window5, text='SC', bg=BLACK, fg=WHITE).grid(row=4, column=0)
    l6 = tkinter.Label(window5, text='EWS', bg=BLACK, fg=WHITE).grid(row=5, column=0)

    def insert():
        done = True
        l1 = SerialNo.get(), general.get(), ST.get(), OBC.get(), SC.get(), EWS.get()
        for j in l1:
            if j == '':
                done = False
                messagebox.showerror(title='Error', message='Enter values in all fields!')
                break
            else:
                ex('select SerialNo from cutoffs_male')
                l = cursor.fetchall()
                for j in l:  # fetching int from tuple from list returned by fetchall
                    for i in j:
                        if int(SerialNo.get()) == i:
                            messagebox.showerror(title='Error', message='Sorry that serial number is taken!')
                            done = False
        if done == True:
            ex("Insert into cutoffs_male values({},{},{},{},{},{})".format(SerialNo.get(), general.get(), ST.get(),OBC.get(), SC.get(), EWS.get()))
            ex('commit;')
            messagebox.showinfo("Success!", "Record added!")

    # insert button
    s = tkinter.Button(window5, text="Add record", command=insert)
    s.config(bg=PURP, activebackground=PURP)
    s.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    # show cutoffs
    c = tkinter.Button(window5, text="Show all records",command=lambda: show('Cutoffs_Male.csv', 'Cutoffs_male', ['Serial No', 'General', 'ST', 'OBC', 'SC', 'EWS']))
    c.config(bg=PURP, activebackground=PURP)
    c.grid(row=7, column=0)

    # delete button
    dlabel = tkinter.Label(window5, text="Enter Sno of record to be deleted:", bg=BLACK, fg=WHITE).grid(row=8, column=0)
    dbox = tkinter.Entry(window5, width=30)
    dbox.grid(row=8, column=1)
    dbox.config(validate='key', validatecommand=(reg, '%P'))
    d = tkinter.Button(window5, text='Delete', command=lambda: delete(dbox, 'Cutoffs_male',dbox.get()))  # using lambda because we want to pass values.
    d.config(bg=PURP, activebackground=PURP)
    d.grid(row=9, column=0)

    window5.mainloop()


def table3():  # table cutoff_female
    window5 = tkinter.Toplevel()
    window5.title('CUTOFFS-FEMALE')
    window5.geometry("500x300")
    window5.config(bg=BLACK)
    # textboxes
    SerialNo = tkinter.Entry(window5, width=30)
    SerialNo.grid(row=0, column=1, padx=20, pady=(10, 0))
    reg = window5.register(validnum)  # validation
    SerialNo.config(validate='key', validatecommand=(reg, '%P'))
    general = tkinter.Entry(window5, width=30)
    general.grid(row=1, column=1, padx=20, pady=(10, 0))
    ST = tkinter.Entry(window5, width=30)
    ST.grid(row=2, column=1, padx=20, pady=(10, 0))
    OBC = tkinter.Entry(window5, width=30)
    OBC.grid(row=3, column=1, padx=20, pady=(10, 0))
    SC = tkinter.Entry(window5, width=30)
    SC.grid(row=4, column=1, padx=20, pady=(10, 0))
    EWS = tkinter.Entry(window5, width=30)
    EWS.grid(row=5, column=1, padx=20, pady=(10, 0))
    # labels
    l1 = tkinter.Label(window5, text='Serial No', bg=BLACK, fg=WHITE).grid(row=0, column=0, pady=(10, 0))
    l2 = tkinter.Label(window5, text='General', bg=BLACK, fg=WHITE).grid(row=1, column=0)
    l3 = tkinter.Label(window5, text='ST ', bg=BLACK, fg=WHITE).grid(row=2, column=0)
    l4 = tkinter.Label(window5, text='OBC', bg=BLACK, fg=WHITE).grid(row=3, column=0)
    l5 = tkinter.Label(window5, text='SC', bg=BLACK, fg=WHITE).grid(row=4, column=0)
    l6 = tkinter.Label(window5, text='EWS', bg=BLACK, fg=WHITE).grid(row=5, column=0)

    def insert():
        done = True
        l1 = SerialNo.get(), general.get(), ST.get(), OBC.get(), SC.get(), EWS.get()
        for j in l1:
            if j == '':
                done = False
                messagebox.showerror(title='Error', message='Enter values in all fields!')
                break
            else:
                ex('select SerialNo from cutoffs_female')
                l = cursor.fetchall()
                for j in l:  # fetching int from tuple from list of SerialNo returned by fetchall
                    for i in j:
                        if int(SerialNo.get()) == i:
                            messagebox.showerror(title='Error', message='Sorry that serial number is taken!')
                            done = False
        if done == True:
            ex("Insert into cutoffs_female values({},{},{},{},{},{})".format(SerialNo.get(), general.get(), ST.get(),OBC.get(), SC.get(), EWS.get()))
            ex('commit;')
            messagebox.showinfo("Success!", "Record added!")

    # insert button
    s = tkinter.Button(window5, text="Add record", command=insert)
    s.config(bg=PURP, activebackground=PURP)
    s.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
    # show cutoffs
    c = tkinter.Button(window5, text="Show all records",command=lambda: show('Cutoffs_Female.csv', 'Cutoffs_female', ['Serial No', 'General', 'ST', 'OBC', 'SC', 'EWS']))
    c.config(bg=PURP, activebackground=PURP)
    c.grid(row=7, column=0)
    # delete button
    dlabel = tkinter.Label(window5, text="Enter Sno of record to be deleted:")
    dlabel.config(bg=BLACK, fg=WHITE)
    dlabel.grid(row=8, column=0)
    dbox = tkinter.Entry(window5, width=30)
    dbox.grid(row=8, column=1)
    d = tkinter.Button(window5, text='Delete', command=lambda: delete(dbox, 'Cutoffs_female',dbox.get()))  # using lambda because we want to pass values.
    d.config(bg=PURP, activebackground=PURP)
    d.grid(row=9, column=0)

    window5.mainloop()


def table4():  # contact details
    window5 = tkinter.Toplevel()
    window5.title('COLLEGE CONTACT DETAILS')
    window5.geometry("500x500")
    window5.config(bg=BLACK)
    # textboxes
    SerialNo = tkinter.Entry(window5, width=30)
    SerialNo.grid(row=0, column=1, padx=20, pady=(10, 0))
    reg = window5.register(validnum)  # validation
    SerialNo.config(validate='key', validatecommand=(reg, '%P'))
    City = tkinter.Entry(window5, width=30)
    City.grid(row=1, column=1, padx=20, pady=(10, 0))
    Address1 = tkinter.Entry(window5, width=30)
    Address1.grid(row=2, column=1, padx=20, pady=(10, 0))
    Address2 = tkinter.Entry(window5, width=30)
    Address2.grid(row=3, column=1, padx=20, pady=(10, 0))
    PhoneNo = tkinter.Entry(window5, width=30)
    PhoneNo.grid(row=4, column=1, padx=20, pady=(10, 0))
    Email = tkinter.Entry(window5, width=30)
    Email.grid(row=5, column=1, padx=20, pady=(10, 0))
    Website = tkinter.Entry(window5, width=30)
    Website.grid(row=6, column=1, padx=20, pady=(10, 0))
    # labels
    l1 = tkinter.Label(window5, text='Serial No', bg=BLACK, fg=WHITE).grid(row=0, column=0, pady=(10, 0))
    l2 = tkinter.Label(window5, text='City', bg=BLACK, fg=WHITE).grid(row=1, column=0)
    l3 = tkinter.Label(window5, text='Address', bg=BLACK, fg=WHITE).grid(row=2, column=0)
    l4 = tkinter.Label(window5, text='Phone No.', bg=BLACK, fg=WHITE).grid(row=4, column=0)
    l5 = tkinter.Label(window5, text='Email', bg=BLACK, fg=WHITE).grid(row=5, column=0)
    l6 = tkinter.Label(window5, text='Website', bg=BLACK, fg=WHITE).grid(row=6, column=0)

    def insert():
        done = True
        l1 = SerialNo.get(), City.get(), Address1.get(), Address2.get(), PhoneNo.get(), Email.get(), Website.get()
        for j in l1:
            if j == '':
                done = False
                messagebox.showerror(title='Error', message='Enter values in all fields!')
                break
            else:
                ex('select SerialNo from College_contact_details')
                l = cursor.fetchall()
                for j in l:  # fetching int from tuple from list returned by fetchall
                    for i in j:
                        if int(SerialNo.get()) == i:
                            messagebox.showerror(title='Error', message='Sorry that serial number is taken')
                            done = False
        if done == True:
            ex("Insert into College_contact_details values({},'{}','{}','{}','{}','{}','{}')".format(SerialNo.get(), City.get(),Address1.get(), Address2.get(), PhoneNo.get(),Email.get(), Website.get()))
            ex('commit;')
            messagebox.showinfo("Success!", "Record added!")

    # insert button
    s = tkinter.Button(window5, text="Add Record ", command=insert)
    s.config(bg=PURP, activebackground=PURP)
    s.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
    # show contact details
    c = tkinter.Button(window5, text="Show all records",
                       command=lambda: show('College_contact_details.csv','College_contact_details', ['Serial No', 'City', 'Address line1','Address line2', 'Phone No.', 'Email', 'Website']))
    c.config(bg=PURP, activebackground=PURP)
    c.grid(row=8, column=0)
    # delete button
    dlabel = tkinter.Label(window5, text="Enter Serial No of data to be deleted:")
    dlabel.config(bg=BLACK, fg=WHITE)
    dlabel.grid(row=9, column=0)
    dbox = tkinter.Entry(window5, width=30)
    dbox.grid(row=9, column=1)
    d = tkinter.Button(window5, text='Delete', command=lambda: delete(dbox, 'College_contact_details',
                                                                      dbox.get()))  # using lambda because we want to pass values.
    d.config(bg=PURP, activebackground=PURP)
    d.grid(row=10, column=0)

    window5.mainloop()

def table5():  # exam
    window5 = tkinter.Toplevel()
    window5.title('EXAM-DETAILS')
    window5.geometry("500x300")
    window5.config(bg=BLACK)
    # textboxes
    SerialNo = tkinter.Entry(window5, width=30)
    SerialNo.grid(row=0, column=1, padx=20, pady=(10, 0))
    reg = window5.register(validnum)  # validation
    SerialNo.config(validate='key', validatecommand=(reg, '%P'))
    ExamName = tkinter.Entry(window5, width=30)
    ExamName.grid(row=1, column=1, padx=20, pady=(10, 0))
    RegistrationDate = tkinter.Entry(window5, width=30)
    RegistrationDate.grid(row=2, column=1, padx=20, pady=(10, 0))
    ExamDate = tkinter.Entry(window5, width=30)
    ExamDate.grid(row=3, column=1, padx=20, pady=(10, 0))
    # labels
    l1 = tkinter.Label(window5, text='Serial No', bg=BLACK, activebackground=BLACK, fg=WHITE).grid(row=0, column=0, pady=(10, 0))
    l2 = tkinter.Label(window5, text='Exam Name', bg=BLACK,activebackground=BLACK, fg=WHITE).grid(row=1, column=0)
    l3 = tkinter.Label(window5, text='Registration Date', bg=BLACK, activebackground=BLACK, fg=WHITE).grid(row=2, column=0)
    l4 = tkinter.Label(window5, text='Exam Date', bg=BLACK, activebackground=BLACK, fg=WHITE).grid(row=3, column=0)

    def insert():
        done = True
        l1 = SerialNo.get(), ExamName.get(), RegistrationDate.get(), ExamDate.get()
        for j in l1:
            if j == '':
                done = False
                messagebox.showerror(title='Error', message='Enter values in all fields!')
                break
            else:
                ex('select SerialNo from Exam_info')
                l = cursor.fetchall()
                for j in l:  # fetching int from tuple from list returned by fetchall
                    for i in j:
                        if int(SerialNo.get()) == i:
                            messagebox.showerror(title='Error', message='Sorry that serial number is taken!')
                            done = False
        if done == True:
            ex("Insert into Exam_info values({},'{}','{}','{}')".format(SerialNo.get(), ExamName.get(),RegistrationDate.get(), ExamDate.get()))
            ex('commit;')
            messagebox.showinfo("Success!", "Record added!")

    # insert button
    s = tkinter.Button(window5, text="Add record", command=insert)
    s.config(bg=PURP, activebackground=PURP)
    s.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
    # show Exam info
    c = tkinter.Button(window5, text="Show all records ", command=lambda: show('Exam_info.csv', 'Exam_info',['Serial No', 'Exam Name','Registration Date','Exam Date']))
    c.config(bg=PURP, activebackground=PURP)
    c.grid(row=5, column=0)
    # delete button
    dlabel = tkinter.Label(window5, text="Enter Serial number of data to be deleted:")
    dlabel.config(bg=BLACK, fg = WHITE)
    dlabel.grid(row=6, column=0)
    dbox = tkinter.Entry(window5, width=30)
    dbox.grid(row=6, column=1)
    d = tkinter.Button(window5, text='Delete', command=lambda: delete(dbox, 'Exam_info',dbox.get()))  # using lambda because we want to pass values.
    d.config(bg=PURP, activebackground=PURP)
    d.grid(row=7, column=0)

    window5.mainloop()


def admin():
    root = tkinter.Toplevel()
    root.title("College cutoff")
    root.configure(width=500, height=300)
    root.configure(bg=BLACK)
    v = tkinter.IntVar()
    tkinter.Label(root, text="""WHAT DATA DO YOU WISH TO UPDATE?""", bg=BLACK, fg=PURP, justify=tkinter.CENTER, padx=20).pack()
    tkinter.Radiobutton(root, text="COLLEGE", bg=BLACK, activebackground=BLACK, fg=WHITE, variable=v, value=1, padx=20, command=table1).pack(anchor=tkinter.W)
    tkinter.Radiobutton(root, text="CUTOFFS-MALE", bg=BLACK, activebackground=BLACK, fg=WHITE, variable=v, value=2, padx=20, command=table2).pack(anchor=tkinter.W)
    tkinter.Radiobutton(root, text="CUTOFFS-FEMALE", bg=BLACK, activebackground=BLACK, fg=WHITE, variable=v, value=1, padx=20, command=table3).pack(
        anchor=tkinter.W)
    tkinter.Radiobutton(root, text="COLLEGE CONTACT DETAILS", bg=BLACK, activebackground=BLACK, fg=WHITE, variable=v, value=1, padx=20, command=table4).pack(
        anchor=tkinter.W)
    tkinter.Radiobutton(root, text="EXAM-DETAILS", bg=BLACK, activebackground=BLACK, fg=WHITE, variable=v, value=1, padx=20, command=table5).pack(anchor=tkinter.W)

    root.mainloop()


#checks if user is admin or guest
#__main__
root = tkinter.Tk()
root.title("Login")
root.config(bg=BLACK)
v = tkinter.IntVar()
tkinter.Label(root, text="""ARE YOU AN ADMIN OR A GUEST?""", justify=tkinter.LEFT, padx=20, bg=BLACK, fg=PURP).pack()
tkinter.Radiobutton(root, text="Guest", variable=v, value=1, padx=20, bg=BLACK, fg=WHITE, command=Guest, activebackground=BLACK, activeforeground=PURP).pack(anchor=tkinter.W)
tkinter.Radiobutton(root, text="Admin", variable=v, value=2, padx=20, bg=BLACK, fg=WHITE, command=admin, activebackground=BLACK, activeforeground=PURP).pack(anchor=tkinter.W)
root.mainloop()
