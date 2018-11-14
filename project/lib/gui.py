import tkinter.ttk
import json
import webbrowser
from tkinter import *
from tkinter import font
from PIL import ImageTk
from steam import SteamClient
from steam.enums import EResult
from steam.guard import SteamAuthenticator
from .guimethods import *
from .database import dataBase
from .colors import *
from .steamclient import clientData
from .api import *

#API key window class
class apiKeyWindow(Toplevel):
    #Initialize
    def __init__(self, parent, colorDic, conn, rootClassRef):
        #Declare class variables
        self.colorDic = colorDic
        self.conn = conn
        self.parent = parent
        self.rootClassRef = rootClassRef
        #Initialize window's frame
        Toplevel.__init__(self)
        #Everything below is created in order from top of application to the bottom
        #Window Title
        self.windowTitle = Label(self, text="Add API Key")
        self.windowTitle.configure(font=("Segoe UI", 12), bg=self.colorDic["windowTitleBackground"], fg=self.colorDic["windowTitleForeground"], width="350", pady=10)
        self.windowTitle.pack()
        #Entry background frame
        self.entryHolder = Frame(self, bg=self.colorDic["appBackground"])
        self.entryHolder.pack(padx=15, pady=15, anchor="w")
        #Guard logo image
        self.img = ImageTk.PhotoImage(file="images/gui/api.png")
        self.apiLogo = Label(self.entryHolder, bg=self.colorDic["appBackground"], image=self.img)
        self.apiLogo.pack(side="left", padx=20)
        #Entry and label background frame
        self.entryLabelHolder = Frame(self.entryHolder, bg=self.colorDic["appBackground"])
        self.entryLabelHolder.pack(side="left")
        #Entry and label
        self.apiLabel = Label(self.entryLabelHolder, text="API key:", bg=self.colorDic["appBackground"], fg=self.colorDic["infoLabelForeground"], font=("Segoe UI", 14))
        self.apiLabel.pack(anchor="nw")
        self.apiEntry = Entry(self.entryLabelHolder, width=35, font=("Segoe UI", 12))
        self.apiEntry.pack(pady=10, anchor="w")
        self.apiEntry.focus()
        #Url information text
        self.infoLabel = Label(self, text="Where do I get this?", font=("Arial", 14))
        self.font = font.Font(self.infoLabel, self.infoLabel.cget("font"))
        self.font.configure(underline=True)
        self.infoLabel.configure(font=self.font)
        self.infoLabel.configure(bg=self.colorDic["appBackground"], fg=self.colorDic["urlForeground"], cursor="hand2")
        self.infoLabel.pack(pady=10)
        self.infoLabel.bind("<Button-1>", self.url_click)
        #Button holding frame, submit button and cancel button
        self.buttonHolder = Frame(self, bg=self.colorDic["appBackground"])
        self.buttonHolder.pack(pady=15)
        self.submitButton = Button(self.buttonHolder, text="Submit Key", font=("Segoe UI", 12), relief="flat", cursor="hand2", command=self.submit_key)
        self.submitButton.configure(fg=self.colorDic["actionButtonForeground"], bg=self.colorDic["actionButtonBackground"])
        self.submitButton.pack(padx=30, ipady=10, ipadx=10, side="left")
        self.cancelButton = Button(self.buttonHolder, text="Cancel", font=("Segoe UI", 12), relief="flat", cursor="hand2", command=self.destroy)
        self.cancelButton.configure(fg=self.colorDic["cancelButtonForeground"], bg=self.colorDic["cancelButtonBackground"])
        self.cancelButton.pack(padx=30, ipady=10, ipadx=10, side="left")
    #Submit and check key method
    def submit_key(self):
        apiKey = self.apiEntry.get()
        self.apiController = api(apiKey)
        if self.apiController.check_api_key():
            self.conn.update_api_key(apiKey)
            self.rootClassRef.apiKey = apiKey
            self.rootClassRef.apiController = api(apiKey)
            self.destroy()
        else:
            self.rootClassRef.show_message(None, "error", "Invalid API Key Entered!")
    #Url click method
    def url_click(self, event):
        webbrowser.open("https://steamcommunity.com/dev/apikey")

