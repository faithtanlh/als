from tkinter import *
from BT2102_ALS_functions import *
import mysql.connector
from Mem_3_Update_Page1 import * 
from SQLpassword import get_password


my_password = get_password()
mydb = mysql.connector.connect(
host = "localhost", 
user = "root", 
passwd = my_password, 
database = "libals")

mycursor = mydb.cursor()


class Mem_3_Update_Page2(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        bg_path = "membg.png"
        self.bg = PhotoImage(file=bg_path)
        label_bkgr = Label(self, image=self.bg)
        label_bkgr.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.controller = controller

        # instruction 
        mem_3_instruction = Label(self, text = "Please enter the requested information below:", font=controller.title_font, bg="#b1b8c0")
        mem_3_instruction.place(relx=0.5, rely=0.1, anchor=CENTER)
        #mem_3_instruction.grid(row=1, column=1, sticky="W", pady=5)


        # labels
        #mem_3_id_lab = Label(self, text = "Membership ID", font=controller.normal_font, bg="#b1b8c0")
        #mem_3_id_lab.place(relx=0.33, rely=0.2, anchor=CENTER)
        #mem_3_id_lab.grid(row=5, column=0, sticky="E", padx=5, pady=10)

        mem_3_firstname_lab = Label(self, text = "First Name", font=controller.normal_font, bg="#b1b8c0")
        mem_3_firstname_lab.place(relx=0.33, rely=0.3, anchor=CENTER)
        #mem_3_name_lab.grid(row=7, column=0, sticky="E", padx=5, pady=10)

        mem_3_lastname_lab = Label(self, text = "Last Name", font=controller.normal_font, bg="#b1b8c0")
        mem_3_lastname_lab.place(relx=0.33, rely=0.4, anchor=CENTER)

        mem_3_faculty_lab = Label(self, text = "Faculty", font=controller.normal_font, bg="#b1b8c0")
        mem_3_faculty_lab.place(relx=0.33, rely=0.5, anchor=CENTER)
        #mem_3_faculty_lab.grid(row=9, column=0, sticky="E", padx=5, pady=10)

        mem_3_phone_num_lab = Label(self, text = "Phone Number", font=controller.normal_font, bg="#b1b8c0")
        mem_3_phone_num_lab.place(relx=0.33, rely=0.6, anchor=CENTER)
        #mem_3_phone_num_lab.grid(row=11, column=0, sticky="E", padx=5, pady=10)

        mem_3_email_add_lab = Label(self, text = "Email Address", font=controller.normal_font, bg="#b1b8c0")
        mem_3_email_add_lab.place(relx=0.33, rely=0.7, anchor=CENTER)
        #mem_3_email_add_lab.grid(row=13, column=0, sticky="E", padx=5, pady=10)


        # entry box
        #mem_3_id_ent = Entry(self, width=30, font=controller.normal_font)
        #mem_3_id_ent.place(relx=0.66, rely=0.2, anchor=CENTER)
        #mem_3_id_ent.grid(row=5, column=1, padx=5, pady=10)

        page_one = self.controller.get_page("Mem_3_Update_Page1")
        mem_3_id_ent = page_one.mem_id

        mem_3_firstname_ent = Entry(self, width=30, font=controller.normal_font)
        mem_3_firstname_ent.place(relx=0.66, rely=0.3, anchor=CENTER)
        #mem_3_firstname_ent.grid(row=7, column=1, padx=5, pady=10)

        mem_3_lastname_ent = Entry(self, width=30, font=controller.normal_font)
        mem_3_lastname_ent.place(relx=0.66, rely=0.4, anchor=CENTER)
        #mem_3_lastname_ent.grid(row=7, column=1, padx=5, pady=10)

        #mem_3_faculty_ent = Entry(self, width=30, font=controller.normal_font)
        #mem_3_faculty_ent.place(relx=0.66, rely=0.5, anchor=CENTER)
        #mem_3_faculty_ent.grid(row=9, column=1, padx=5, pady=10)

        OPTIONS = ["Science", "Business", "Law", "FASS", "Engineering", "Medicine", "Computing", "Dentistry", "Design & Engineering", "Others"]
        mem_3_faculty_ent = StringVar(self)
        mem_3_faculty_ent.set("") #default value

        w = OptionMenu(self, mem_3_faculty_ent, *OPTIONS)
        w.config(width=25, font=controller.normal_font)
        w.place(relx=0.66, rely=0.5, anchor=CENTER) 

        mem_3_phone_num_ent = Entry(self, width=30, font=controller.normal_font)
        mem_3_phone_num_ent.place(relx=0.66, rely=0.6, anchor=CENTER)
        #mem_3_phone_num_ent.grid(row=11, column=1, padx=5, pady=10)

        mem_3_email_add_ent = Entry(self, width=30, font=controller.normal_font)
        mem_3_email_add_ent.place(relx=0.66, rely=0.7, anchor=CENTER)
        #mem_3_email_add_ent.grid(row=13, column=1, padx=5, pady=10)

        #button commands

        def invalidPhoneNo(phoneNo):
            if phoneNo == "":
                return False
            if (len(phoneNo) != 8) or (not phoneNo.isdigit()):
                return True
            else:
                return False

        def email_used(email):
            mycursor.execute("SELECT eMail FROM LibMembers WHERE eMail = %s", (email,))
            result = mycursor.fetchall()
            if len(result) == 0: 
                return False
            return True

        def get_error():
            err = ""
            if mem_3_firstname_ent.get() == "" or mem_3_email_add_ent.get() == "":
                err += "\nMissing mandatory field (First name, email);"
            if invalidPhoneNo(mem_3_phone_num_ent.get()):
                err += "\nInvalid phone number entered;"
            if email_used(mem_3_email_add_ent.get()):
                err += "\nEmail is currently in use;"
            err = err[:-1]
            return err
            
        def which_popup(): 
            error_string = get_error()

            if error_string == "":
                global pop1
                pop1 = Toplevel(self)
                pop1.title("Confirm update details")
                pop1.geometry("600x400")
                pop1.config(bg="#3ac5a5")

                update_frame = Frame(pop1, bg="#3ac5a5")
                update_frame.place(anchor = CENTER)

                pop1_label_main = Label(pop1, text="Please Confirm Updated Details to be Correct", font=controller.title_font)
                pop1_label_main.place(relx = 0.5, rely = 0.1, anchor = CENTER)
                
                pop1_label_memID = Label(pop1, text= mem_3_id_ent.get(), font=controller.normal_font)
                pop1_label_memID.place(relx = 0.5, rely = 0.2, anchor = CENTER)

                pop1_label_firstname = Label(pop1, text= mem_3_firstname_ent.get(), font=controller.normal_font)
                pop1_label_firstname.place(relx = 0.5, rely = 0.3, anchor = CENTER)

                pop1_label_lastname = Label(pop1, text= mem_3_lastname_ent.get(), font=controller.normal_font)
                pop1_label_lastname.place(relx = 0.5, rely = 0.4, anchor = CENTER)

                pop1_label_fac = Label(pop1, text= mem_3_faculty_ent.get(), font=controller.normal_font)
                pop1_label_fac.place(relx = 0.5, rely = 0.5, anchor = CENTER)

                pop1_label_phonenum = Label(pop1, text= mem_3_phone_num_ent.get(), font=controller.normal_font)
                pop1_label_phonenum.place(relx = 0.5, rely = 0.6, anchor = CENTER)

                pop1_label_email = Label(pop1, text= mem_3_email_add_ent.get(), font=controller.normal_font)
                pop1_label_email.place(relx = 0.5, rely = 0.7, anchor = CENTER)

                confirm = Button(pop1, text="Confirm Update", font=controller.normal_font, command= lambda: [success_popup(), pop1.destroy()])
                confirm.place(relx = 0.33, rely = 0.85, anchor = CENTER)

                back = Button(pop1, text="Back to Update function", font=controller.normal_font, 
                command= lambda: [controller.show_frame("Mem_3_Update_Page1"), pop1.destroy()])
                back.place(relx = 0.66, rely = 0.85, anchor = CENTER)

            else:
                global pop2
                pop2 = Toplevel(self)
                pop2.title("Error!")
                pop2.geometry("600x400")
                pop2.config(bg="#C53A5A")

                pop2_label1 = Label(pop2, text="Error!", font=controller.normal_font)
                pop2_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                pop2_label2 = Label(pop2, text=error_string, font=controller.normal_font)
                pop2_label2.place(relx=0.5, rely=0.5, anchor=CENTER)
                error_frame = Frame(pop2, bg="#C53A5A")
                error_frame.place(anchor=CENTER)

                back = Button(pop2, text="Back to Update Function", font=controller.normal_font, command=lambda: [controller.show_frame("Mem_3_Update_Page1"), pop2.destroy()])
                back.place(relx=0.5, rely=0.75, anchor=CENTER)



        def success_popup():
            global pop3
            pop3 = Toplevel(self)
            pop3.title("Success!")
            pop3.geometry("600x400")
            pop3.config(bg="#3ac5a5")

            pop3_label1 = Label(pop3, text="Success!", font=controller.normal_font)
            pop3_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
            pop3_label2 = Label(pop3, text="ALS membership updated.", font=controller.normal_font)
            pop3_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

            success_frame = Frame(pop1, bg="#3ac5a5")
            success_frame.place(anchor=CENTER)

            another= Button(pop1, text="Create another member", font=controller.normal_font, command=lambda: controller.show_frame("Mem_1_Creation"))
            another.place(relx=0.33, rely=0.75, anchor=CENTER)

            back= Button(pop1, text="Back to Update Function", font=controller.normal_font, bg="#b1b8c0", command=lambda: [controller.show_frame("Mem_3_Update_Page1"), pop3.destroy()])
            back.place(relx=0.66, rely=0.75, anchor=CENTER)

            sql = "UPDATE LibMembers SET fName = %s, lName = %s, faculty = %s, phoneNo = %s, eMail = %s WHERE membershipID = %s"
            val = (mem_3_firstname_ent.get(), mem_3_lastname_ent.get(), mem_3_faculty_ent.get(), mem_3_phone_num_ent.get(), mem_3_email_add_ent.get(), mem_3_id_ent.get())
            mycursor.execute(sql, val)
            mydb.commit()



        #buttons
        mem_3_updateButton = Button(self, text="Update Member", padx=10, pady=10, font=controller.normal_font, bg="#b1b8c0", 
        command= which_popup) #which_popup)
        mem_3_updateButton.place(relx=0.25, rely=0.85, anchor=CENTER)
        #mem_3_updateButton.grid(row=80, column=2, padx=10, pady=10)

        mem_3_menuButton = Button(self, text="Back to Membership Menu", padx=10, pady=10, font=controller.normal_font, bg="#b1b8c0",
        command=lambda: controller.show_frame("MembershipMenu"))
        mem_3_menuButton.place(relx=0.5, rely=0.85, anchor=CENTER)
        #mem_3_menuButton.grid(row=80, column=1, sticky="E", padx=10, pady=10)

        mainmenuButton = Button(self, text="Back to Main Menu", padx=10, pady=10, font=controller.normal_font, bg="black", fg="white", 
        command=lambda: controller.show_frame("MainMenu"))
        mainmenuButton.place(relx=0.75, rely=0.85, anchor=CENTER)
        #mainmenuButton.grid(row=80, column=0, sticky="E", padx=10, pady=10)
                        



