from tkinter import  *
from PIL import ImageTk
import os

class Homepage:
    def __init__(self,root):
        self.root = root
        self.root.title('Offline Purchase Order Management System')
        self.root.geometry('1200x1200')
        self.root.resizable(False, False)

        self.bg = ImageTk.PhotoImage(file="C:\\Users\\Christian Paul Colo\Pictures\\Saved Pictures\\backg.jpg")
        self.bg_image = Label(self.root, image=self.bg).place(x=0, y=0, width=1200, height=1200)
        self.bttn = Button(root,text="Open Shop",bg="#FFFFB6",fg="#191919",bd=2,font=("garamond",15),command=self.Menu) . place(x=450,y=230,width=300,height=55)
        self.bttn = Button(root, text="Admin Login", bg="#FFFFB6", fg="black", bd=2, font=("garamond", 15),command=self.records).place(x=450, y=295, width=300,height=55)

    def Menu(self):
        root.destroy()
        os.system('python menu.py')
    def records(self):
        root.destroy()
        os.system('python admin.py')


root = Tk()
obj = Homepage(root)
root.mainloop()