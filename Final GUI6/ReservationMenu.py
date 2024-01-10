from tkinter import * 

class ReservationMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        bg_path = "resbg.png"
        self.bg = PhotoImage(file=bg_path)
        label_bkgr = Label(self, image=self.bg)
        label_bkgr.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.controller = controller

        label = Label(self, text="Reservation Menu", font=controller.title_font, bg="#b1b8c0", relief="solid")
        label.place(relx=0.5, rely=0.2, anchor="center")

        container = Frame(self)
        container.place(anchor="center")

        b1 = Button(self, text="Make a Reservation", font=controller.normal_font, bg="#b1b8c0", 
         command=lambda: controller.show_frame("Res_8_MakeRes"))
        b1.place(relx=0.25, rely=0.5, anchor="center")
        b1.config(height = 5, width = 20 )

        b2 = Button(self, text="Cancel a Reservation", font=controller.normal_font, bg="#b1b8c0", 
        command=lambda: controller.show_frame("Res_9_CancelRes"))
        b2.place(relx=0.50, rely=0.5, anchor="center")
        b2.config(height = 5, width = 20 )

        b3 = Button(self, text="Back to Main Menu", font=controller.normal_font, bg="black", fg="white", 
        command=lambda: controller.show_frame("MainMenu"))
        b3.place(relx=0.75, rely=0.5, anchor="center")
        b3.config(height = 5, width = 20 )