#New account window class
class clientLoginWindow(Toplevel):
    #Initialize
    def __init__(self, parent, colorDic, conn, rootClassRef):
        #Declare class variables
        self.authWindow = None
        self.colorDic = colorDic
        self.conn = conn
        self.parent = parent
        self.rootClassRef = rootClassRef
        #Initialize window's frame
        Toplevel.__init__(self)
        #Window title
        self.windowTitle = Label(self, text="New Account")
        self.windowTitle.configure(font=("Segoe UI", 12), bg=self.colorDic["windowTitleBackground"], fg=self.colorDic["windowTitleForeground"], width="350", pady=10)
        self.windowTitle.pack()
        #Steam logo image
        self.img = ImageTk.PhotoImage(file="images/gui/steam_logo.png")
        self.steamLogo = Label(self, bg=self.colorDic["appBackground"], image=self.img)
        self.steamLogo.pack(anchor="w", padx=35, pady=25)
        #Login item's frame
        self.loginHolder = Frame(self, bg=self.colorDic["appBackground"])
        self.loginHolder.pack(anchor="w", padx=45, pady=25)
        self.labelHolder = Frame(self.loginHolder, bg=self.colorDic["appBackground"])
        self.labelHolder.pack(side="left")
        self.entryHolder = Frame(self.loginHolder, bg=self.colorDic["appBackground"])
        self.entryHolder.pack(side="left")
        #Account name and password text
        self.userNameLabel = Label(self.labelHolder, text="Account Name", bg=self.colorDic["appBackground"], fg=self.colorDic["infoLabelForeground"], font=("Segoe UI", 12))
        self.userNameLabel.pack(padx=5, pady=5, anchor="e")
        self.passwordLabel = Label(self.labelHolder, text="Password", bg=self.colorDic["appBackground"], fg=self.colorDic["infoLabelForeground"], font=("Segoe UI", 12))
        self.passwordLabel.pack(padx=5, pady=5, anchor="e")
        #Account name and password entry boxes
        self.userNameEntry = Entry(self.entryHolder, width=45)
        self.userNameEntry.pack(padx=5, pady=5)
        self.userNameEntry.focus()
        self.passwordEntry = Entry(self.entryHolder, width=45, show="*")
        self.passwordEntry.pack(padx=5, pady=5)
        #Button holding frame, login button and cancel button
        self.buttonHolder = Frame(self, bg=self.colorDic["appBackground"])
        self.buttonHolder.pack(pady=15)
        self.loginButton = Button(self.buttonHolder, text="Login to Steam", font=("Segoe UI", 12), relief="flat", cursor="hand2", command=self.login_account)
        self.loginButton.configure(fg=self.colorDic["actionButtonForeground"], bg=self.colorDic["actionButtonBackground"])
        self.loginButton.pack(padx=30, ipady=10, ipadx=10, side="left")
        self.cancelButton = Button(self.buttonHolder, text="Cancel", font=("Segoe UI", 12), relief="flat", cursor="hand2", command=self.destroy)
        self.cancelButton.configure(fg=self.colorDic["cancelButtonForeground"], bg=self.colorDic["cancelButtonBackground"])
        self.cancelButton.pack(padx=30, ipady=10, ipadx=10, side="left")
    #Login and add guard method
    def login_account(self):
        #Login to steam with provided credentials
        self.userObject = clientData(self.userNameEntry.get(), self.passwordEntry.get(), None, None)
        self.userObject.login()
        #If password is invalid
        if self.userObject.loginResult == EResult.InvalidPassword:
            #Show error stating password is incorrect
            self.rootClassRef.show_message(None, "error", "Your password is incorrect. Please try again.")
        else:
            #If email code is required
            if self.userObject.loginResult in (EResult.AccountLogonDenied, EResult.InvalidLoginAuthCode):
                self.authWindow = promptFor2FA(self.parent, self.colorDic, True, self.rootClassRef)
            #If 2FA code is required
            elif self.userObject.loginResult in (EResult.AccountLoginDeniedNeedTwoFactor, EResult.TwoFactorCodeMismatch):
                self.authWindow = promptFor2FA(self.parent, self.colorDic, False, self.rootClassRef)
            #If email or 2FA code was required
            if self.authWindow:
                #Start 2FA prompt window
                self.authWindow.geometry("400x250")
                self.authWindow.resizable(0,0)
                self.authWindow.configure(bg=self.colorDic["appBackground"])
                guiController(self.authWindow).center()
                self.authWindow.wait_window()
                #If auth code was set
                if self.authWindow.guardCode:
                    #If auth code was sent to email
                    if self.authWindow.isEmail:
                        self.userObject = clientData(self.userNameEntry.get(), self.passwordEntry.get(), self.authWindow.guardCode, None)
                    else:
                        #If auth code was sent to mobile
                        self.userObject = clientData(self.userNameEntry.get(), self.passwordEntry.get(), None, self.authWindow.guardCode)
                    self.userObject.login()
            #If login and code is correct
            if self.userObject.loginResult == EResult.OK:
                self.steamGuardController = SteamAuthenticator(medium=self.userObject.client)
                if self.steamGuardController.status()['steamguard_scheme'] != 2:
                    #If account has a phone number
                    if self.steamGuardController.has_phone_number():
                        #Add steam guard
                        self.steamGuardController.add()
                        #Start 2FA prompt window to get phone confirmation
                        self.authWindow = promptFor2FA(self.parent, self.colorDic, False, self.rootClassRef)
                        self.authWindow.geometry("400x250")
                        self.authWindow.resizable(0,0)
                        self.authWindow.configure(bg=self.colorDic["appBackground"])
                        guiController(self.authWindow).center()
                        self.authWindow.title("Steam Guardian - Mobile")
                        self.authWindow.windowTitle.configure(text="Enter Text Sent to Phone")
                        self.authWindow.wait_window()
                        #If phone code is set
                        if self.authWindow.guardCode:
                            try:
                                self.steamGuardController.finalize(self.authWindow.guardCode)
                            except:
                                #If phone code is incorrect show an error
                                self.rootClassRef.show_message(None, "error", "Couldn't confirm your phone. Code is incorrect!")
                            else:
                                #Update data and gui
                                self.conn.create_user(str(json.dumps(self.steamGuardController.secrets)), str(self.userObject.client.user.steam_id), self.userNameEntry.get(), self.passwordEntry.get())
                                self.rootClassRef.update_guard()
                        #We destroy our window here because Steam loves to rate limit if you retry too fast
                        self.destroy()
                    else:
                        #If account doesn't have phone number show an error
                        self.rootClassRef.show_message(None, "error", "Your account is missing a phone number to confirm.\nPlease add one and try again!")
                        webbrowser.open("https://store.steampowered.com/phone/manage")
                else:
                    #If account already has 2FA (email is fine) show an error
                    self.rootClassRef.show_message(None, "error", "Your account already has Steam Guard Mobile.\nPlease disable it and try again.")
            else:
                #If steam guard code was incorrect.
                self.rootClassRef.show_message(None, "error", "Login or code was incorrect.")

