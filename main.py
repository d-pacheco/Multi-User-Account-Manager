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
        
        for page in (LoginPage, CreateUserPage, EditPasswordPage):
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

    def userLogout(self):
        # self: The AccountManager class
        # Deletes the pages that were made when a user has successfully logged in
        self.show_frame(LoginPage)
        for page in (HomePage, PasswordViewPage, CreatePasswordPage):
            del self.frames[page]

    def PasswordViewRefresh(self):
        page = self.frames[PasswordViewPage]
        page.refreshData()

    def goToEditPage(self, website, username, password):
        page = self.frames[EditPasswordPage]
        page.setUserData(website, username, password)
        self.show_frame(EditPasswordPage)

    def saveEditFromEditPage(self, website, username, password):
        page = self.frames[PasswordViewPage]
        page.saveEditChanges(website, username, password)


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        # self: The LoginPage class
        # parent: The frameContainer
        # controller: The AccountManager class

        tk.Frame.__init__(self, parent)
        self.userL = tk.Label(self, text= "Username")
        self.passwordL = tk.Label(self, text= "Password")
        self.userL.grid(row=0, column=0, sticky="E")
        self.passwordL.grid(row=1, column=0, sticky="E")
        
        self.userE = tk.Entry(self, width=35)
        self.passwordE = tk.Entry(self, width=35, show="*")
        self.userE.grid(row=0, column=1)
        self.passwordE.grid(row=1, column=1)

        self.loginB = ttk.Button(self, text= "Login", command = lambda: self.login(controller))
        self.createB = ttk.Button(self, text= "Sign up", command= lambda: controller.show_frame(CreateUserPage))
        self.loginB.grid(row=2, column=0, columnspan=2)
        self.createB.grid(row=3, column=0, columnspan=2)

    def login(self, controller):
        # self: The LoginPage class
        # controller: The AccountManager class
        self.errorL = tk.Label(self, text= "Username or Password incorrect")
        self.username = self.userE.get()
        self.password = self.passwordE.get()
        filename = userToFilename(self.username)
        try:
            f = open(filename, "r")
            savedPass = f.readline()
            savedPass = savedPass.strip()
            if encrypt(self.password) == savedPass:
                self.userE.delete(0, 'end')
                self.passwordE.delete(0, 'end')
                controller.loginSuccess(filename)
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
        self.instructionL = tk.Label(self, text="Username and password must be 8 characters minimum")
        self.userL = tk.Label(self, text= "Username")
        self.passwordL = tk.Label(self, text= "Password")
        self.passwordL2 = tk.Label(self, text= "Password")
        self.instructionL.grid(row=0, columnspan=2)
        self.userL.grid(row=1, column=0, sticky="E")
        self.passwordL.grid(row=2, column=0, sticky="E")
        self.passwordL2.grid(row=3, column=0, sticky="E")

        self.userE = tk.Entry(self, width=35)
        self.passwordE1 = tk.Entry(self, width=35, show="*")
        self.passwordE2 = tk.Entry(self, width=35, show="*")
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
            filename = userToFilename(username)
            # Check to see if the username already exists
            try: 
                f = open(filename, "r")
                self.errorL = tk.Label(self, text = "Username is not avaialable")
                self.errorL.grid(row=5, columnspan=2)
                f.close()
            except:
                f = open(filename, "w")
                f.write(encrypt(password) + '\n')
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
        self.viewPassesB.grid(row = 0, column = 0)
        self.createPassB.grid(row = 0, column = 1)
        self.logoutB = ttk.Button(self, text = "Logout", command = controller.userLogout)
        self.logoutB.grid(row = 0, column = 2, sticky='e')


