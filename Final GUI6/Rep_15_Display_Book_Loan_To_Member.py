from tkinter import *
from BT2102_ALS_functions import * 
from tkinter import ttk
import mysql.connector
from SQLpassword import get_password

my_password = get_password()
mydb = mysql.connector.connect(
host = "localhost", 
user = "root", 
passwd = my_password, 
database = "libals")

mycursor = mydb.cursor()

class Rep_15_Display_Book_Loan_To_Member(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        bg_path = "repbg.png"
        self.bg = PhotoImage(file=bg_path)
        label_bkgr = Label(self, image=self.bg)
        label_bkgr.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        self.controller = controller

        # instruction for book search 
        mem_15_instruction = Label(self, text = "Books on Loan to Member", font=controller.title_font, bg="#b1b8c0")
        mem_15_instruction.place(relx = 0.5, rely = 0.25, anchor = CENTER)
        #mem_15_instruction.grid(row=1, column=1, sticky="W", pady=5)


        # labels for book search
        mem_15_memID_lab = Label(self, text = "Membership ID", font=controller.normal_font, bg="#b1b8c0")
        mem_15_memID_lab.place(relx = 0.33, rely = 0.5, anchor = CENTER)
        #mem_15_memID_lab.grid(row=5, column=0, sticky="E", padx=5, pady=10)


        # entry variables for book search
        mem_15_memID_ent = Entry(self, width=30, font=controller.normal_font)
        mem_15_memID_ent.place(relx = 0.66, rely = 0.5, anchor = CENTER)
        #mem_15_memID_ent.grid(row=5, column=1, padx=5, pady=10)

        def getBooksLoanedByMemID(mem_id):
            mycursor.execute("SELECT t1.* FROM Books AS t1 INNER JOIN Loans AS t2 ON t1.accessionNo = \
                t2.accessionNo WHERE t2.membershipID = %s AND t2.loanReturn IS NULL;", (mem_id,))
            result = mycursor.fetchall()
            return result

        def checkMemberExists(mem_id):
            mycursor.execute("SELECT membershipID FROM LibMembers WHERE membershipID = %s", (mem_id,))
            result = mycursor.fetchall()
            if len(result) == 0: 
                return False
            return True
            
        def search_func():
            if not checkMemberExists(mem_15_memID_ent.get()):
                global pop1
                pop1 = Toplevel(self)
                pop1.title("Error!")
                pop1.geometry("600x400")
                pop1.config(bg="#C53A5A")

                pop1_label1 = Label(pop1, text="Error!", font=controller.normal_font)
                pop1_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                pop1_label2 = Label(pop1, text= "Member does not exist", font=controller.normal_font)      #backend determine which error msg
                pop1_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

                error_frame = Frame(pop1, bg="#C53A5A")
                error_frame.place(anchor=CENTER)

                back = Button(pop1, text="Back to Display Function", font=controller.normal_font, command=lambda: [controller.show_frame("Rep_15_Display_Book_Loan_To_Member"), pop1.destroy()])
                back.place(relx=0.5, rely=0.75, anchor=CENTER)
                return

            booksLoanedByMemRows = getBooksLoanedByMemID(mem_15_memID_ent.get()) #backend function

            # win = Tk()

            # frm =Frame(win)
            # frm.pack(side=tk.LEFT, padx=20)

            # tv = ttk.Treeview(frm, columns=(1,2,3,4,5,6), show="headings", height="S")
            # tv.pack()

            # tv.heading(1, text="Accession Number")
            # tv.heading(2, text="Title")
            # tv.heading(3, text="Authors")
            # tv.heading(4, text="ISBN")
            # tv.heading(5, text="Publisher")
            # tv.heading(6, text="Year")

            # back = Button(win, text="Back to Reports menu", bg="black", fg="white", command=reportsmenu)
            # back.grid(row=15, column=0, padx=50)

            # for i in booksLoanedByMemRows:
            #     tv.insert('', 'end', values=i)

            # win.title("Customer Data")
            # win.geometry("650x500")
            # win.resizable(False, False)
            # win.mainloop()

            ws = Tk()
            ws.title('Books on Loan to Member')
            ws.geometry('600x300')
            ws['bg']='#fb0'

            tv = ttk.Treeview(ws)
            tv['columns']=('Accession Number', 'Title', 'Authors', 'ISBN', 'Publisher', 'Year')
            tv.column('#0', width=0, stretch=NO)
            tv.column('Accession Number', anchor=CENTER, width=110)
            tv.column('Title', anchor=CENTER, width=100)
            tv.column('Authors', anchor=CENTER, width=100)
            tv.column('ISBN', anchor=CENTER, width=70)
            tv.column('Publisher', anchor=CENTER, width=100)
            tv.column('Year', anchor=CENTER, width=70)

            tv.heading('#0', text='', anchor=CENTER)
            tv.heading('Accession Number', text='Accession Number', anchor=CENTER)
            tv.heading('Title', text='Title', anchor=CENTER)
            tv.heading('Authors', text='Authors', anchor=CENTER)
            tv.heading('ISBN', text='ISBN', anchor=CENTER)
            tv.heading('Publisher', text='Publisher', anchor=CENTER)
            tv.heading('Year', text='Year', anchor=CENTER)


            for i in booksLoanedByMemRows:
                tv.insert('', 'end', values=i)

            # tv.insert(parent='', index=0, iid=0, text='', values=('1','Vineet','Alpha'))
            # tv.insert(parent='', index=1, iid=1, text='', values=('2','Anil','Bravo'))
            # tv.insert(parent='', index=2, iid=2, text='', values=('3','Vinod','Charlie'))
            # tv.insert(parent='', index=3, iid=3, text='', values=('4','Vimal','Delta'))
            # tv.insert(parent='', index=4, iid=4, text='', values=('5','Manjeet','Echo'))
            tv.pack()

            back = Button(ws, text="Back to Reports Menu", bg="black", fg="white", command=lambda: [controller.show_frame("ReportMenu"), ws.destroy()])
            back.pack()

            ws.mainloop()


        #Buttons
        mem_15_searchButton = Button(self, text="Search Member", padx=10, pady=10, 
        font=controller.normal_font, bg="#b1b8c0", command=search_func)
        mem_15_searchButton.place(relx = 0.25, rely = 0.75, anchor = CENTER)
        #mem_15_searchButton.grid(row=80, column=1, padx=10, pady=10)

        mem_15_menuButton = Button(self, text="Back to Reports Menu", padx=10, pady=10, 
        font=controller.normal_font, bg="#b1b8c0", command=lambda: controller.show_frame("ReportMenu"))
        mem_15_menuButton.place(relx = 0.5, rely = 0.75, anchor = CENTER)
        #mem_15_menuButton.grid(row=80, column=0, sticky="E", padx=10, pady=10)

        mainmenuButton = Button(self, text="Back to Main Menu", padx=10, pady=10, 
        font=controller.normal_font, bg="black", fg="white", command=lambda: controller.show_frame("MainMenu"))
        mainmenuButton.place(relx = 0.75, rely = 0.75, anchor = CENTER)
        #mainmenuButton.grid(row=80, column=0, sticky="E", padx=10, pady=10)