#Switch account window class
class clientSwitchWindow(Toplevel):
    #Initialize
    def __init__(self, parent, colorDic, conn, rootClassRef):
        #Declare class variables
        self.colorDic = colorDic
        self.conn = conn
        self.frameList = []
        self.labelList = []
        self.parent = parent
        self.rootClassRef = rootClassRef
        #Initialize window's frame
        Toplevel.__init__(self)
        self.guiControl = guiController(self, colorDic)
        #Window title
        self.windowTitle = Label(self, text="Switch Accounts")
        self.windowTitle.configure(font=("Segoe UI", 12), bg=self.colorDic["windowTitleBackground"], fg=self.colorDic["windowTitleForeground"], width="350", pady=10)
        self.windowTitle.pack()
        #Canvas so we can have a scrollable frame
        self.canvas = Canvas(self, bg=self.colorDic["specialButtonBackground"], border=0, highlightthickness=0)
        self.canvas.pack(side="left", anchor="n")
        self.scrollbar = Scrollbar(self, command=self.canvas.yview)
        self.scrollbar.pack(side="left", fill='y')
        self.canvas.configure(yscrollcommand = self.scrollbar.set)
        self.canvas.bind('<Configure>', self.guiControl.on_configure)
        self.frame = Frame(self.canvas, bg=self.colorDic["hrColor"])
        self.frame.pack()
        self.canvas.create_window((0,0), window=self.frame, anchor='nw')
        #For every secret found place a label with the account name
        for counter, secretText in enumerate(self.conn.get_secrets()):
            self.frameList.append(Frame(self.frame, bg=self.colorDic["specialButtonBackground"], width="400", height="79", cursor="hand2"))
            self.labelList.append(Label(self.frameList[counter], text=json.loads(secretText[0])["account_name"], font=("Segoe UI", 15), bg=self.colorDic["specialButtonBackground"], fg=self.colorDic["specialButtonForeground"], cursor="hand2"))
            self.labelList[counter].pack(side="left", pady="15", padx="20")
            self.frameList[counter].pack()
            self.frameList[counter].pack_propagate(0)
            #Just a padding trick
            if counter % 2 == 0:
                self.frameList[counter].pack(pady="1")
            else:
                self.frameList[counter].pack()
            #We need to be able to hover and leave these "buttons"!
            self.frameList[counter].bind("<Enter>", self.guiControl.special_button_hover)
            self.frameList[counter].bind("<Leave>", self.guiControl.special_button_leave)
            self.frameList[counter].secret = secretText[0]
            self.labelList[counter].secret = secretText[0]
            self.frameList[counter].bind("<Button-1>", self.update_active_user)
            self.labelList[counter].bind("<Button-1>", self.update_active_user)
    #Update active secret method
    def update_active_user(self, event):
        self.conn.update_active_user(event.widget.secret)
        self.destroy()
        self.rootClassRef.update_guard()