class PasswordViewPage(tk.Frame):
    def __init__(self, parent, controller, filename):
        # self: The PasswordViewPage class
        # parent: The frameContainer
        # controller: The AccountManager class
        # filename: Name of file for current logged in User

        tk.Frame.__init__(self, parent)
        self.filename = filename
        self.spacing = "                          "
        self.accountData = {}
        self.sortedKeyList = []

        self.homeB = ttk.Button(self, text = "Home", command = lambda: controller.show_frame(HomePage))
        self.homeB.grid(row=0, column=0, sticky = 'w')

        self.searchB = ttk.Button(self, text = "Search", command = self.search)
        self.searchE = tk.Entry(self, width=35)
        self.searchB.grid(row=1, column=3, sticky='w')
        self.searchE.grid(row=1, column=0, sticky='e', columnspan=3)
        self.passwordLB = tk.Listbox(self, height = 8, width = 90, font = ('Courier', 9))
        self.passwordLB.grid(row=2, column=0, columnspan=4)
        self.passwordLB.insert('end', "Website" + self.spacing + "Username"+ self.spacing + "Password")

        self.editB = ttk.Button(self, text = "Edit", command  = lambda: self.editSelect(controller))
        self.editB.grid(row=3, column=1, sticky='e')
        self.deleteB = ttk.Button(self, text = "Delete", command = self.deleteSelect)
        self.deleteB.grid(row=3, column=2, sticky='w')

        self.loadAndDisplayAll()

    def loadAndDisplayAll(self):
        # self: The PasswordViewPage class
        # Opens users file and reads the account data it contains and stores the data in the self.accountData dictionary
        with open(self.filename, "r") as f:
            raw_data = f.readlines()
            raw_data = [line.strip() for line in raw_data]
            raw_data = [line.split('~.|') for line in raw_data]
        f.close()
        
        self.userPass = raw_data[0][0]
        for i in range(len(raw_data)-1):
            self.accountData[raw_data[i+1][0]] = decrypt(raw_data[i+1][1])
        
        self.sortedKeyList = []
        for key in self.accountData:
            self.sortedKeyList.append(key)
        quickSort(self.sortedKeyList, 0, len(self.sortedKeyList)-1)
        self.displayAllData()

    def displayAllData(self):
        # self: The PasswordViewPage class
        # Display the account data stored in the self.accountData dictionary
        for key in self.sortedKeyList:
            self.displayEntry(key)

    def displayEntry(self, key):
        # self: The PasswordViewPage class

        WebsiteUser = key.split("|.~")
        website = WebsiteUser[0]
        username = WebsiteUser[1]

        webSpaceLen = (len("Website") + len(self.spacing)) - len(website)
        webSpace = ""
        for i in range(webSpaceLen):
            webSpace += " "

        userSpaceLen = (len("Username") + len(self.spacing) - len(username))
        userSpace = ""
        for i in range(userSpaceLen):
            userSpace += " "

        self.passwordLB.insert('end', website + webSpace + username + userSpace + self.accountData[key])

    def clearListbox(self):
        # self: The PasswordViewPage class
        # Clears all the entries in the password Listbox and inserts the headers back
        self.passwordLB.delete(0, 'end')
        self.passwordLB.insert('end', "Website" + self.spacing + "Username"+ self.spacing + "Password")

    def search(self):
        # self: The PasswordViewPage class
        searchKey = self.searchE.get()
        self.clearListbox

        keyList = []
        for key in self.accountData:
            if searchKey.lower() in key.lower():
                keyList.append(key)
        quickSort(keyList, 0, len(keyList)-1)
        for key in keyList:
            self.displayEntry(key)

    def getSelect(self):
        # self: The PasswordViewPage class
        # Get the currently selected item from the password Listbox and return that accounts data dict key
        try:
            selection = self.passwordLB.get(self.passwordLB.curselection())
            selection = selection.split()
            dictKey = selection[0] + '|.~' + selection[1]
            return dictKey
        except:
            return False

    def editSelect(self, controller):
        # self: The PasswordViewPage class
        # controller: The AccountManager class
        # Gets the account data slected and passes it to edit password page
        key = self.getSelect()
        if key != "Website|.~Username":
            website, username = key.split("|.~")
            password = self.accountData[key]
            controller.goToEditPage(website, username, password)

    def saveEditChanges(self, website, username, password):
        # self: The PasswordViewPage class
        # Recieves the changed data from the EditPasswordPage and saves/displays the changes
        key = website + "|.~" + username
        self.accountData[key] = password
        self.saveChangedData()
        self.refreshData()

    def deleteSelect(self):
        # self: The PasswordViewPage class
        # Deletes the currently selected account data from the dictionary and calls to write new dictionary to file
        key = self.getSelect()
        if key != False and key != "Website|.~Username":
            del self.accountData[key]
            self.sortedKeyList.remove(key)
            self.saveChangedData()
            self.clearListbox()
            self.displayAllData()

    def saveChangedData(self):
        # self: The PasswordViewPage class
        # Writes the current dictonary to the users file
        file = open(self.filename, "w")
        file.write(self.userPass + '\n')
        for key in self.sortedKeyList:
            file.write(key + '~.|' + encrypt(self.accountData[key]) + '\n')
        file.close

    def refreshData(self):
        # self: The PasswordViewPage class
        # Refresh the listbox to display any changes that could have been made to the dictionary or to the file
        self.clearListbox()
        self.loadAndDisplayAll()

