from tkinter import *

window = Tk()
window.withdraw()
window.title("Account Manager")

class LoginScreen:
    def __init__(self, master):
        top = self.top =Toplevel(master)
        top.title("Login")
        top.resizable(width=False, height=False)
        self.userL = Label(top, text= "Username")
        self.passwordL = Label(top, text= "Password")
        self.userL.grid(row=0, column=0, sticky=E)
        self.passwordL.grid(row=1, column=0, sticky=E)

        self.userE = Entry(top, width=35)
        self.passwordE = Entry(top, width=35, show="*")
        self.userE.grid(row=0, column=1)
        self.passwordE.grid(row=1, column=1)

        self.loginB = Button(top, text= "Login", command=self.login)
        self.createB = Button(top, text= "Create Account")
        self.loginB.grid(row=3, column=0)
        self.createB.grid(row=4, column=0)

    def login(self):
        self.errorL = Label(self.top, text= "Username or Password incorrect")
        self.username = self.userE.get()
        self.password = self.passwordE.get()
        fileName = self.username + '.txt'
        try:
            f = open(fileName, 'r')
            savedPass = f.readline()
            if self.password == savedPass:
                pass
            else:
                self.errorL.grid(row=2, column=0, columnspan=2)
        except:
            self.errorL.grid(row=2, column=0, columnspan=2)

w = LoginScreen(window)

window.mainloop()