from tkinter import *
from BT2102_ALS_functions import * 
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


class Rep_11_Search(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        bg_path = "repbg.png"
        self.bg = PhotoImage(file=bg_path)
        label_bkgr = Label(self, image=self.bg)
        label_bkgr.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        self.controller = controller

        # instruction for book search 
        mem_11_instruction = Label(self, text = "Search based on one of the categories below:",  font=controller.title_font, bg="#b1b8c0")
        mem_11_instruction.place(relx = 0.5, rely = 0.1, anchor = CENTER)
        #mem_11_instruction.grid(row=1, column=1, sticky="W", pady=5)


        # labels for book search
        mem_11_title_lab = Label(self, text = "Title", font=controller.normal_font, bg="#b1b8c0")
        mem_11_title_lab.place(relx = 0.33, rely = 0.3, anchor = CENTER)
        #mem_11_title_lab.grid(row=5, column=0, sticky="E", padx=5, pady=10)

        mem_11_author_lab = Label(self, text = "Authors", font=controller.normal_font, bg="#b1b8c0")
        mem_11_author_lab.place(relx = 0.33, rely = 0.4, anchor = CENTER)
        #mem_11_author_lab.grid(row=7, column=0, sticky="E", padx=5, pady=10)

        mem_11_ISBN_lab = Label(self, text = "ISBN", font=controller.normal_font, bg="#b1b8c0")
        mem_11_ISBN_lab.place(relx = 0.33, rely = 0.5, anchor = CENTER)
        #mem_11_ISBN_lab.grid(row=9, column=0, sticky="E", padx=5, pady=10)

        mem_11_publisher_lab = Label(self, text = "Publisher", font=controller.normal_font, bg="#b1b8c0")
        mem_11_publisher_lab.place(relx = 0.33, rely = 0.6, anchor = CENTER)
        #mem_11_publisher_lab.grid(row=11, column=0, sticky="E", padx=5, pady=10)

        mem_11_pubYr_lab = Label(self, text = "Publication Year", font=controller.normal_font, bg="#b1b8c0")
        mem_11_pubYr_lab.place(relx = 0.33, rely = 0.7, anchor = CENTER)
        #mem_11_pubYr_lab.grid(row=13, column=0, sticky="E", padx=5, pady=10)



        # entry variables for book search
        mem_11_title_ent = Entry(self, width=30, font=controller.normal_font)
        mem_11_title_ent.place(relx = 0.66, rely = 0.3, anchor = CENTER)
        #mem_11_title_ent.grid(row=5, column=1, padx=5, pady=10)

        mem_11_author_ent = Entry(self, width=30, font=controller.normal_font)
        mem_11_author_ent.place(relx = 0.66, rely = 0.4, anchor = CENTER)
        #mem_11_author_ent.grid(row=7, column=1, padx=5, pady=10)

        mem_11_ISBN_ent = Entry(self, width=30, font=controller.normal_font)
        mem_11_ISBN_ent.place(relx = 0.66, rely = 0.5, anchor = CENTER)
        #mem_11_ISBN_ent.grid(row=9, column=1, padx=5, pady=10)

        mem_11_publisher_ent = Entry(self, width=30, font=controller.normal_font)
        mem_11_publisher_ent.place(relx = 0.66, rely = 0.6, anchor = CENTER)
        #mem_11_publisher_ent.grid(row=11, column=1, padx=5, pady=10)

        mem_11_pubYr_ent = Entry(self, width=30, font=controller.normal_font)
        mem_11_pubYr_ent.place(relx = 0.66, rely = 0.7, anchor = CENTER)
        #mem_11_pubYr_ent.grid(row=13, column=1, padx=5, pady=10)


        #Button functions

        def isOneWord(word):
            return len(word.split(" ")) <= 1

        def get_error():
            err = ""
            if mem_11_title_ent.get() == "" and mem_11_author_ent.get() == "" and mem_11_ISBN_ent.get() == "" and mem_11_publisher_ent.get() == "" \
                and mem_11_pubYr_ent.get() == "":
                err += "\nSearch not specified;"
            elif not(isOneWord(mem_11_title_ent.get()) and isOneWord(mem_11_author_ent.get()) and isOneWord(mem_11_ISBN_ent.get()) and \
                isOneWord(mem_11_publisher_ent.get()) and isOneWord(mem_11_pubYr_ent.get())):
                err += "\nOnly one word is accepted for each search field;"
            err = err[:-1]
            return err

        def search_func():
            error_string = get_error()
            
            if error_string == "":
                if mem_11_title_ent.get() == "":
                    search_title = "%"
                else:
                    search_title = "%" + mem_11_title_ent.get() + "%"
                if mem_11_author_ent.get() == "":
                    search_authors = "%"
                else:
                    search_authors = "%" + mem_11_author_ent.get() + "%"
                if mem_11_ISBN_ent.get() == "":
                    search_isbn = "%"
                else:
                    search_isbn = "%" + mem_11_ISBN_ent.get() + "%"
                if mem_11_publisher_ent.get() == "":
                    search_publisher = "%"
                else:
                    search_publisher = "%" + mem_11_publisher_ent.get() + "%"
                if mem_11_pubYr_ent.get() == "":
                    search_year = "%"
                else:
                    search_year = "%" + mem_11_pubYr_ent.get() + "%"
                sql = "SELECT accessionNo, title, author1, author2, author3, ISBN, publisher, publicationYear \
                    FROM Books WHERE title LIKE %s AND (author1 LIKE %s OR author2 LIKE %s OR author3 LIKE %s) \
                    AND ISBN LIKE %s AND publisher LIKE %s AND publicationYear LIKE %s"
                val = (search_title, search_authors, search_authors, search_authors, search_isbn, search_publisher, search_year)
                mycursor.execute(sql, val)
                rows = mycursor.fetchall()
                total = mycursor.rowcount
                #print("Total Data Entries: "+ str(total))

                ws = Tk()
                ws.title('Book Search Results')
                ws.geometry('800x300')
                ws['bg']='#fb0'

                tv = ttk.Treeview(ws)
                tv['columns']=('Accession Number', 'Title', 'Author1', 'Author2', 'Author3', 'ISBN', 'Publisher', 'Year')
                tv.column('#0', width=0, stretch=NO)
                tv.column('Accession Number', anchor=CENTER, width=110)
                tv.column('Title', anchor=CENTER, width=100)
                tv.column('Author1', anchor=CENTER, width=80)
                tv.column('Author2', anchor=CENTER, width=80)
                tv.column('Author3', anchor=CENTER, width=80)
                tv.column('ISBN', anchor=CENTER, width=70)
                tv.column('Publisher', anchor=CENTER, width=100)
                tv.column('Year', anchor=CENTER, width=70)

                tv.heading('#0', text='', anchor=CENTER)
                tv.heading('Accession Number', text='Accession Number', anchor=CENTER)
                tv.heading('Title', text='Title', anchor=CENTER)
                tv.heading('Author1', text='Author1', anchor=CENTER)
                tv.heading('Author2', text='Author2', anchor=CENTER)
                tv.heading('Author3', text='Author3', anchor=CENTER)
                tv.heading('ISBN', text='ISBN', anchor=CENTER)
                tv.heading('Publisher', text='Publisher', anchor=CENTER)
                tv.heading('Year', text='Year', anchor=CENTER)


                for i in rows:
                    tv.insert('', 'end', values=i)

                # tv.insert(parent='', index=0, iid=0, text='', values=('1','Vineet','Alpha'))
                # tv.insert(parent='', index=1, iid=1, text='', values=('2','Anil','Bravo'))
                # tv.insert(parent='', index=2, iid=2, text='', values=('3','Vinod','Charlie'))
                # tv.insert(parent='', index=3, iid=3, text='', values=('4','Vimal','Delta'))
                # tv.insert(parent='', index=4, iid=4, text='', values=('5','Manjeet','Echo'))
                tv.pack()

                back = Button(ws, text="Back to Search function", bg="black", fg="white", command=lambda: [controller.show_frame("Rep_11_Search"), ws.destroy()])
                back.pack()

                ws.mainloop()
            
            else:        
                global pop1
                pop1 = Toplevel(self)
                pop1.title("Error!")
                pop1.geometry("600x400")
                pop1.config(bg="#C53A5A")

                pop1_label1 = Label(pop1, text="Error!", font=controller.normal_font, bg="#b1b8c0")
                pop1_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                pop1_label2 = Label(pop1, text=error_string, font=controller.normal_font, bg="#b1b8c0")
                pop1_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

                error_frame = Frame(pop1, bg="#C53A5A")
                error_frame.place(anchor=CENTER)

                yes = Button(pop1, text="Back to Book Search Function", font=controller.normal_font, bg="#b1b8c0", command=lambda: [controller.show_frame("Rep_11_Search"), pop1.destroy()])
                yes.place(relx=0.5, rely=0.75, anchor=CENTER)
            
                ##insert error code pop up here
                ##return
                
        #Buttons
        mem_11_searchButton = Button(self, text="Search Book", padx=10, pady=10, 
        font=controller.normal_font, bg="#b1b8c0", command=search_func)
        mem_11_searchButton.place(relx = 0.25, rely = 0.9, anchor = CENTER)
        #mem_11_searchButton.grid(row=80, column=1, padx=10, pady=10)

        mem_11_menuButton = Button(self, text="Back to Reports Menu", padx=10, pady=10, 
        font=controller.normal_font, bg="#b1b8c0", command=lambda: controller.show_frame("ReportMenu"))
        mem_11_menuButton.place(relx = 0.5, rely = 0.9, anchor = CENTER)
        #mem_11_menuButton.grid(row=80, column=0, sticky="E", padx=10, pady=10)

        mainmenuButton = Button(self, text="Back to Main Menu", padx=10, pady=10, 
        font=controller.normal_font, bg="black", fg="white", command=lambda: controller.show_frame("MainMenu"))
        mainmenuButton.place(relx = 0.75, rely = 0.9, anchor = CENTER)
        #mainmenuButton.grid(row=80, column=0, sticky="E", padx=10, pady=10)