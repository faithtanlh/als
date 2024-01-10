from tkinter import *
from BT2102_ALS_functions import * 
import mysql.connector
from datetime import datetime
from SQLpassword import get_password

my_password = get_password()
mydb = mysql.connector.connect(
host = "localhost", 
user = "root", 
passwd = my_password, 
database = "libals")

mycursor = mydb.cursor()


class Fin_10_Payment(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        bg_path = "finbg.png"
        self.bg = PhotoImage(file=bg_path)
        label_bkgr = Label(self, image=self.bg)
        label_bkgr.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.controller = controller
        
        #instruction 
        mem_10_instruction = Label(self, text = "To Pay a Fine, Please Enter Information Below:", font=controller.title_font, bg="#b1b8c0")
        mem_10_instruction.place(relx = 0.5, rely = 0.15, anchor = CENTER)
        #mem_10_instruction.grid(row=1, column=1, sticky="W", pady=5)

        #labels
        mem_10_memID_lab = Label(self, text = "Membership ID", font=controller.normal_font, bg="#b1b8c0")
        mem_10_memID_lab.place(relx = 0.33, rely = 0.3, anchor = CENTER)
        #mem_10_memID_lab.grid(row=3, column=0, sticky="E", padx=5, pady=10)

        mem_10_paymentDate_lab = Label(self, text = "Payment Date", font=controller.normal_font, bg="#b1b8c0")
        mem_10_paymentDate_lab.place(relx = 0.33, rely = 0.5, anchor = CENTER)
        #mem_10_paymentDate_lab.grid(row=5, column=0, sticky="E", padx=5, pady=10)

        mem_10_paymentAmt_lab = Label(self, text = "Payment Amount", font=controller.normal_font, bg="#b1b8c0")
        mem_10_paymentAmt_lab.place(relx = 0.33, rely = 0.7, anchor = CENTER)
        #mem_10_paymentAmt_lab.grid(row=7, column=0, sticky="E", padx=5, pady=10)

        #entry box
        mem_10_memID_ent = Entry(self, width=30, font=controller.normal_font)
        mem_10_memID_ent.place(relx = 0.66, rely = 0.3, anchor = CENTER)
        #mem_10_memID_ent.grid(row=3, column=1, padx=5, pady=10)

        mem_10_paymentDate_ent = Entry(self, width=30, font=controller.normal_font)
        mem_10_paymentDate_ent.place(relx = 0.66, rely = 0.5, anchor = CENTER)
        #mem_10_paymentDate_ent.grid(row=5, column=1, padx=5, pady=10)
        
        mem_10_paymentAmt_ent = Entry(self, width=30, font=controller.normal_font)
        mem_10_paymentAmt_ent.place(relx = 0.66, rely = 0.7, anchor = CENTER)
        #mem_10_paymentAmt_ent.grid(row=7, column=1, padx=5, pady=10)

        def invalidMemID(mem_id):
            ref_alphabets = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            if mem_id == "":
                return False
            elif (len(mem_id) > 8) or(mem_id[0] not in ref_alphabets) or (mem_id[-1] not in ref_alphabets) or \
                (mem_id[1:-1].isdigit() == False):
                return True
            else:
                return False

        def checkMemberExists(mem_id):
            mycursor.execute("SELECT membershipID FROM LibMembers WHERE membershipID = %s", (mem_id,))
            result = mycursor.fetchall()
            if len(result) == 0: 
                return False
            return True

        def checkDateFormat(date_string):
            if len(date_string) != 10:
                return False
            if date_string[2] != "/" or date_string[5] != "/":
                return False
            return date_string[:2].isdigit() and date_string[3:5].isdigit() and date_string[6:].isdigit()

        #Button functions
        def confirm_popup():
            if invalidMemID(mem_10_memID_ent.get()):
                global pop4
                pop4 = Toplevel(self)
                pop4.title("Error!")
                pop4.geometry("600x400")
                pop4.config(bg="#C53A5A")

                pop4_label1 = Label(pop4, text="Error!", font=controller.normal_font)
                pop4_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                pop4_label2 = Label(pop4, text= "Invalid membership ID", font=controller.normal_font)      #backend determine which error msg
                pop4_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

                error_frame = Frame(pop4, bg="#C53A5A")
                error_frame.place(anchor=CENTER)

                back = Button(pop4, text="Back to Payment Function", font=controller.normal_font, command=lambda: [controller.show_frame("Fin_10_Payment"), pop4.destroy()])
                back.place(relx=0.5, rely=0.75, anchor=CENTER)
                return
            elif not checkMemberExists(mem_10_memID_ent.get()):
                global pop2
                pop2 = Toplevel(self)
                pop2.title("Error!")
                pop2.geometry("600x400")
                pop2.config(bg="#C53A5A")

                pop2_label1 = Label(pop2, text="Error!", font=controller.normal_font)
                pop2_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                pop2_label2 = Label(pop2, text= "Member does not exist", font=controller.normal_font)      #backend determine which error msg
                pop2_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

                error_frame = Frame(pop2, bg="#C53A5A")
                error_frame.place(anchor=CENTER)

                back = Button(pop2, text="Back to Payment Function", font=controller.normal_font, command=lambda: [controller.show_frame("Fin_10_Payment"), pop2.destroy()])
                back.place(relx=0.5, rely=0.75, anchor=CENTER)
                return
            if not checkDateFormat(mem_10_paymentDate_ent.get()):
                global pop5
                pop5 = Toplevel(self)
                pop5.title("Error!")
                pop5.geometry("600x400")
                pop5.config(bg="#C53A5A")

                pop5_label1 = Label(pop5, text="Error!", font=controller.normal_font)
                pop5_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                pop5_label2 = Label(pop5, text= "Invalid date format", font=controller.normal_font)      #backend determine which error msg
                pop5_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

                error_frame = Frame(pop5, bg="#C53A5A")
                error_frame.place(anchor=CENTER)

                back = Button(pop5, text="Back to Payment Function", font=controller.normal_font, command=lambda: [controller.show_frame("Fin_10_Payment"), pop5.destroy()])
                back.place(relx=0.5, rely=0.75, anchor=CENTER)
                return
            
            global pop1
            pop1 = Toplevel(self)
            pop1.title("Confirm Payment details")
            pop1.geometry("600x400")
            pop1.config(bg="#3ac5a5")

            pop1.columnconfigure(0,weight=0)
            pop1.columnconfigure(1,weight=2)

            def get_memID():
                return mem_10_memID_ent.get()

            def get_paymentDate():
                return mem_10_paymentDate_ent.get()

            def get_outstandingFine():
                mem_id = mem_10_memID_ent.get()
                mycursor.execute("SELECT paymentAmt FROM Fines WHERE membershipID = %s", (mem_id,))
                result = mycursor.fetchone()[0]
                return result

            pop1_label_main = Label(pop1, text="Please Confirm Details To Be Correct", font=controller.normal_font)
            pop1_label_main.place(relx=0.5, rely=0.15, anchor=CENTER)

            pop1_label_paymentDue1 = Label(pop1, text= "Payment Due : $", font=controller.normal_font)  ##quotation marks are to test
            pop1_label_paymentDue1.place(relx=0.33, rely=0.3, anchor=CENTER)
            pop1_label_paymentDue2 = Label(pop1, text= get_outstandingFine(), font=controller.normal_font)  
            pop1_label_paymentDue2.place(relx=0.33, rely=0.45, anchor=CENTER)
            pop1_label_paymentDue3 = Label(pop1, text= "Exact Fee only", font=controller.normal_font )  
            pop1_label_paymentDue3.place(relx=0.33, rely=0.6, anchor=CENTER)
            pop1_label_memID = Label(pop1, text= get_memID(), font=controller.normal_font)
            pop1_label_memID.place(relx=0.66, rely=0.3, anchor=CENTER)
            pop1_label_paymentDate = Label(pop1, text= get_paymentDate(), font=controller.normal_font)
            pop1_label_paymentDate.place(relx=0.66, rely=0.45, anchor=CENTER)

            payment_frame = Frame(pop1, bg="#3ac5a5")
            payment_frame.place(anchor=CENTER)

            confirm = Button(pop1, text="Confirm Payment", font=controller.normal_font, command= lambda: [pay_or_error(), pop1.destroy()]) 
            confirm.place(relx=0.33, rely=0.8, anchor=CENTER)

            back = Button(pop1, text="Back to Payment function", font=controller.normal_font, command=lambda: [controller.show_frame("Fin_10_Payment"), pop1.destroy()])
            back.place(relx=0.66, rely=0.8, anchor=CENTER)

        def checkIsNumber(payment_amt):
            try:
                float(payment_amt)
            except ValueError:
                return False
            else:
                return True

        def get_error():
            err = ""
            if not checkIsNumber(mem_10_paymentAmt_ent.get()):
                err += "\nInvalid amount to pay;"
                return err[:-1]
            if not checkMemberExists(mem_10_memID_ent.get()):
                err += "\nMember does not exist;"
            else:
                mycursor.execute("SELECT paymentAmt FROM Fines WHERE membershipID = %s", (mem_10_memID_ent.get(),))
                result = mycursor.fetchone()[0]
                cumulative_amt = float(result)
                if cumulative_amt == 0:
                    err += "\nMember has no fines to pay;"
                elif cumulative_amt != float(mem_10_paymentAmt_ent.get()):
                    err += "\nIncorrect payment amount: exact payment is required;"
            err = err[:-1]
            return err

        def convert_to_date(date_string):
            dto = datetime.strptime(date_string, '%m/%d/%Y').date()
            return dto

        def pay_fine():
            payment_date = convert_to_date(mem_10_paymentDate_ent.get())
            sql = "UPDATE Fines SET paymentDate = %s, paymentAmt = 0 WHERE membershipID = %s"
            val = (payment_date, mem_10_memID_ent.get())
            mycursor.execute(sql, val)
            mydb.commit()
            msg = "Fines have been completely paid"

            global pop3
            pop3 = Toplevel(self)
            pop3.title("Success!")
            pop3.geometry("600x400")
            pop3.config(bg="#3ac5a5")

            pop3_label1 = Label(pop3, text="Success!", font=controller.normal_font, bg="#b1b8c0")
            pop3_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
            pop3_label2 = Label(pop3, text=msg, font=controller.normal_font, bg="#b1b8c0")
            pop3_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

            success_frame = Frame(pop3, bg="#3ac5a5")
            success_frame.place(anchor=CENTER)

            back = Button(pop3, text="Back to Payment Function", font=controller.normal_font, bg="#b1b8c0", command=lambda: [controller.show_frame("Fin_10_Payment"), pop3.destroy()])
            back.place(relx=0.5, rely=0.75, anchor=CENTER)
            ##code for pop up

        def pay_or_error():
            error_string = get_error()

            if error_string == "":
                return pay_fine()            #backend pay func
            else:
                global pop2
                pop2 = Toplevel(self)
                pop2.title("Error!")
                pop2.geometry("600x400")
                pop2.config(bg="#C53A5A")

                pop2_label1 = Label(pop2, text="Error!", font=controller.normal_font)
                pop2_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                pop2_label2 = Label(pop2, text= error_string, font=controller.normal_font) ##backend function to decide which error code  
                pop2_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

                error_frame = Frame(pop2, bg="#C53A5A")
                error_frame.place(anchor=CENTER)

                back = Button(pop2, text="Back to Payment Function", font=controller.normal_font, command=lambda: [controller.show_frame("Fin_10_Payment"), pop2.destroy()])
                back.place(relx=0.5, rely=0.75, anchor=CENTER)


        #buttons
        mem_10_payButton = Button(self, text="Pay Fine", padx=10, pady=10, 
        font=controller.normal_font, bg="#b1b8c0", command=confirm_popup)
        mem_10_payButton.place(relx = 0.25, rely = 0.85, anchor = CENTER)
        #mem_10_payButton.grid(row=80, column=2, padx=10, pady=10)

        mem_10_menuButton = Button(self, text="Back to Fines Menu", padx=10, pady=10, 
        font=controller.normal_font, bg="#b1b8c0", command=lambda: controller.show_frame("FineMenu"))
        mem_10_payButton.place(relx = 0.5, rely = 0.85, anchor = CENTER)
        #mem_10_menuButton.grid(row=80, column=1, sticky="E", padx=10, pady=10)

        mainmenuButton = Button(self, text="Back to Main Menu", padx=10, pady=10, 
        bg="black", fg="white", command=lambda: controller.show_frame("MainMenu"))
        mainmenuButton.place(relx = 0.75, rely = 0.85, anchor = CENTER)
        #mainmenuButton.grid(row=80, column=0, sticky="E", padx=10, pady=10)