#Confirmations window class
class confirmationsWindow(Toplevel):
    def __init__(self, parent, colorDic, rootClassRef):
        #Class variables
        self.colorDic = colorDic
        self.parent = parent
        self.rootClassRef = rootClassRef
        #Initialize window's frame
        Toplevel.__init__(self)
        #Window title
        self.windowTitle = Label(self, text="Your Trade With: Somebody_37")
        self.windowTitle.configure(font=("Segoe UI", 12), bg=self.colorDic["windowTitleBackground"], fg=self.colorDic["windowTitleForeground"], pady=10)
        self.windowTitle.pack(fill="x")

        self.allInfo = Frame(self, bg=self.colorDic["appBackground"])
        self.allInfo.pack(anchor="nw")

        self.tradeInfo = Frame(self.allInfo, bg=self.colorDic["appBackground"])
        self.tradeInfo.pack(padx=(20,0), pady=20, side="left")
        self.tradeTotal = Label(self.tradeInfo, text="Your Total: $410.73")
        self.tradeTotal.configure(font=("Segoe UI", 14), bg=self.colorDic["appBackground"], fg=self.colorDic["infoLabelForeground"], pady=10)
        self.tradeTotal.pack()
        self.tradeBox = Frame(self.tradeInfo, bg=self.colorDic["tradeFrameBackground"], highlightbackground=self.colorDic["tradeFrameHighlight"], highlightthickness=1)
        self.tradeBox.pack()
        self.trade = [["knife.png", "#8650ac", "$166.77"], ["ak47.png", "#d2d2d2", "$28.22"], ["fiveseven.png", "#d2d2d2", "$0.49"], ["p250.png", "#cf6a32", "$6.16"], ["famas.png", "#d2d2d2", "$0.05"], ["knife2.png", "#8650ac", "$208.95"], ["czauto.png", "#d2d2d2", "$0.09"], ["knife.png", "#8650ac", "$166.77"], ["ak47.png", "#d2d2d2", "$28.22"], ["fiveseven.png", "#d2d2d2", "$0.49"], ["p250.png", "#cf6a32", "$6.16"], ["famas.png", "#d2d2d2", "$0.05"], ["knife2.png", "#8650ac", "$208.95"], ["czauto.png", "#d2d2d2", "$0.09"]]
        self.pages = [self.trade[i:i+12] for i in range(0, len(self.trade), 12)]
        self.page_Counter = 1
        self.items = self.load_inventory(self.tradeBox, self.pages[0])

        self.backwardFrame = Frame(self.tradeInfo,  bg=self.colorDic["appBackground"])
        self.backwardFrame.pack(side="left", pady=10, padx=10)
        self.backwardimg = ImageTk.PhotoImage(file="images/gui/backward.png")
        self.backward = Label(self.backwardFrame, bg=self.colorDic["appBackground"], image=self.backwardimg, cursor="hand2")
        self.backward.pack()
        self.backward.bind("<Button-1>", lambda event: self.load_own_page(event, "backward"))
        self.pageFrame = Frame(self.tradeInfo, bg=self.colorDic["appBackground"])
        self.pageFrame.pack_propagate(0)
        self.pageFrame.pack(side="left", pady=10, fill="both", expand=1)
        self.pageCounter = Label(self.pageFrame, text="Page 1 of 1", font=("Segoe UI", 11), bg=self.colorDic["appBackground"], fg=self.colorDic["infoLabelForeground"])
        self.pageCounter.pack()
        self.forwardFrame = Frame(self.tradeInfo,  bg=self.colorDic["appBackground"])
        self.forwardFrame.pack(side="right", padx=10)
        self.forwardimg = ImageTk.PhotoImage(file="images/gui/forward.png")
        self.forward = Label(self.forwardFrame, bg=self.colorDic["appBackground"], image=self.forwardimg, cursor="hand2")
        self.forward.pack()
        self.forward.bind("<Button-1>", lambda event: self.load_own_page(event, "forward"))

        self.tradeInfo1 = Frame(self.allInfo, bg=self.colorDic["appBackground"])
        self.tradeInfo1.pack(padx=(20,0), pady=20, side="left")
        self.tradeTotal1 = Label(self.tradeInfo1, text="Their Total: $392.76")
        self.tradeTotal1.configure(font=("Segoe UI", 14), bg=self.colorDic["appBackground"], fg=self.colorDic["infoLabelForeground"], pady=10)
        self.tradeTotal1.pack()
        self.tradeBox1 = Frame(self.tradeInfo1, bg=self.colorDic["tradeFrameBackground"], highlightbackground=self.colorDic["tradeFrameHighlight"], highlightthickness=1)
        self.tradeBox1.pack()
        self.trade1 = [["knife3.png", "#8650ac", "$392.76"]]
        self.pages1 = [self.trade1[i:i+12] for i in range(0, len(self.trade1), 12)]
        self.page_Counter1 = 1
        self.items1 = self.load_inventory(self.tradeBox1, self.pages1[0])

        self.backwardFrame1 = Frame(self.tradeInfo1,  bg=self.colorDic["appBackground"])
        self.backwardFrame1.pack(side="left", pady=10, padx=10)
        self.backwardimg1 = ImageTk.PhotoImage(file="images/gui/backward.png")
        self.backward1 = Label(self.backwardFrame1, bg=self.colorDic["appBackground"], image=self.backwardimg1, cursor="hand2")
        self.backward1.pack()
        self.pageFrame1 = Frame(self.tradeInfo1, bg=self.colorDic["appBackground"])
        self.pageFrame1.pack_propagate(0)
        self.pageFrame1.pack(side="left", pady=10, fill="both", expand=1)
        self.pageCounter1 = Label(self.pageFrame1, text="Page 1 of 1", font=("Segoe UI", 11), bg=self.colorDic["appBackground"], fg=self.colorDic["infoLabelForeground"])
        self.pageCounter1.pack()
        self.forwardFrame1 = Frame(self.tradeInfo1,  bg=self.colorDic["appBackground"])
        self.forwardFrame1.pack(side="right", padx=10)
        self.forwardimg1 = ImageTk.PhotoImage(file="images/gui/forward.png")
        self.forward1 = Label(self.forwardFrame1, bg=self.colorDic["appBackground"], image=self.forwardimg1, cursor="hand2")
        self.forward1.pack()

        self.buttonHolder = Frame(self, bg=self.colorDic["appBackground"])
        self.buttonHolder.pack()
        self.submitButton = Button(self.buttonHolder, text="Confirm Trade", font=("Segoe UI", 12), relief="flat", cursor="hand2", width=15)
        self.submitButton.configure(fg=self.colorDic["actionButtonForeground"], bg=self.colorDic["actionButtonBackground"])
        self.submitButton.pack(ipady=10, ipadx=10, side="left")
        self.cancelButton = Button(self.buttonHolder, text="Cancel Trade", font=("Segoe UI", 12), relief="flat", cursor="hand2", width=15)
        self.cancelButton.configure(fg=self.colorDic["cancelButtonForeground"], bg=self.colorDic["cancelButtonBackground"])
        self.cancelButton.pack(padx=(20,0), ipady=10, ipadx=10, side="left")

    def load_own_page(self, event, direction):
        if direction == "forward":
            if self.page_Counter < len(self.pages):
                self.forget_own_widgets()
                self.page_Counter+=1
                self.items = self.load_inventory(self.tradeBox, self.pages[self.page_Counter-1])
        elif direction == "backward":
            if self.page_Counter > 1:
                self.forget_own_widgets()
                self.page_Counter-=1
                self.items = self.load_inventory(self.tradeBox, self.pages[self.page_Counter-1])

    def load_inventory(self, frame, inventory):
        items = {"framelines": [], "frames": [], "images": [], "labels": []}
        total = len(inventory)
        inventory = [inventory[i:i+4] for i in range(0, len(inventory), 4)]

        for invList in inventory:
            items["framelines"].append(Frame(frame, bg=self.colorDic["tradeFrameBackground"]))
            items["framelines"][-1].pack(anchor="w")
            for counter, item in enumerate(invList, start=1):
                items["frames"].append(Frame(items["framelines"][-1], bg=self.colorDic["tradeItemBackground"], highlightbackground=item[1], highlightthickness=1))
                if counter % 4 == 0:
                    items["frames"][-1].pack(padx=(10,10), pady=(10,0), side="left")
                else:
                    items["frames"][-1].pack(padx=(10,0), pady=(10,0), side="left")
                items["images"].append(ImageTk.PhotoImage(file="images/cache/" + item[0]))
                items["labels"].append(Label(items["frames"][-1], bg=self.colorDic["tradeItemBackground"], image=items["images"][-1]))
                items["labels"][-1].grid(row=0, column=0)
                items["labels"].append(Label(items["frames"][-1], bg=self.colorDic["tradeItemPriceBackground"], fg=self.colorDic["tradeItemPriceForeground"], text=item[2]))
                items["labels"][-1].grid(row=0, column=0, sticky="sew")

        if total < 12:
            rangeList = list(range(total+1, 13))
            newList = []
            tempList = []
            for i in rangeList:
                if i % 4 == 0:
                    tempList.append(i)
                    newList.append(tempList)
                    tempList = []
                else:
                    tempList.append(i)
            for item in newList:
                for i in item:
                    items["frames"].append(Frame(items["framelines"][-1], bg=self.colorDic["tradeItemBackground"], width=102, height=102))
                    if i % 4 == 0:
                        items["frames"][-1].pack(padx=(10,10), pady=(10,0), side="left")
                    else:
                        items["frames"][-1].pack(padx=(10,0), pady=(10,0), side="left")
                    items["frames"][-1].pack_propagate(0)
                items["framelines"].append(Frame(frame, bg=self.colorDic["tradeFrameBackground"]))
                items["framelines"][-1].pack(anchor="w")
        items["framelines"].append(Frame(frame, bg=self.colorDic["tradeFrameBackground"]))
        items["framelines"][-1].pack(pady=(0,10), anchor="e")

        return items

    def forget_own_widgets(self):
        for label in self.items["framelines"]:
            label.pack_forget()

        self.items = None

    def forget_partner_widgets(self):
        for label in self.items1["framelines"]:
            label.pack_forget()

        self.items1 = None

