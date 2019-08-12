import tkinter as tk
from tkinter import ttk
import random


class AccountManager(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Account Manager")
        tk.Tk.wm_resizable(self, width=False, height=False)

        self.frameContainer = tk.Frame(self)
        self.frameContainer.pack(side="top", fill="both", expand = True)
        self.frameContainer.grid_rowconfigure(0, weight=1)
        self.frameContainer.grid_columnconfigure(0, weight=1)

        self.frames = {}    # Dictionary hold frames which represent pages
        
        for page in (LoginPage, CreateUserPage):
            frame = page(self.frameContainer, self)
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
        for page in (HomePage, PasswordViewPage, CreatePasswordPage):
            frame = page(self.frameContainer, self, filename)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
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
            savedPass = f.readline()
            savedPass = savedPass.split('~.|')
            if self.password == savedPass[0]:
                self.userE.delete(0, 'end')
                self.passwordE.delete(0, 'end')
                controller.loginSuccess(self.username + '.txt')
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
                f.write(password + '~.|' + '\n')
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
    def __init__(self, parent, controller, filename):
        # self: The HomePage class
        # parent: The frameContainer
        # controller: The AccountManager class
        # filename: Name of file for current logged in User

        tk.Frame.__init__(self, parent)
        self.filename = filename
        self.viewPassesB = ttk.Button(self, text = "View Passwords", command = lambda: controller.show_frame(PasswordViewPage))
        self.createPassB = ttk.Button(self, text = "Create New Password", command = lambda: controller.show_frame(CreatePasswordPage))
        self.logoutB = ttk.Button(self, text = "Logout", command = lambda: controller.show_frame(LoginPage))
        self.viewPassesB.grid(row = 0, column = 0)
        self.createPassB.grid(row = 0, column = 1)
        self.logoutB.grid(row = 0, column = 2)
  
        
class PasswordViewPage(tk.Frame):
    def __init__(self, parent, controller, filename):
        # self: The PasswordViewPage class
        # parent: The frameContainer
        # controller: The AccountManager class
        # filename: Name of file for current logged in User

        tk.Frame.__init__(self, parent)
        self.homeB = ttk.Button(self, text = "Home", command = lambda: controller.show_frame(HomePage))
        self.homeB.grid(row=0, column=0)

class CreatePasswordPage(tk.Frame):
    def __init__(self, parent, controller, filename):
        # self: The CreatePasswordPage class
        # parent: The frameContainer
        # controller: The AccountManager class
        # filename: Name of file for current logged in User

        tk.Frame.__init__(self, parent)
        self.filename = filename
        self.homeB = ttk.Button(self, text = "Home", command = lambda: self.goHome(controller))
        self.homeB.grid(row=0, column=0)

        self.rowEntryStart = 1
        self.websiteL = ttk.Label(self, text = "Website")
        self.usernameL = ttk.Label(self, text = "Username")
        self.passwordL = ttk.Label(self, text = "Password")
        self.websiteL.grid(row=self.rowEntryStart, column=0)
        self.usernameL.grid(row=self.rowEntryStart+1, column=0)
        self.passwordL.grid(row=self.rowEntryStart+2 , column=0)

        self.websiteE = ttk.Entry(self, width=35)
        self.usernameE = ttk.Entry(self, width=35)
        self.passwordE = ttk.Entry(self, width=35)
        self.websiteE.grid(row=self.rowEntryStart, column=1)
        self.usernameE.grid(row=self.rowEntryStart+1, column=1)
        self.passwordE.grid(row=self.rowEntryStart+2, column=1)

        self.randPassB = ttk.Button(self, text = "Generate Strong Password", command = self.generatePassword)
        self.saveAccountB = ttk.Button(self, text = "Save Account", command = self.saveAccountData)
        self.randPassB.grid(row=self.rowEntryStart+3, columnspan=2)
        self.saveAccountB.grid(row=self.rowEntryStart+4, columnspan=2)

    def generatePassword(self):
        # self: The CreatePasswordPage class
        # Generate a random 16 length password and display it in password entry field
        self.passwordE.delete(0, 'end')
        chars = 'abcdefghijklmnopqrstuvwxyz'
        password = ''
        for i in range(16):
            if random.choice([True, True, False]):
                if random.choice([True, True, False]):
                    password = password + random.choice(chars)
                else:
                    password = password + random.choice(chars).upper()
            else:
                password = password + str(random.randint(0,9))
        self.passwordE.insert(0, password)

    def saveAccountData(self):
        # self: The CreatePasswordPage class
        # Retrieve data from the entry fields, check correctness and append data to users file
        website = self.websiteE.get()
        username = self.usernameE.get()
        password = self.passwordE.get()
        if len(website) < 1 or len(username) < 1 or len(password) < 1:
            self.errorL = ttk.Label(self, text = "Text fields cannot be blank")
            self.errorL.grid(row=self.rowEntryStart+5, columnspan=2)
        else:
            with open(self.filename, "a") as f:
                f.write(website + '~.|' + username + '~.|' + password + '\n')
                f.close()
            self.clearEntries()

    def clearEntries(self):
        # self: The CreatePasswordPage class
        # Clears all entry fields 
        self.websiteE.delete(0, 'end')
        self.usernameE.delete(0, 'end')
        self.passwordE.delete(0, 'end')

    def goHome(self, controller):
        # self: The CreatePasswordPage class
        # controller: The AccountManager class
        # Clears Entries before returning to home page
        self.clearEntries()
        controller.show_frame(HomePage)
    


        

app = AccountManager()

app.mainloop()