class EditPasswordPage(tk.Frame):
    def __init__(self, parent, controller):
        # self: The EditPasswordVPage class
        # parent: The frameContainer
        # controller: The AccountManager class

        tk.Frame.__init__(self, parent)
        self.errorOccured = False
        self.websiteL = tk.Label(self, text = "Website: ")
        self.passwordL = tk.Label(self, text = "Password: ")
        self.usernameL = tk.Label(self, text = "Username: ")
        self.passwordE = tk.Entry(self, width=35)

        self.websiteL.grid(row=0, column=0)
        self.usernameL.grid(row=1, column=0)
        self.passwordL.grid(row=2, column=0)
        self.passwordE.grid(row=2, column=1)

        self.cancelB = ttk.Button(self, text = "Cancel", command = lambda: self.leavePage(controller))
        self.saveB   = ttk.Button(self, text = "Save", command = lambda: self.saveChangedEntries(controller))
        self.cancelB.grid(row=3, column=0)
        self.saveB.grid(row=3, column=1, sticky="w")

    def setUserData(self, website, username, password):
        # self: The EditPasswordVPage class
        self.website = website
        self.username = username
        self.password = password

        self.userWebsiteL = tk.Label(self, text = self.website)
        self.userWebsiteL.grid(row=0, column=1, sticky="w")
        self.accountUsernameL = tk.Label(self, text = self.username)
        self.accountUsernameL.grid(row=1, column=1, sticky="w")
        self.passwordE.insert(0, self.password)

    def saveChangedEntries(self, controller):
        # self: The EditPasswordVPage class
        # controller: The AccountManager class
        password = self.passwordE.get()
        if len(password) < 1:
            self.errorL = tk.Label(self, text = "Password field can not be blank")
            self.errorL.grid(row=4, column=0, columnspan=2)
            self.errorOccured = True
        else:
            # No changes were actually made
            if password == self.password:
                self.leavePage(controller)
            else:
                controller.saveEditFromEditPage(self.website, self.username, password)
                self.leavePage(controller)

    def leavePage(self, controller):
        # self: The EditPasswordVPage class
        # controller: The AccountManager class
        if self.errorOccured:
            self.errorL.destroy()
            self.errorOccured = False
        self.userWebsiteL.destroy()
        self.accountUsernameL.destroy()
        self.passwordE.delete(0, 'end')
        controller.show_frame(PasswordViewPage)


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
        self.websiteL = tk.Label(self, text = "Website")
        self.usernameL = tk.Label(self, text = "Username")
        self.passwordL = tk.Label(self, text = "Password")
        self.websiteL.grid(row=self.rowEntryStart, column=0)
        self.usernameL.grid(row=self.rowEntryStart+1, column=0)
        self.passwordL.grid(row=self.rowEntryStart+2 , column=0)

        self.websiteE = tk.Entry(self, width=35)
        self.usernameE = tk.Entry(self, width=35)
        self.passwordE = tk.Entry(self, width=35)
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
            self.errorL = tk.Label(self, text = "Text fields cannot be blank")
            self.errorL.grid(row=self.rowEntryStart+5, columnspan=2)
        else:
            if len(website.split()) > 1:
                websiteSplit = website.split()
                website = ""
                for split in websiteSplit:
                    website += split
            if len(username.split()) > 1:
                usernameSplit = username.split()
                username = ""
                for split in usernameSplit:
                    username += split

            with open(self.filename, "a") as f:
                f.write(website + '|.~' + username + '~.|' + encrypt(password) + '\n')
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
        controller.PasswordViewRefresh()
        controller.show_frame(HomePage)
    
def encrypt(string):
    encryptPass = ""
    for letter in string:
        if letter == ' ':
            encryptPass += ' '
        else:
            encryptPass += chr(ord(letter) + 7)
    return encryptPass

def decrypt(string):
    decryptPass = ""
    for letter in string:
        if letter == ' ':
            decryptPass += ' '
        else:
            decryptPass += chr(ord(letter) - 7)
    return decryptPass

def userToFilename(username):
    # username: A string that is the users username
    # Takes in the username and turns each letter into its ASCII value and concates to make filename
    filename = ""
    for i in username:
        filename += str(ord(i))
    filename += ".txt"
    return filename

def quickSort(array, low, high):
    if low < high:
        pivot = partition(array, low, high)
        quickSort(array, low, pivot-1)
        quickSort(array, pivot+1, high)

def partition(array, low, high):
    i = low-1
    pivot = array[high].lower()

    for j in range(low, high):
        if array[j].lower() <= pivot:
            i += 1
            temp = array[j]
            array[j] = array[i]
            array[i] = temp
    temp = array[high]
    array[high] = array[i+1]
    array[i+1] = temp
    return(i+1)

app = AccountManager()
app.mainloop()