#2FA prompt window class
class promptFor2FA(Toplevel):
    #Initialize
    def __init__(self, parent, colorDic, isEmail, rootClassRef):
        #Class variables
        self.colorDic = colorDic
        self.guardCode = None
        self.isEmail = isEmail
        self.parent = parent
        #Initialize window's frame
        Toplevel.__init__(self)
        #If code required is sent to email
        if self.isEmail:
            self.file="images/gui/steam_email.png"
            self.header = "Steam Guard Email"
            self.title("Steam Guardian - Email")
        else:
            #If code required is sent to mobile
            self.file="images/gui/steam_phone.png"
            self.header = "Steam Guard Mobile"
            self.title("Steam Guardian - 2FA")
        #Window title
        self.windowTitle = Label(self, text=self.header)
        self.windowTitle.configure(font=("Segoe UI", 12), bg=self.colorDic["windowTitleBackground"], fg=self.colorDic["windowTitleForeground"], width="350", pady=10)
        self.windowTitle.pack()
        #Entry background frame
        self.entryHolder = Frame(self, bg=self.colorDic["appBackground"])
        self.entryHolder.pack(padx=35, pady=25, anchor="w")
        #Guard logo image
        self.img = ImageTk.PhotoImage(file=self.file)
        self.authLogo = Label(self.entryHolder, bg=self.colorDic["appBackground"], image=self.img)
        self.authLogo.pack(side="left", padx=20)
        self.authEntry = Entry(self.entryHolder, width=6, font=("Segoe UI", 35))
        self.authEntry.pack(side="left")
        self.authEntry.focus()
        #Button background frame
        self.buttonHolder = Frame(self, bg=self.colorDic["appBackground"])
        self.buttonHolder.pack(pady=15)
        self.submitButton = Button(self.buttonHolder, text="Submit", font=("Segoe UI", 12), relief="flat", cursor="hand2", command=self.submitAuth)
        self.submitButton.configure(fg=self.colorDic["actionButtonForeground"], bg=self.colorDic["actionButtonBackground"])
        self.submitButton.pack(padx=30, ipady=10, ipadx=10, side="left")
        self.cancelButton = Button(self.buttonHolder, text="Cancel", font=("Segoe UI", 12), relief="flat", cursor="hand2", command=self.destroy)
        self.cancelButton.configure(fg=self.colorDic["cancelButtonForeground"], bg=self.colorDic["cancelButtonBackground"])
        self.cancelButton.pack(padx=30, ipady=10, ipadx=10, side="left")
    #Submit code method
    def submitAuth(self):
        allowed = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        #If code is 5 characters long and Alphanumeric
        if len(self.authEntry.get()) == 5 and [char for char in self.authEntry.get().upper() if char in allowed]:
            self.guardCode = self.authEntry.get()
            self.destroy()
        else:
            #If code is not 5 characters long and or Alphanumeric show an error
            self.rootClassRef.show_message(None, "error", "Something seems wrong about that Code.")
            self.destroy()

