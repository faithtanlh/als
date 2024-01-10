from tkinter import *    
from BT2102_ALS_functions import * 
import mysql.connector 
from tkinter import font as tkfont 
from MainMenu import MainMenu
from MembershipMenu import MembershipMenu
from BookMenu import BookMenu
from LoanMenu import LoanMenu
from ReservationMenu import ReservationMenu
from FineMenu import FineMenu
from ReportMenu import ReportMenu
from Mem_1_Creation import Mem_1_Creation
from Mem_2_Deletion import Mem_2_Deletion
from Mem_3_Update_Page1 import Mem_3_Update_Page1
from Mem_3_Update_Page2 import Mem_3_Update_Page2
from Boo_4_Acquisition import Boo_4_Acquisition
from Boo_5_Withdrawal import Boo_5_Withdrawal
from Loa_6_Borrow import Loa_6_Borrow
from Loa_7_Return import Loa_7_Return
from Res_8_MakeRes import Res_8_MakeRes
from Res_9_CancelRes import Res_9_CancelRes
from Fin_10_Payment import Fin_10_Payment
from Rep_11_Search import Rep_11_Search
from Rep_15_Display_Book_Loan_To_Member import Rep_15_Display_Book_Loan_To_Member 
from SQLpassword import get_password

my_password = get_password()
mydb = mysql.connector.connect(
host = "localhost", 
user = "root", 
passwd = my_password, 
database = "libals")

mycursor = mydb.cursor()


class Root(Tk):

    bg_path = "startpagebg.png"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.title_font = tkfont.Font(family='System', size=18, weight="bold")
        self.bg = PhotoImage(file=self.bg_path)
        

        self.normal_font = tkfont.Font(family="System", size=8)

        self.frames = {}
        for F in (StartPage, MainMenu, MembershipMenu, BookMenu, LoanMenu, ReservationMenu, FineMenu
        , ReportMenu, Mem_1_Creation, Mem_2_Deletion, Mem_3_Update_Page1, Mem_3_Update_Page2, Boo_4_Acquisition, Boo_5_Withdrawal,
        Loa_6_Borrow, Loa_7_Return, Res_8_MakeRes, Res_9_CancelRes, Fin_10_Payment, Rep_11_Search, Rep_15_Display_Book_Loan_To_Member):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise() 
        
    def get_page(self, classname):
        '''Returns an instance of a page given it's class name as a string'''
        for page in self.frames.values():
            if str(page.__class__.__name__) == classname:
                return page
        return None     

class BasePage(Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        label_bkgr = Label(self, image=controller.bg)
        label_bkgr.place(relx=0.5, rely=0.5, anchor=CENTER)  # Center label w/image.

class StartPage(BasePage):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        # label = Label(self, text="Group70 Library System", font=controller.title_font, bg="#d1cbcd", fg="black")
        # label.place(relx=0.5, rely=0.2, anchor="center")

        button1 = Button(self, text="Go to Main Menu", bg="#d1cbcd", font=controller.normal_font,
                            command=lambda: controller.show_frame("MainMenu"))
        button1.place(relx=0.5, rely=0.5, anchor="center")
        button1.config(height = 5, width = 20 )  ##change button size




if __name__ == "__main__":
    root = Root()
    root.geometry("1280x720")
    #root.attributes('-fullscreen', True) 
    root.mainloop()



