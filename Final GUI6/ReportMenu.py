from tkinter import * 
import mysql.connector
from tkinter import ttk
from SQLpassword import get_password

my_password = get_password()
mydb = mysql.connector.connect(
host = "localhost", 
user = "root", 
passwd = my_password, 
database = "libals")

mycursor = mydb.cursor()

class ReportMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        bg_path = "repbg.png"
        self.bg = PhotoImage(file=bg_path)
        label_bkgr = Label(self, image=self.bg)
        label_bkgr.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.controller = controller

        ## start for 12-Display Loan 
        def getBooksOnLoan():
            mycursor.execute("SELECT t1.* FROM Books AS t1 INNER JOIN Loans AS \
                t2 ON t1.accessionNo = t2.accessionNo WHERE t2.loanReturn IS NULL")
            result = mycursor.fetchall()
            return result

        def display_loan_func(): 
            loanRows = getBooksOnLoan() #backend function

            ws = Tk()
            ws.title('Books on Loan Results')
            ws.geometry('700x300')
            ws['bg']='#fb0'

            tv = ttk.Treeview(ws)
            tv['columns']=('Accession Number', 'Title', 'Author 1', 'Author 2', 'Author 3', 'ISBN', 'Publisher', 'Year')
            tv.column('#0', width=0, stretch=NO)
            tv.column('Accession Number', anchor=CENTER, width=110)
            tv.column('Title', anchor=CENTER, width=100)
            tv.column('Author 1', anchor=CENTER, width=70)
            tv.column('Author 2', anchor=CENTER, width=70)
            tv.column('Author 3', anchor=CENTER, width=70)
            tv.column('ISBN', anchor=CENTER, width=70)
            tv.column('Publisher', anchor=CENTER, width=100)
            tv.column('Year', anchor=CENTER, width=70)

            tv.heading('#0', text='', anchor=CENTER)
            tv.heading('Accession Number', text='Accession Number', anchor=CENTER)
            tv.heading('Title', text='Title', anchor=CENTER)
            tv.heading('Author 1', text='Author 1', anchor=CENTER)
            tv.heading('Author 2', text='Author 2', anchor=CENTER)
            tv.heading('Author 3', text='Author 3', anchor=CENTER)
            tv.heading('ISBN', text='ISBN', anchor=CENTER)
            tv.heading('Publisher', text='Publisher', anchor=CENTER)
            tv.heading('Year', text='Year', anchor=CENTER)

            

            for i in loanRows:
                tv.insert('', 'end', values=i)

            # tv.insert(parent='', index=0, iid=0, text='', values=('1','Vineet','Alpha'))
            # tv.insert(parent='', index=1, iid=1, text='', values=('2','Anil','Bravo'))
            # tv.insert(parent='', index=2, iid=2, text='', values=('3','Vinod','Charlie'))
            # tv.insert(parent='', index=3, iid=3, text='', values=('4','Vimal','Delta'))
            # tv.insert(parent='', index=4, iid=4, text='', values=('5','Manjeet','Echo'))
            tv.pack()
            
            back = Button(ws, text="Back to Reports Menu", bg="black", fg="white", command=lambda: [controller.show_frame("ReportMenu"), ws.destroy()])
            back.pack()

        ## start for 13 - Display Reservation 
        def getReservedBooks():
            mycursor.execute("SELECT T3.accessionNo, T1.title, T3.membershipID, concat(fName, ' ', lName) name \
                    FROM (Books as T1 INNER JOIN Reservations as T3 ON T1.accessionNo = T3.accessionNo) \
                    INNER JOIN LibMembers as T2 ON T2.membershipID = T3.membershipID ORDER BY accessionNo;")
            result = mycursor.fetchall()
            return result

            
        def display_res_func():
            reservationRows = getReservedBooks() #backend function

            ws = Tk()
            ws.title('Books on Reservation Report')
            ws.geometry('700x300')
            ws['bg']='#fb0'

            tv = ttk.Treeview(ws)
            tv['columns']=('Accession Number', 'Title', 'Membership ID', 'Name')
            tv.column('#0', width=0, stretch=NO)
            tv.column('Accession Number', anchor=CENTER, width=110)
            tv.column('Title', anchor=CENTER, width=110)
            tv.column('Membership ID', anchor=CENTER, width=110)
            tv.column('Name', anchor=CENTER, width=110)


            tv.heading('#0', text='', anchor=CENTER)
            tv.heading('Accession Number', text='Accession Number', anchor=CENTER)
            tv.heading('Title', text='Title', anchor=CENTER)
            tv.heading('Membership ID', text='Membership ID', anchor=CENTER)
            tv.heading('Name', text='Name', anchor=CENTER)



            for i in reservationRows:
                tv.insert('', 'end', values=i)

            # tv.insert(parent='', index=0, iid=0, text='', values=('1','Vineet','Alpha'))
            # tv.insert(parent='', index=1, iid=1, text='', values=('2','Anil','Bravo'))
            # tv.insert(parent='', index=2, iid=2, text='', values=('3','Vinod','Charlie'))
            # tv.insert(parent='', index=3, iid=3, text='', values=('4','Vimal','Delta'))
            # tv.insert(parent='', index=4, iid=4, text='', values=('5','Manjeet','Echo'))
            tv.pack()

            back = Button(ws, text="Back to Reports Menu", bg="black", fg="white", command=lambda: [controller.show_frame("ReportMenu"), ws.destroy()])
            back.pack()

        # start for 14 - Display Fines
        def getMembersWithFine():
            mycursor.execute("SELECT t1.membershipID, concat(fName, ' ', lName) name, faculty, phoneNo, eMail \
                FROM LibMembers AS t1 INNER JOIN Fines AS t2 ON t1.membershipID = t2.membershipID \
                WHERE t2.paymentAmt > 0;")
            result = mycursor.fetchall()
            return result

        def display_fine_func(): 
            memWithFinesRows = getMembersWithFine() #backend function

            ws = Tk()
            ws.title('Members with Outstanding Fines')
            ws.geometry('700x300')
            ws['bg']='#fb0'

            tv = ttk.Treeview(ws)
            tv['columns']=('Membership ID', 'Name', 'Faculty', 'Phone Number', 'Email Address')
            tv.column('#0', width=0, stretch=NO)
            tv.column('Membership ID', anchor=CENTER, width=110)
            tv.column('Name', anchor=CENTER, width=110)
            tv.column('Faculty', anchor=CENTER, width=90)
            tv.column('Phone Number', anchor=CENTER, width=110)
            tv.column('Email Address', anchor=CENTER, width=130)


            tv.heading('#0', text='', anchor=CENTER)
            tv.heading('Membership ID', text='Membership ID', anchor=CENTER)
            tv.heading('Name', text='Name', anchor=CENTER)
            tv.heading('Faculty', text='Faculty', anchor=CENTER)
            tv.heading('Phone Number', text='Phone Number', anchor=CENTER)
            tv.heading('Email Address', text='Email Address', anchor=CENTER)


            for i in memWithFinesRows:
                tv.insert('', 'end', values=i)

            # tv.insert(parent='', index=0, iid=0, text='', values=('1','Vineet','Alpha'))
            # tv.insert(parent='', index=1, iid=1, text='', values=('2','Anil','Bravo'))
            # tv.insert(parent='', index=2, iid=2, text='', values=('3','Vinod','Charlie'))
            # tv.insert(parent='', index=3, iid=3, text='', values=('4','Vimal','Delta'))
            # tv.insert(parent='', index=4, iid=4, text='', values=('5','Manjeet','Echo'))
            tv.pack()

            back = Button(ws, text="Back to Reports Menu", bg="black", fg="white",  command=lambda: [controller.show_frame("ReportMenu"), ws.destroy()])
            back.pack()



        # Report Menu Buttons 

        label = Label(self, text="Report Menu", font=controller.title_font, bg="#b1b8c0", relief="solid")
        label.place(relx=0.5, rely=0.15, anchor="center")

        container = Frame(self)
        container.place(anchor="center")

        b1 = Button(self, text="Book Search", font=controller.normal_font, bg="#b1b8c0",
        command=lambda: controller.show_frame("Rep_11_Search"))
        b1.place(relx=0.25, rely=0.4, anchor="center")
        b1.config(height = 5, width = 20 )

        b2 = Button(self, text="Display Books On \n Loan", font=controller.normal_font, bg="#b1b8c0",
        command=display_loan_func)
        b2.place(relx=0.50, rely=0.4, anchor="center")
        b2.config(height = 5, width = 20 )

        b3 = Button(self, text="Display Books On \n Reservation", font=controller.normal_font, bg="#b1b8c0",
        command=display_res_func)
        b3.place(relx=0.75, rely=0.4, anchor="center")
        b3.config(height = 5, width = 20 )

        b4 = Button(self, text="Display Outstanding Fees", font=controller.normal_font, bg="#b1b8c0",
        command=display_fine_func)
        b4.place(relx=0.25, rely=0.7, anchor="center")
        b4.config(height = 5, width = 20 )

        b5 = Button(self, text="Display Books On \n Loan to Member", font=controller.normal_font, bg="#b1b8c0",
        command=lambda: controller.show_frame("Rep_15_Display_Book_Loan_To_Member"))
        b5.place(relx=0.50, rely=0.7, anchor="center")
        b5.config(height = 5, width = 20 )

        b6 = Button(self, text="Back to Main Menu", font=controller.normal_font, bg="black", fg="white",
        command=lambda: controller.show_frame("MainMenu"))
        b6.place(relx=0.75, rely=0.7, anchor="center")
        b6.config(height = 5, width = 20 )



        