#Main window class
class mainWindow(Frame):
    #Initialize
    def __init__(self, parent, colorDic):
        #Declare class variables
        self.activeSecrets = None
        self.client = SteamClient()
        self.colorDic = colorDic
        self.conn = dataBase()
        self.apiKey = self.conn.get_api_key()
        self.apiController = api(self.apiKey)
        self.parent = parent
        self.guiControl = guiController(self.parent, self.colorDic)
        self.steamGuardController = None
        self.steamName = ""
        self.updateProgressBarID = None
        #Initialize window's frame
        Frame.__init__(self, self.parent)
        #Everything below is created in order from top of application to the bottom
        #Menu bar
        self.menuBar = Menu(self.parent, border=0)
        self.menuBar.config(bg=self.colorDic["menuBarBackground"], fg=self.colorDic["menuBarForeground"])
        self.accountMenu = Menu(self.menuBar, tearoff=0)
        #New account and Import account button
        self.accountMenu.add_command(label="New Steam Guard", command=self.new_account_window)
        self.accountMenu.add_command(label="Delete Steam Guard", command=self.delete_steam_guard)
        #Seperator makes it look fabulous
        self.accountMenu.add_separator()
        self.accountMenu.add_command(label="Import Steam Guard")
        self.menuBar.add_cascade(label="Guard", menu=self.accountMenu)
        self.accountMenu.config(bg=self.colorDic["menuBarBackground"], fg=self.colorDic["menuBarForeground"])
        self.editMenu = Menu(self.menuBar, tearoff=0)
        #Security preferences and color scheme button
        self.editMenu.add_command(label="Security Preferences")
        self.editMenu.add_command(label="Color Scheme")
        self.menuBar.add_cascade(label="Edit", menu=self.editMenu)
        self.editMenu.config(bg=self.colorDic["menuBarBackground"], fg=self.colorDic["menuBarForeground"])
        #Window Title
        self.windowTitle = Label(self.parent, text="Steam Guard")
        self.windowTitle.configure(font=("Segoe UI", 12), bg=self.colorDic["windowTitleBackground"], fg=self.colorDic["windowTitleForeground"], width="350", pady=10)
        self.windowTitle.pack()
        #Guard codes and Steam name frame
        self.guardCodeHolder = Frame(self.parent, bg=self.colorDic["guardCodeBackground"])
        self.guardCodeHolder.pack()
        #Generated Steam Guard text
        self.guardLabel = Label(self.guardCodeHolder, text="...")
        self.guardLabel.configure(font=("Segoe UI", 30), bg=self.colorDic["guardCodeBackground"], fg=self.colorDic["guardCodeForeground"], width="350", pady=15)
        self.guardLabel.pack()
        #Styling for progress bar
        self.barStyle = ttk.Style()
        self.barStyle.theme_use('alt')
        self.barStyle.configure("blue.Horizontal.TProgressbar", troughrelief="flat", troughcolor=self.colorDic["progressBarBackground"], background=self.colorDic["progressBarForeground"], relief="flat")
        #Progress bar
        self.progressBar = ttk.Progressbar(self.guardCodeHolder, style="blue.Horizontal.TProgressbar", orient ="horizontal", length=250, mode="determinate")
        self.progressBar.pack()
        self.progressBar["maximum"] = 58
        #Steam name text
        self.steamNameLabel = Label(self.guardCodeHolder, text=self.steamName)
        self.steamNameLabel.configure(font=("Segoe UI", 10), bg=self.colorDic["guardCodeBackground"], fg=self.colorDic["steamNameForeground"], width="350", pady=5)
        self.steamNameLabel.pack()
        #Special buttons frame
        self.specialButtonsHolder = Frame(self.parent, bg=self.colorDic["specialButtonBackground"])
        self.specialButtonsHolder.pack(side="top", expand=True, fill="y")
        self.specialButtonsBackground = Frame(self.specialButtonsHolder, bg=self.colorDic["hrColor"], width="350", height="241")
        self.specialButtonsBackground.pack()
        self.specialButtonsBackground.pack_propagate(0)
        #"Confirmations" button frame
        self.confirmationHolder = Frame(self.specialButtonsBackground, bg=self.colorDic["specialButtonBackground"], width="350", height="79", cursor="hand2")
        self.confirmationHolder.pack(pady="1")
        self.confirmationLabel = Label(self.confirmationHolder, text="Confirmations", font=("Segoe UI", 15), bg=self.colorDic["specialButtonBackground"], fg=self.colorDic["specialButtonForeground"], cursor="hand2")
        self.confirmationLabel.pack(side="left", pady="15", padx="20")
        self.confirmationHolder.pack_propagate(0)
        self.confirmationHolder.bind("<Enter>", self.guiControl.special_button_hover)
        self.confirmationHolder.bind("<Leave>", self.guiControl.special_button_leave)
        self.confirmationHolder.bind("<Button-1>", self.confirmations_window)
        self.confirmationLabel.bind("<Button-1>", self.confirmations_window)
        #"Revocation" button frame
        self.revocationCodeHolder = Frame(self.specialButtonsBackground, bg=self.colorDic["specialButtonBackground"], width="350", height="79", cursor="hand2")
        self.revocationCodeLabel = Label(self.revocationCodeHolder, text="Revocation Code", font=("Segoe UI", 15), bg=self.colorDic["specialButtonBackground"], fg=self.colorDic["specialButtonForeground"], cursor="hand2")
        self.revocationCodeLabel.pack(side="left", pady="15", padx="20")
        self.revocationCodeHolder.pack()
        self.revocationCodeHolder.pack_propagate(0)
        self.revocationCodeHolder.bind("<Enter>", self.guiControl.special_button_hover)
        self.revocationCodeHolder.bind("<Leave>", self.guiControl.special_button_leave)
        self.revocationCodeHolder.bind("<Button-1>", self.revocation_code_window)
        self.revocationCodeLabel.bind("<Button-1>", self.revocation_code_window)
        #"Switch Account" button frame
        self.switchAccountHolder = Frame(self.specialButtonsBackground, bg=self.colorDic["specialButtonBackground"], width="350", height="79", cursor="hand2")
        self.switchAccountLabel = Label(self.switchAccountHolder, text="Switch Accounts", font=("Segoe UI", 15), bg=self.colorDic["specialButtonBackground"], fg=self.colorDic["specialButtonForeground"], cursor="hand2")
        self.switchAccountLabel.pack(side="left", pady="15", padx="20")
        self.switchAccountHolder.pack(pady="1")
        self.switchAccountHolder.pack_propagate(0)
        self.switchAccountHolder.bind("<Enter>", self.guiControl.special_button_hover)
        self.switchAccountHolder.bind("<Leave>", self.guiControl.special_button_leave)
        self.switchAccountHolder.bind("<Button-1>", self.switch_account_window)
        self.switchAccountLabel.bind("<Button-1>", self.switch_account_window)
        #Copy button frame
        self.buttonHolder = Frame(self.parent, bg=self.colorDic["appBackground"])
        self.copyCodeButton = Button(self.buttonHolder, text="Copy Code", command=lambda: self.guiControl.copy_label_text(self.guardLabel), font=("Segoe UI", 12), relief="flat", cursor="hand2")
        self.copyCodeButton.configure(fg=self.colorDic["actionButtonForeground"], bg=self.colorDic["actionButtonBackground"])
        self.copyCodeButton.pack(padx=30,pady=20, ipady=10, ipadx=10)
        self.buttonHolder.pack(side="bottom")
        #Set our window properties
        self.parent.geometry("350x500")
        self.parent.resizable(0,0)
        self.parent.configure(bg=self.colorDic["appBackground"])
        self.parent.title("Steam Guardian")
        self.parent.config(menu=self.menuBar)
        self.guiControl.center()

        if self.conn.has_active_user():
            self.update_guard()
    #API key window method
    def api_key_window(self):
        #Start API key window
        self.clientLogin = apiKeyWindow(self.parent, self.colorDic, self.conn, self)
        self.clientLogin.geometry("500x300")
        self.clientLogin.resizable(0,0)
        self.clientLogin.configure(bg=self.colorDic["appBackground"])
        self.clientLogin.title("Steam Guardian - Api Key")
        guiController(self.clientLogin).center()
    #Check for active account method
    def check_active_secrets(self):
        if self.activeSecrets:
            return True
        else:
            self.show_message(None, "error", "No active account! This is required to do this action.\nGo to 'Guard -> New Steam Guard' to add one.")
    #Check for active api key
    def check_active_api(self):
        if self.check_active_secrets():
            if self.apiKey:
                if self.apiController.check_api_key():
                    return True
                else:
                    self.show_message(None, "error", "API key is invalid! Taking you to the\nAPI window to update your key.")
                    self.api_key_window()
            else:
                self.show_message(None, "error", "No API key is set! This is required to do this action.\nTaking you to the API window to add a key.")
                self.api_key_window()
    #Confirmations window method
    def confirmations_window(self, event):
        if self.check_active_api():
            #Everything's good, get our confirmations
            self.confirmationWindow = confirmationsWindow(self.parent, self.colorDic, self)
            self.confirmationWindow.geometry("980x611")
            self.confirmationWindow.resizable(0,0)
            self.confirmationWindow.configure(bg=self.colorDic["appBackground"])
            self.confirmationWindow.title("Steam Guardian - Confirmations")
            guiController(self.confirmationWindow).center()
    #Delete Steam Guard method
    def delete_steam_guard(self):
        #If active secrets set
        if self.check_active_secrets():
            #Ask user if it's okay to remove Steam Guard
            userApproves = self.show_message(None, "warning", "This will remove steam guard from your {} account.\nYou cannot undo this action, would yo like to continue?".format(self.steamName), True)
            #If user approves
            if userApproves:
                self.conn.remove_guard(self.guardLabel["text"], self.activeSecrets)
                #Reset Steam Guard in GUI
                self.steamName = ''
                self.activeSecrets = None
                self.steamGuardController = None
                self.guardLabel.config({"text" : "..."})
                self.progressBar["value"] = 0
                self.steamName = ''
                self.steamNameLabel.configure(text=self.steamName)
                self.barStyle.configure("blue.Horizontal.TProgressbar", troughcolor=self.colorDic["progressBarBackground"], background=self.colorDic["progressBarForeground"])
                self.guardLabel.configure(fg=self.colorDic["guardCodeForeground"], bg=self.colorDic["guardCodeBackground"])
                self.steamNameLabel.config(fg=self.colorDic["steamNameForeground"], bg=self.colorDic["guardCodeBackground"])
                self.guardCodeHolder.config(bg=self.colorDic["guardCodeBackground"])
                #Tell user we're done
                self.show_message(None, "success", "Steam Guard has been successfully removed.")
        else:
            #No active secrets set
            self.show_message(None, "error", "No account to delete!")
    #New account window method
    def new_account_window(self):
        #Start login window
        self.clientLogin = clientLoginWindow(self.parent, self.colorDic, self.conn, self)
        self.clientLogin.geometry("500x350")
        self.clientLogin.resizable(0,0)
        self.clientLogin.configure(bg=self.colorDic["appBackground"])
        self.clientLogin.title("Steam Guardian - New Account")
        guiController(self.clientLogin).center()
    #Revocation code window method
    def revocation_code_window(self, event):
        if self.check_active_secrets():
            #Start revocation code window
            self.revocationCode = revocationCodeWindow(self.parent, self.colorDic, self)
            self.revocationCode.geometry("350x300")
            self.revocationCode.resizable(0,0)
            self.revocationCode.configure(bg=self.colorDic["appBackground"])
            self.revocationCode.title("Steam Guardian - Revocation Code")
            guiController(self.revocationCode).center()
    #Message window method
    def show_message(self, event, messageType, text, yesNo = False):
        #Start message window
        self.messageWindow = showMessage(self.parent, self.colorDic, messageType, text, yesNo)
        self.messageWindow.title("Steam Guardian - {}".format(messageType))
        guiController(self.messageWindow).center()
        self.messageWindow.wait_window()
        return self.messageWindow.response
    #Switch account window method
    def switch_account_window(self, event):
        #If there's more than 1 user to select
        if self.conn.count_users() > 1:
            #Start switch account window
            self.switchGui = clientSwitchWindow(self.parent, self.colorDic, self.conn, self)
            self.switchGui.geometry("400x450")
            self.switchGui.resizable(0,0)
            self.switchGui.configure(bg=self.colorDic["appBackground"])
            self.switchGui.title("Steam Guardian - Accounts")
            guiController(self.switchGui).center()
        else:
            #If no accounts were found to switch to show an error
            self.rootClassRef.show_message(None, "warning", "You have no accounts to switch to.\n'Click Account-> New Account' to add a new one.")
    #Update secrets and reset progress bar method
    def update_guard(self):
        #Update active guard secrets, Steam name and reset our progress bar
        self.activeSecrets = json.loads(self.conn.get_active_secrets())
        self.apiKey = self.conn.get_api_key()
        self.apiController = api(self.apiKey)
        self.steamGuardController = SteamAuthenticator(secrets=self.activeSecrets, medium=self.client)
        self.steamName = self.activeSecrets["account_name"]
        self.steamNameLabel.configure(text=self.steamName)
        if self.progressBar["value"] <= 18:
            self.barStyle.configure("blue.Horizontal.TProgressbar", troughcolor=self.colorDic["progressBarBackground"], background=self.colorDic["progressBarForeground"])
            self.guardLabel.configure(fg=self.colorDic["guardCodeForeground"], bg=self.colorDic["guardCodeBackground"])
            self.steamNameLabel.config(fg=self.colorDic["steamNameForeground"], bg=self.colorDic["guardCodeBackground"])
            self.guardCodeHolder.config(bg=self.colorDic["guardCodeBackground"])
        #Cancel wait for updating progress bar. This way we don't call the same function twice doubling our speed.
        if self.updateProgressBarID:
            self.parent.after_cancel(self.updateProgressBarID)
            self.progressBar["value"] = 0
        self.update_progress_bar()
    #Progress bar timer and color changing method
    def update_progress_bar(self):
        #If our Steam guard controller object is set
        if self.steamGuardController:
            #Update progress bar and reset when value is 0. Set background to "warn" color when low on time or under 18
            if self.progressBar["value"] == 0:
                self.guardLabel.config({"text" : str(self.steamGuardController.get_code(timestamp=self.steamGuardController.get_time()))})
                self.progressBar["value"] = 58
                self.barStyle.configure("blue.Horizontal.TProgressbar", troughcolor=self.colorDic["progressBarBackground"], background=self.colorDic["progressBarForeground"])
                self.guardLabel.configure(fg=self.colorDic["guardCodeForeground"], bg=self.colorDic["guardCodeBackground"])
                self.steamNameLabel.config(fg=self.colorDic["steamNameForeground"], bg=self.colorDic["guardCodeBackground"])
                self.guardCodeHolder.config(bg=self.colorDic["guardCodeBackground"])
            elif self.progressBar["value"] <= 18:
                self.barStyle.configure("blue.Horizontal.TProgressbar", troughcolor=self.colorDic["progressBarBackgroundWarn"], background=self.colorDic["progressBarForegroundWarn"])
                self.guardLabel.configure(fg=self.colorDic["guardCodeForeground"], bg=self.colorDic["guardCodeBackgroundWarn"])
                self.steamNameLabel.config(fg=self.colorDic["steamNameForegroundWarn"], bg=self.colorDic["guardCodeBackgroundWarn"])
                self.guardCodeHolder.config(bg=self.colorDic["guardCodeBackgroundWarn"])
            self.progressBar["value"] = self.progressBar["value"]-1
            self.updateProgressBarID = self.parent.after(500, self.update_progress_bar)

