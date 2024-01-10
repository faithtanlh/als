from tkinter import * 

class MembershipMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        bg_path = "membg.png"
        self.bg = PhotoImage(file=bg_path)
        label_bkgr = Label(self, image=self.bg)
        label_bkgr.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.controller = controller

        label = Label(self, text="Membership Menu", font=controller.title_font, bg="#b1b8c0", relief="solid")
        label.place(relx=0.5, rely=0.15, anchor="center")

        container = Frame(self)
        container.place(anchor="center")

        b1 = Button(self, text="Create Member", font=controller.normal_font, bg="#b1b8c0", 
        command=lambda: controller.show_frame("Mem_1_Creation"))
        b1.place(relx=0.25, rely=0.4, anchor="center")
        b1.config(height = 5, width = 20 )

        b2 = Button(self, text="Delete Member", font=controller.normal_font, bg="#b1b8c0", 
        command=lambda: controller.show_frame("Mem_2_Deletion"))
        b2.place(relx=0.5, rely=0.4, anchor="center")
        b2.config(height = 5, width = 20 )

        b3 = Button(self, text="Update Member", font=controller.normal_font, bg="#b1b8c0", 
        command=lambda: controller.show_frame("Mem_3_Update_Page1"))
        b3.place(relx=0.75, rely=0.4, anchor="center")
        b3.config(height = 5, width = 20 )

        b4 = Button(self, text="Back to Main Menu", font=controller.normal_font, bg="black", fg="white",
        command=lambda: controller.show_frame("MainMenu"))
        b4.place(relx=0.5, rely=0.7, anchor="center")
        b4.config(height = 5, width = 20 )