import tkinter as tk

class AccountManager(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        frameContainer = tk.Frame(self)

        frameContainer.pack(side="top", fill="both", expand = True)

        frameContainer.grid_rowconfigure(0, weight=1)
        frameContainer.grid_columnconfigure(0, weight=1)
        
        self.frames = {}  # Dictionary hold frames which represent pages
        
        for page in (LoginPage, CreateUserPage):
            frame = page(frameContainer, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(LoginPage)

    def show_frame(self, content):
        frame = self.frames[content]
        frame.tkraise()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.userL = tk.Label(self, text= "Username")
        self.passwordL = tk.Label(self, text= "Password")
        self.userL.grid(row=0, column=0, sticky="E")
        self.passwordL.grid(row=1, column=0, sticky="E")

        self.userE = tk.Entry(self, width=35)
        self.passwordE = tk.Entry(self, width=35, show="*")
        self.userE.grid(row=0, column=1)
        self.passwordE.grid(row=1, column=1)

        self.loginB = tk.Button(self, text= "Login", command = self.login)
        self.createB = tk.Button(self, text= "Create Account", command= lambda: controller.show_frame(CreateUserPage))
        self.loginB.grid(row=2, column=0)
        self.createB.grid(row=2, column=1)

    def login(self):
        self.errorL = tk.Label(self, text= "Username or Password incorrect")
        self.username = self.userE.get()
        self.password = self.passwordE.get()
        filename = self.username + '.txt'
        try:
            f = open(filename, "r")
            sevedPass = f.readline()
            if self.password == sevedPass:
                # Temp Labels until proper functionallity implemented
                self.errorL.destroy()
                self.successL = tk.Label(self, text = "Login Successful")
                self.successL.grid(row=3, columnspan=2)
            else:
                self.errorL.grid(row=3, column=0, columnspan=2)
        except:
            self.errorL.grid(row=3, column=0, columnspan=2)


class CreateUserPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.userL = tk.Label(self, text= "Username")
        self.passwordL = tk.Label(self, text= "Password")
        self.passwordL2 = tk.Label(self, text= "Password")
        self.userL.grid(row=0, column=0, sticky="E")
        self.passwordL.grid(row=1, column=0, sticky="E")
        self.passwordL2.grid(row=2, column=0, sticky="E")

        self.userE = tk.Entry(self, width=35)
        self.passwordE1 = tk.Entry(self, width=35, show="*")
        self.passwordE2 = tk.Entry(self, width=35, show="*")
        self.userE.grid(row=0, column=1)
        self.passwordE1.grid(row=1, column=1)
        self.passwordE2.grid(row=2, column=1)

        self.backB = tk.Button(self, text = "Back", command = lambda: controller.show_frame(LoginPage))
        self.createUserB = tk.Button(self, text = "Create Account", command= lambda: self.createUser(controller))
        self.backB.grid(row=3, column = 0)
        self.createUserB.grid(row=3, column=1)

    def createUser(self, controller):
        username = self.userE.get()
        password = self.passwordE1.get()
        rePassword = self.passwordE2.get()
        if password == rePassword:
            filename = username + '.txt'
            f = open(filename, "w")
            f.write(password)
            f.close
            controller.show_frame(LoginPage)
        else:
            self.errorL = tk.Label(self, text = "Passwords do not match")
            self.errorL.grid(row=4, columnspan=2)
        

app = AccountManager()
app.mainloop()