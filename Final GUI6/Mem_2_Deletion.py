from tkinter import * 
from BT2102_ALS_functions import *
import mysql.connector
from SQLpassword import get_password

my_password = get_password()
mydb = mysql.connector.connect(
host = "localhost", 
user = "root", 
passwd = my_password, 
database = "libals")

mycursor = mydb.cursor()

class Mem_2_Deletion(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        bg_path = "membg.png"
        self.bg = PhotoImage(file=bg_path)
        label_bkgr = Label(self, image=self.bg)
        label_bkgr.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.controller = controller

        #instruction 
        mem_2_instruction = Label(self, text = "To delete member, please enter Membership ID", font=controller.title_font, bg="#b1b8c0")
        mem_2_instruction.place(relx = 0.5, rely = 0.25, anchor = CENTER)
        #mem_2_instruction.grid(row=1, column=1, sticky="W", pady=5)
        
        #labels
        mem_2_id_lab = Label(self, text = "Membership ID", font=controller.normal_font, bg="#b1b8c0")
        mem_2_id_lab.place(relx = 0.33, rely = 0.5, anchor = CENTER)
        #mem_2_id_lab.grid(row=5, column=0, sticky="E", padx=5, pady=10)

        #entry box
        mem_2_id_ent = Entry(self, width=30, font=controller.normal_font)
        mem_2_id_ent.place(relx = 0.66, rely = 0.5, anchor = CENTER)
        #mem_2_id_ent.grid(row=5, column=1, padx=5, pady=10)

        #check_loan_reservation_OF function
        def check_loan_reservation_OF(mem_id):
            error_string = ""   
            if not checkMemberExists(mem_id): #checkMemberExists is a backend function
                return "No such member exists"
            else:
                mycursor.execute("SELECT membershipID FROM Loans WHERE membershipID = %s AND loanReturn IS NULL", (mem_id,))
                result = mycursor.fetchall()
                if len(result) != 0:
                    error_string += "\nMember has yet to return loaned books;"

                mycursor.execute("SELECT membershipID FROM Reservations WHERE membershipID = %s", (mem_id,))
                result = mycursor.fetchall()
                if len(result) != 0:
                    error_string += "\nMember still has some books reserved;"
                
                mycursor.execute("SELECT membershipID FROM Fines WHERE membershipID = %s AND paymentAmt != 0", (mem_id,))
                result = mycursor.fetchall()
                if len(result) != 0:
                    error_string += "\nMember has outstanding fines;"
            return error_string

        #Button functions
        def delete_popup(): 
            err_string = check_loan_reservation_OF(mem_2_id_ent.get())
            if err_string != "":
                global pop1
                pop1 = Toplevel(self)
                pop1.title("Error")
                pop1.geometry("600x400")
                pop1.config(bg="#C53A5A")

                pop1_label1 = Label(pop1, text="Error!", font=controller.normal_font)
                pop1_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                pop1_label2 = Label(pop1, text="Member has loans, reservations, or outstanding fines", font=controller.normal_font)
                pop1_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

                error_frame = Frame(pop1, bg="#C53A5A")
                error_frame.place(anchor=CENTER)

                back = Button(pop1, text="Back to Delete Function", font=controller.normal_font, command=lambda: [controller.show_frame("Mem_2_Deletion"), pop1.destroy()])
                back.place(relx=0.5, rely=0.75, anchor=CENTER)

            else:
                global pop2
                pop2 = Toplevel(self)
                pop2.title("Confirm Details")
                pop2.geometry("600x400")
                pop2.config(bg="#3ac5a5")

                def get_memID():
                    return mem_2_id_ent.get()

                def get_name():
                    mem_id = mem_2_id_ent.get()
                    mycursor.execute("SELECT lName FROM LibMembers WHERE membershipID = %s", (mem_id,))
                    result = mycursor.fetchone()[0]
                    if result != None:
                        mycursor.execute("SELECT concat(fName, ' ', lName) FROM LibMembers WHERE membershipID = %s", (mem_id,))
                        final_result = mycursor.fetchone()[0]
                    else:
                        mycursor.execute("SELECT fName FROM LibMembers WHERE membershipID = %s", (mem_id,))
                        final_result = mycursor.fetchone()[0]
                    return final_result

                def get_fac():
                    mem_id = mem_2_id_ent.get()
                    mycursor.execute("SELECT faculty FROM LibMembers WHERE membershipID = %s", (mem_id,))
                    result = mycursor.fetchone()[0]
                    return result

                def get_phonenum():
                    mem_id = mem_2_id_ent.get()
                    mycursor.execute("SELECT phoneNo FROM LibMembers WHERE membershipID = %s", (mem_id,))
                    result = mycursor.fetchone()[0]
                    return result

                def get_email():
                    mem_id = mem_2_id_ent.get()
                    mycursor.execute("SELECT eMail FROM LibMembers WHERE membershipID = %s", (mem_id,))
                    result = mycursor.fetchone()[0]
                    return result

                pop2_label_main = Label(pop2, text="Please Confirm Details to be Correct", font=controller.normal_font)
                pop2_label_main.place(relx=0.5, rely=0.15, anchor=CENTER)
                pop2_label_memID = Label(pop2, text= get_memID(), font=controller.normal_font)
                pop2_label_memID.place(relx=0.5, rely=0.3, anchor=CENTER)
                pop2_label_name = Label(pop2, text= get_name(), font=controller.normal_font)
                pop2_label_name.place(relx=0.5, rely=0.4, anchor=CENTER)
                pop2_label_fac = Label(pop2, text= get_fac(), font=controller.normal_font)
                pop2_label_fac.place(relx=0.5, rely=0.5, anchor=CENTER)
                pop2_label_phonenum = Label(pop2, text= get_phonenum(), font=controller.normal_font)
                pop2_label_phonenum.place(relx=0.5, rely=0.6, anchor=CENTER)
                pop2_label_email = Label(pop2, text= get_email(), font=controller.normal_font)
                pop2_label_email.place(relx=0.5, rely=0.7, anchor=CENTER)

                deletion_frame = Frame(pop2, bg="#3ac5a5")
                deletion_frame.place(anchor=CENTER)

                def delete_member():
                    global pop3
                    pop3 = Toplevel(self)
                    pop3.title("Success!")
                    pop3.geometry("600x400")
                    pop3.config(bg="#3ac5a5")

                    success_frame = Frame(pop3, bg="#3ac5a5")
                    success_frame.place(anchor=CENTER)

                    pop3_label1 = Label(pop3, text="Success!", font=controller.normal_font)
                    pop3_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                    pop3_label2 = Label(pop3, text="ALS membership deleted.", font=controller.normal_font)
                    pop3_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

                    yes = Button(pop3, text="Back to Delete Function", font=controller.normal_font, command=lambda: [controller.show_frame("Mem_2_Deletion"), pop3.destroy()])
                    yes.place(relx=0.5, rely=0.75, anchor=CENTER)

                    mycursor.execute("DELETE FROM LibMembers WHERE membershipID = %s", (mem_2_id_ent.get(),))
                    mydb.commit()
                    
                confirm_deletion = Button(pop2, text="Confirm Deletion", font=controller.normal_font, command=lambda: [delete_member(), pop2.destroy()])
                confirm_deletion.place(relx=0.33, rely=0.85, anchor=CENTER)
                back = Button(pop2, text="Back to delete function", font=controller.normal_font, command=lambda: [controller.show_frame("Mem_2_Deletion"), pop2.destroy()])
                back.place(relx=0.66, rely=0.85, anchor=CENTER)


        #Buttons
        mem_2_deleteButton = Button(self, text="Delete Member", padx=10, pady=10, font=controller.normal_font, 
        bg="#b1b8c0", command=delete_popup)
        mem_2_deleteButton.place(relx = 0.25, rely = 0.75, anchor = CENTER)
        #mem_2_deleteButton.grid(row=80, column=1, padx=10, pady=10)

        mem_2_backButton = Button(self, text="Back to Membership Menu", padx=10, pady=10, font=controller.normal_font, 
        bg="#b1b8c0", command=lambda: controller.show_frame("MembershipMenu"))
        mem_2_backButton.place(relx = 0.5, rely = 0.75, anchor = CENTER)
        #mem_2_backButton.grid(row=80, column=1, sticky="E", padx=10, pady=10)

        mainmenuButton = Button(self, text="Back to Main Menu", padx=10, pady=10, font=controller.normal_font, 
        bg="black", fg="white", command=lambda: controller.show_frame("MainMenu"))
        mainmenuButton.place(relx = 0.75, rely = 0.75, anchor = CENTER)
        #mainmenuButton.grid(row=80, column=0, sticky="E", padx=10, pady=10)