#Revocation window class
class revocationCodeWindow(Toplevel):
    #Initialize
    def __init__(self, parent, colorDic, rootClassRef):
        #Declare class variables
        self.colorDic = colorDic
        self.parent = parent
        #This breaks alphabetical order, but it has to come first to create our next variable
        self.rootClassRef = rootClassRef
        self.revocationCode = self.rootClassRef.activeSecrets["revocation_code"]
        #Initialize window's frame
        Toplevel.__init__(self)
        self.guiControl = guiController(self, self.colorDic)
        #Everything below is created in order from top of application to the bottom
        #Window Title
        self.windowTitle = Label(self, text="Revocation Code")
        self.windowTitle.configure(font=("Segoe UI", 12), bg=self.colorDic["windowTitleBackground"], fg=self.colorDic["windowTitleForeground"], width="350", pady=10)
        self.windowTitle.pack()
        #Revocation code background and text
        self.codeBackground = Frame(self, bg=self.colorDic["guardCodeBackground"])
        self.codeBackground.pack()
        self.codeLabel = Label(self.codeBackground, text=self.revocationCode, font=("Segoe UI", 30), bg=self.colorDic["guardCodeBackground"], fg=self.colorDic["guardCodeForeground"])
        self.codeLabel.configure(width="350")
        self.codeLabel.pack(pady=15)
        #Steam name text
        self.steamNameLabel = Label(self.codeBackground, text=self.rootClassRef.steamName)
        self.steamNameLabel.configure(font=("Segoe UI", 10), bg=self.colorDic["guardCodeBackground"], fg=self.colorDic["steamNameForeground"], width="350", pady=5)
        self.steamNameLabel.pack()
        #Url information text
        self.infoLabel = Label(self, text="What's This?", font=("Arial", 12))
        self.font = font.Font(self.infoLabel, self.infoLabel.cget("font"))
        self.font.configure(underline=True)
        self.infoLabel.configure(font=self.font)
        self.infoLabel.configure(bg=self.colorDic["appBackground"], fg=self.colorDic["urlForeground"], cursor="hand2")
        self.infoLabel.pack(pady=20)
        self.infoLabel.bind("<Button-1>", self.url_click)
        #Copy code button
        self.copyCodeButton = Button(self, text="Copy Code", command=lambda: self.guiControl.copy_label_text(self.codeLabel), font=("Segoe UI", 12), relief="flat", cursor="hand2")
        self.copyCodeButton.configure(fg=self.colorDic["actionButtonForeground"], bg=self.colorDic["actionButtonBackground"])
        self.copyCodeButton.pack(side="bottom", pady=20, ipady=10, ipadx=10)
    #Question url method
    def url_click(self, event):
        #Tell user to keep code safe and information about it
        self.rootClassRef.show_message(None, "dialogue", "Keep this code safe. Never share it with anybody for any reason.\n\nThe revocation code is used by Steam to remove your Steam Guard\nin the event that you lose your phone number.")

