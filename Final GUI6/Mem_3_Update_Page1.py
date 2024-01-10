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

class Mem_3_Update_Page1(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        bg_path = "membg.png"
        self.bg = PhotoImage(file=bg_path)
        label_bkgr = Label(self, image=self.bg)
        label_bkgr.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        self.controller = controller

        ## Membership Update Page 1
        #instruction 
        mem_3_instruction = Label(self, text = "To update a member, please enter Membership ID", font=controller.title_font, bg="#b1b8c0")
        mem_3_instruction.place(relx=0.5, rely=0.25, anchor=CENTER)
        #mem_3_instruction.grid(row=1, column=1, sticky="W", pady=5)

        #labels
        mem_3_id_lab = Label(self, text = "Membership ID", font=controller.normal_font, bg="#b1b8c0")
        mem_3_id_lab.place(relx=0.33, rely=0.5, anchor=CENTER)
        #mem_3_id_lab.grid(row=5, column=0, sticky="E", padx=5, pady=10)

        #entry box
        mem_3_id_ent = Entry(self, width=30, font=controller.normal_font)
        mem_3_id_ent.place(relx=0.66, rely=0.5, anchor=CENTER)
        #mem_3_id_ent.grid(row=5, column=1, padx=5, pady=10)

        self.mem_id = mem_3_id_ent

        def checkMemberExists(mem_id):
            mycursor.execute("SELECT membershipID FROM LibMembers WHERE membershipID = %s", (mem_id,))
            result = mycursor.fetchall()
            if len(result) == 0: 
                return False
            print("Member exists")
            return True

        def update2_or_menu():
            if checkMemberExists(mem_3_id_ent.get()):
                return self.controller.show_frame("Mem_3_Update_Page2")
            else:
                global pop1
                pop1 = Toplevel(self)
                pop1.title("Error")
                pop1.geometry("600x400")
                pop1.config(bg="#C53A5A")

                error_frame = Frame(pop1, bg="#C53A5A")
                error_frame.place(anchor = CENTER)

                pop1_label1 = Label(pop1, text="Error!", font=controller.normal_font)
                pop1_label1.place(relx = 0.5, rely = 0.25, anchor = CENTER)
                pop1_label2 = Label(pop1, text="Invalid membership ID", font=controller.normal_font)
                pop1_label2.place(relx = 0.5, rely = 0.5, anchor = CENTER)

                back = Button(pop1, text="Back to Update Function", font=controller.normal_font, command=lambda: [controller.show_frame("Mem_3_Update_Page1"), pop1.destroy()])
                back.place(relx = 0.5, rely = 0.75, anchor = CENTER)
                    


        #buttons
        mem_3_updateButton = Button(self, text="Update Member", padx=10, pady=10, font=controller.normal_font, bg="#b1b8c0", 
        command=update2_or_menu)
        mem_3_updateButton.place(relx=0.25, rely=0.75, anchor=CENTER)
        #mem_3_updateButton.grid(row=80, column=2, padx=10, pady=10)

        mem_3_menuButton = Button(self, text="Back to Membership Menu", padx=10, pady=10, font=controller.normal_font, bg="#b1b8c0", 
        command=lambda: controller.show_frame("MembershipMenu"))
        mem_3_menuButton.place(relx=0.5, rely=0.75, anchor=CENTER)
        #mem_3_menuButton.grid(row=80, column=1, sticky="E", padx=10, pady=10)

        mainmenuButton = Button(self, text="Back to Main Menu", padx=10, pady=10, font=controller.normal_font, bg="black", fg="white", 
        command=lambda: controller.show_frame("MainMenu"))
        mainmenuButton.place(relx=0.75, rely=0.75, anchor=CENTER)
        #mainmenuButton.grid(row=80, column=0, sticky="E", padx=10, pady=10)
                




