import tkinter as tk
from tkinter import ttk


class AccountManager(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Account Manager")
        tk.Tk.wm_resizable(self, width=False, height=False)

        frameContainer = tk.Frame(self)
        frameContainer.pack(side="top", fill="both", expand = True)
        frameContainer.grid_rowconfigure(0, weight=1)
        frameContainer.grid_columnconfigure(0, weight=1)

        self.filename = ""  # The filename to be opened when successful login occurs
        self.frames = {}    # Dictionary hold frames which represent pages
        
        for page in (LoginPage, CreateUserPage, HomePage):
            frame = page(frameContainer, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(LoginPage)

    def show_frame(self, content):
        # self: The AccountManager class
        # content: A class name to be fetched from frames to bring new frame to top
        frame = self.frames[content]
        frame.tkraise()

    def loginSuccess(self, filename):
        # self: The AccountManager class
        # filename: The name of file that was used for successful login
        self.filename = filename
        self.show_frame(HomePage)

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        # self: The LoginPage class
        # parent: The frameContainer
        # controller: The AccountManager class

        tk.Frame.__init__(self, parent)
        self.userL = ttk.Label(self, text= "Username")
        self.passwordL = ttk.Label(self, text= "Password")
        self.userL.grid(row=0, column=0, sticky="E")
        self.passwordL.grid(row=1, column=0, sticky="E")
        
        self.userE = ttk.Entry(self, width=35)
        self.passwordE = ttk.Entry(self, width=35, show="*")
        self.userE.grid(row=0, column=1)
        self.passwordE.grid(row=1, column=1)

        self.loginB = ttk.Button(self, text= "Login", command = lambda: self.login(controller))
        self.createB = ttk.Button(self, text= "Sign up", command= lambda: controller.show_frame(CreateUserPage))
        self.loginB.grid(row=2, column=0, columnspan=2)
        self.createB.grid(row=3, column=0, columnspan=2)

    def login(self, controller):
        # self: The LoginPage class
        # controller: The AccountManager class

        self.errorL = ttk.Label(self, text= "Username or Password incorrect")
        self.username = self.userE.get()
        self.password = self.passwordE.get()
        filename = self.username + '.txt'
        try:
            f = open(filename, "r")
            sevedPass = f.readline()
            if self.password == sevedPass:
                controller.loginSuccess(self.username)
            else:
                self.errorL.grid(row=4, column=0, columnspan=2)
        except:
            self.errorL.grid(row=4, column=0, columnspan=2)


class CreateUserPage(tk.Frame):
    def __init__(self, parent, controller):
        # self: The CreateUserPage class
        # parent: The frameContainer
        # controller: The AccountManager class

        tk.Frame.__init__(self, parent)
        self.instructionL = ttk.Label(self, text="Username and password must be 8 characters minimum")
        self.userL = ttk.Label(self, text= "Username")
        self.passwordL = ttk.Label(self, text= "Password")
        self.passwordL2 = ttk.Label(self, text= "Password")
        self.instructionL.grid(row=0, columnspan=2)
        self.userL.grid(row=1, column=0, sticky="E")
        self.passwordL.grid(row=2, column=0, sticky="E")
        self.passwordL2.grid(row=3, column=0, sticky="E")

        self.userE = ttk.Entry(self, width=35)
        self.passwordE1 = ttk.Entry(self, width=35, show="*")
        self.passwordE2 = ttk.Entry(self, width=35, show="*")
        self.userE.grid(row=1, column=1)
        self.passwordE1.grid(row=2, column=1)
        self.passwordE2.grid(row=3, column=1)

        self.backB = ttk.Button(self, text = "Back", command = lambda: controller.show_frame(LoginPage))
        self.createUserB = ttk.Button(self, text = "Create Account", command= lambda: self.createUser(controller))
        self.backB.grid(row=4, column = 0)
        self.createUserB.grid(row=4, column=1)

    def createUser(self, controller):
        # self: The CreateUserPage class
        # controller: The AccountManger class

        username = self.userE.get()
        password = self.passwordE1.get()
        rePassword = self.passwordE2.get()
        if len(username) < 8 or len(password) < 8:
            self.errorL = tk.Label(self, text = "Username or password isn't long enough")
            self.errorL.grid(row=5, columnspan=2)
        elif password == rePassword:
            filename = username + '.txt'
            # Check to see if the username already exists
            try: 
                f = open(filename, "r")
                self.errorL = tk.Label(self, text = "Username is not avaialable")
                self.errorL.grid(row=5, columnspan=2)
                f.close()
            except:
                f = open(filename, "w")
                f.write(password)
                f.close()
                self.clearEntries() # Clear entry field once leaving create user page
                controller.show_frame(LoginPage)
            f.close()
        else:
            self.errorL = tk.Label(self, text = "Passwords do not match")
            self.errorL.grid(row=5, columnspan=2)

    def clearEntries(self):
        #self: The CreateUserPage class

        self.userE.delete(0, 'end')
        self.passwordE1.delete(0, 'end')
        self.passwordE2.delete(0, 'end')

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        # self: The HomePage class
        # parent: The frameContainer
        # controller: The AccountManager class

        tk.Frame.__init__(self, parent)
        self.viewPassesB = ttk.Button(self, text = "View Passwords")
        self.createPassB = ttk.Button(self, text = "Create New Password")
        self.logoutB = ttk.Button(self, text = "Logout")
        self.viewPassesB.grid(row = 0, column = 0)
        self.createPassB.grid(row = 0, column = 1)
        self.logoutB.grid(row = 0, column = 2)
        

app = AccountManager()

app.mainloop()