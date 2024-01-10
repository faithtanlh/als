from tkinter import *

class MainMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        bg_path = "mainmenubg.png"
        self.bg = PhotoImage(file=bg_path)
        label_bkgr = Label(self, image=self.bg)
        label_bkgr.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.controller = controller

        label = Label(self, text="Main Menu", font=controller.title_font, bg="#b1b8c0", relief="solid")
        label.place(relx=0.5, rely=0.15, anchor="center")

        container = Frame(self)
        container.place(anchor="center")

        b1 = Button(self, text="Membership Menu", font=controller.normal_font, bg="#b1b8c0", 
        command=lambda: controller.show_frame("MembershipMenu"))
        b1.place(relx=0.25, rely=0.4, anchor="center")
        b1.config(height = 5, width = 20 )

        b2 = Button(self, text="Books Menu", font=controller.normal_font, bg="#b1b8c0", 
        command=lambda: controller.show_frame("BookMenu"))
        b2.place(relx=0.50, rely=0.4, anchor="center")
        b2.config(height = 5, width = 20 )

        b3 = Button(self, text="Loan Menu", font=controller.normal_font, bg="#b1b8c0", 
        command=lambda: controller.show_frame("LoanMenu"))
        b3.place(relx=0.75, rely=0.4, anchor="center")
        b3.config(height = 5, width = 20 )

        b4 = Button(self, text="Fine Menu", font=controller.normal_font, bg="#b1b8c0", 
        command=lambda: controller.show_frame("FineMenu"))
        b4.place(relx=0.25, rely=0.7, anchor="center")
        b4.config(height = 5, width = 20 )

        b5 = Button(self, text="Reservation Menu", font=controller.normal_font, bg="#b1b8c0", 
        command=lambda: controller.show_frame("ReservationMenu"))
        b5.place(relx=0.50, rely=0.7, anchor="center")
        b5.config(height = 5, width = 20 )

        b6 = Button(self, text="Report Menu", font=controller.normal_font, bg="#b1b8c0",
        command=lambda: controller.show_frame("ReportMenu"))
        b6.place(relx=0.75, rely=0.7, anchor="center")
        b6.config(height = 5, width = 20 )



        