#Message window class
class showMessage(Toplevel):
    #Initialize
    def __init__(self, parent, colorDic, messageType, text, yesNo = False):
        #Declare class variables
        self.colorDic = colorDic
        self.messageLines = []
        self.messageType = messageType
        self.parent = parent
        self.response = False
        self.text = text
        #Initialize window's frame
        Toplevel.__init__(self)
        #Because setting our background elsewhere every time is a pain
        self.configure(bg=self.colorDic["appBackground"])
        #Message background frame
        self.messageContainer = Frame(self, bg=self.colorDic["appBackground"])
        self.messageContainer.pack(pady=20)
        #Message image icon
        self.img = ImageTk.PhotoImage(file="images/gui/messagebox/{}.png".format(self.messageType))
        self.imgLogo = Label(self.messageContainer, bg=self.colorDic["appBackground"], image=self.img)
        self.imgLogo.pack(side="left", pady=20, padx=10)
        #Add each line in the message as a label. This way we can align our text to the left.
        #Probobaly better way to do this, but a Text widget is difficult to calculate its width to the length of the text
        for count, messageLine in enumerate(list(self.text.split("\n"))):
            self.messageLines.append(Label(self.messageContainer, text=messageLine, bg=self.colorDic["appBackground"], fg=self.colorDic["infoLabelForeground"]))
            self.messageLines[count].configure(font=("Segoe UI", 14))
            self.messageLines[count].pack(anchor="w", padx=10)
        #Button holder
        self.buttonHolder = Frame(self, bg=self.colorDic["appBackground"])
        self.buttonHolder.pack(pady=10)
        #If dialogue is a question create 'yes' and 'no' buttons.
        if yesNo:
            self.yesButton = Button(self.buttonHolder, text="Yes", command=self.update_response, font=("Segoe UI", 12), relief="flat", cursor="hand2")
            self.yesButton.configure(fg=self.colorDic["actionButtonForeground"], bg=self.colorDic["actionButtonBackground"])
            self.yesButton.pack(side="left", padx=20, ipady=10, ipadx=30)
            self.noButton = Button(self.buttonHolder, text="No", command=self.destroy, font=("Segoe UI", 12), relief="flat", cursor="hand2")
            self.noButton.configure(fg=self.colorDic["cancelButtonForeground"], bg=self.colorDic["cancelButtonBackground"])
            self.noButton.pack(side="left", padx=20, ipady=10, ipadx=30)
        else:
            #Otherwise just a simple confirm button will do
            self.confirmButton = Button(self.buttonHolder, text="Okay", command=self.destroy, font=("Segoe UI", 12), relief="flat", cursor="hand2")
            self.confirmButton.configure(fg=self.colorDic["actionButtonForeground"], bg=self.colorDic["actionButtonBackground"])
            self.confirmButton.pack(padx=20, ipady=10, ipadx=30)
        #Disable resizing after averything has the chance to adjust the window size
        self.resizable(0,0)
    #User response is set to False by default (No)
    #Updage response method (change response to True (Yes))
    def update_response(self):
        self.response = True
        self.destroy()
