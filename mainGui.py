from tkinter import *
import boto3
from boto3.dynamodb.conditions import Key
import pygame, pygame.font, pygame.event, pygame.draw
from pygame.locals import *
import time


class attendant():

    def __init__(self):
        # connect to dynamodb
        self.ddb = boto3.resource('dynamodb', region_name='us-east-2')
        self.data = self.loadTable()

        # the length of what a valid uid will be
        self.validLength = 10

    # make the browser add data to the db
    def add(self, item):
        self.data.put_item(Item=item)

    # queries ddb to see if the userID exists
    def checkExists(self, uid):
        self.retrievedData = self.data.query(KeyConditionExpression=Key('participantID').eq(uid))

        if self.retrievedData['Count'] == 0:
            return False
        else:
            self.retrievedData = self.retrievedData['Items'][0]
            return True

    # verify the length of the entered uid
    def verifyUID(self, uid):
        if len(str(uid)) != self.validLength:
            return False
        else:
            return True

    # load the table in init and every time an action happens at the table
    def loadTable(self):
        data = self.ddb.Table('practiceAttendance')
        return data


# setting up gui
class GUI():

    def __init__(self, master):
        self.master = master
        # doesnt work on linux, need fix
        self.master.state("zoomed")
        self.initUI()

    def initUI(self):
        # background and icon
        self.master.title("CUhackit Check In System")
        self.master.configure(background="white")
        self.background = PhotoImage(file="bg.png")
        Label(self.master, image=self.background, bg="white").grid(row=0, columnspan=3)
        Label(self.master, bg="white").grid(rowspan=4, column=0)
        Label(self.master, bg="white").grid(rowspan=4, column=2)

        # Label
        self.labelTitle = Label(self.master, text="Check In System", bg="white", font="Ariel 30 bold")
        self.labelID = Label(self.master, text="Enter ID", font="Ariel 20 bold", bg="white")
        self.labelName = Label(self.master, text="Enter Name", font="Ariel 20 bold", bg="white")
        self.labelTechOut = Label(self.master, text="Enter Tech to be Checked Out", font="Ariel 20 bold", bg="white")
        self.labelTechIn = Label(self.master, text="Enter the Number of the Tech", font="Ariel 20 bold", bg="white")
        self.labelTechList = Label(self.master, font="Ariel 20 bold", bg="white", anchor='w')

        # buttons for attendance, tech check, status check
        self.buttonAttend = Button(self.master, text="Check In", width=20, height=3,
                                   command=lambda: self.checkInMenu())
        self.buttonCName = Button(self.master, text="Chang Name", width=20, height=3,
                                  command=lambda: self.changeNameMenu())
        self.buttonTO = Button(self.master, text="Check Out Tech", width=20, height=3,
                               command=lambda: self.techOutMenu())
        self.buttonTI = Button(self.master, text="Return Tech", width=20, height=3,
                               command=lambda: self.techInMenu())
        self.buttonStatus = Button(self.master, text="Show Status", width=20, height=3,
                                   command=lambda: self.checkStatus())
        self.buttonMainMenu = Button(self.master, text="Back", width=20, height=3, command=lambda: self.mainMenu())
        self.buttonEnter = Button(self.master, text="Enter", width=20, height=3)

        # entry for inputs
        self.entryInput = Entry(self.master, font="Aerial 30")

        # resize widget based on window size
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_rowconfigure(3, weight=1)
        self.master.grid_rowconfigure(4, weight=1)
        self.master.grid_rowconfigure(5, weight=1)
        self.master.grid_rowconfigure(6, weight=1)

        # default grid setup
        self.labelTitle.grid(row=1, column=1)
        self.buttonAttend.grid(row=2, column=1)
        self.buttonCName.grid(row=3, column=1)
        self.buttonTO.grid(row=4, column=1)
        self.buttonTI.grid(row=5, column=1)
        self.buttonStatus.grid(row=6, column=1)

    def mainMenu(self):
        # change menu title
        self.labelTitle.configure(text="Check In System")
        # add main menu buttons
        self.buttonAttend.grid(row=2, column=1)
        self.buttonCName.grid(row=3, column=1)
        self.buttonTO.grid(row=4, column=1)
        self.buttonTI.grid(row=5, column=1)
        self.buttonStatus.grid(row=6, column=1)
        # remove other menu widgets
        self.labelID.grid_forget()
        self.entryInput.grid_forget()
        self.buttonMainMenu.grid_forget()
        self.buttonEnter.grid_forget()
        # set keys
        self.master.unbind('<Return>')
        # clear input if there was input in the entry when button pressed
        self.entryInput.delete(0, 'end')

    def checkInMenu(self):
        # change menu title
        self.labelTitle.configure(text="Check In and Check Out")
        # get rid of main menu widgets
        self.buttonAttend.grid_forget()
        self.buttonCName.grid_forget()
        self.buttonTO.grid_forget()
        self.buttonTI.grid_forget()
        self.buttonStatus.grid_forget()
        # add checkInMenu widgets
        self.buttonMainMenu.grid(row=5, column=0)
        self.buttonEnter.grid(row=3, column=2)
        self.entryInput.grid(row=3, column=1)
        self.labelID.grid(row=2, column=1)
        # make sure keyboard focus on the entry
        self.entryInput.focus_set()
        # set keys
        self.buttonEnter.configure(command=lambda: self.checkIn(event=None))
        self.master.bind('<Return>', self.checkIn)

    def changeNameMenu(self):
        # change menu title
        self.labelTitle.configure(text="Change Name")
        # get rid of main menu widgets
        self.buttonAttend.grid_forget()
        self.buttonCName.grid_forget()
        self.buttonTO.grid_forget()
        self.buttonTI.grid_forget()
        self.buttonStatus.grid_forget()
        # add checkInMenu widgets
        self.buttonMainMenu.grid(row=5, column=0)
        self.buttonEnter.grid(row=3, column=2)
        self.entryInput.grid(row=3, column=1)
        self.labelID.grid(row=2, column=1)
        # make sure keyboard focus on the entry
        self.entryInput.focus_set()
        # set keys
        self.buttonEnter.configure(command=lambda: self.changeName(event=None))
        self.master.bind('<Return>', self.changeName)

    def techOutMenu(self):
        # change menu title
        self.labelTitle.configure(text="Check Out Tech")
        # get rid of main menu widgets
        self.buttonAttend.grid_forget()
        self.buttonCName.grid_forget()
        self.buttonTO.grid_forget()
        self.buttonTI.grid_forget()
        self.buttonStatus.grid_forget()
        # add checkInMenu widgets
        self.buttonMainMenu.grid(row=5, column=0)
        self.buttonEnter.grid(row=3, column=2)
        self.entryInput.grid(row=3, column=1)
        self.labelID.grid(row=2, column=1)
        self.buttonEnter.configure(command=lambda: self.techOut(event=None))
        self.master.bind('<Return>', self.techOut)

    def techInMenu(self):
        # change menu title
        self.labelTitle.configure(text="Return Tech")
        # get rid of main menu widgets
        self.buttonAttend.grid_forget()
        self.buttonCName.grid_forget()
        self.buttonTO.grid_forget()
        self.buttonTI.grid_forget()
        self.buttonStatus.grid_forget()
        # add checkInMenu widgets
        self.buttonMainMenu.grid(row=5, column=0)
        self.buttonEnter.grid(row=3, column=2)
        self.entryInput.grid(row=3, column=1)
        self.labelID.grid(row=2, column=1)
        self.buttonEnter.configure(command=lambda: self.techIn(event=None))
        self.master.bind('<Return>', self.techIn)

    # main function for adding new user, checking in and out old users
    def checkIn(self, event):
        if a.verifyUID(self.entryInput.get()):
            self.uid = int(self.entryInput.get())
            if a.checkExists(self.uid):
                a.retrievedData['status'] *= -1
                a.add(a.retrievedData)
                self.greet(a.retrievedData, False)
            else:
                # setting the input entry to take name
                self.buttonEnter.configure(command=lambda: self.addNewUser(event=None))
                self.master.bind('<Return>', self.addNewUser)
                self.entryInput.delete(0, 'end')
                self.buttonMainMenu.configure(state="disabled")
                self.labelID.grid_forget()
                self.labelName.grid(row=2, column=1)
        else:
            self.popUp("Error: Invalid ID")

        self.entryInput.delete(0, 'end')

    # main function for changing name of an existing user
    def changeName(self, event):
        if a.verifyUID(self.entryInput.get()):
            self.uid = int(self.entryInput.get())
            if a.checkExists(self.uid):
                self.buttonEnter.configure(command=lambda: self.changeNameHelper(event=None))
                self.master.bind('<Return>', self.changeNameHelper)
                self.entryInput.delete(0, 'end')
                self.buttonMainMenu.configure(state="disabled")
                self.labelID.grid_forget()
                self.labelName.grid(row=2, column=1)
            else:
                self.popUp("Error: User does not exist")
        else:
            self.popUp("Error: Invalid ID")

        self.entryInput.delete(0, 'end')

    # main function for checking out tech
    def techOut(self, event):
        if a.verifyUID(self.entryInput.get()):
            self.uid = int(self.entryInput.get())
            if a.checkExists(self.uid):
                self.buttonEnter.configure(command=lambda: self.techOutHelper(event=None))
                self.master.bind('<Return>', self.techOutHelper)
                self.entryInput.delete(0, 'end')
                self.buttonMainMenu.configure(state="disabled")
                self.labelID.grid_forget()
                self.labelTechOut.grid(row=2, column=1)
            else:
                self.popUp("Error: User does not exist")
        else:
            self.popUp("Error: Invalid ID")

        self.entryInput.delete(0, 'end')

    # main function for returning tech
    def techIn(self, event):
        if a.verifyUID(self.entryInput.get()):
            self.uid = int(self.entryInput.get())
            if a.checkExists(self.uid):
                # formatting window with a list of tech already checked out
                count = 0
                techList = "Tech Already Checked Out: \n"
                currentTech = a.retrievedData['tech']
                for i in currentTech:
                    techList += "{msg: <15}".format(msg=str(count) + ". " + i)
                    count += 1
                self.buttonEnter.configure(command=lambda: self.techInHelper(event=None))
                self.master.bind('<Return>', self.techInHelper)
                self.entryInput.delete(0, 'end')
                self.buttonMainMenu.configure(state="disabled")
                self.labelTechList.configure(text=techList)
                self.labelID.grid_forget()
                self.labelTechList.grid(row=2, column=1)
                self.labelTechIn.grid(row=3, column=1)
                self.entryInput.grid(row=4, column=1)
                self.buttonEnter.grid(row=4, column=2)
            else:
                self.popUp("Error: User does not exist")
        else:
            self.popUp("Error: Invalid ID")

        self.entryInput.delete(0, 'end')

    # check status for all users in the database
    # used pack to format because it's easier for this situation
    # if you can, convert it to grid
    def checkStatus(self):
        # helper method for scroll bar
        def yview(*args):
            nameList.yview(*args)
            statusList.yview(*args)

        # helper method for scrolling outside the bar
        def onMouseWheel(event):
            # event 4 and 5 are for linux, not tested
            # else is for windows, tested
            if event.num == 4:
                delta = int(-1*(event.delta/120))
            elif event.num ==5:
                delta = int((event.delta / 120))
            else:
                delta = int(-1*(event.delta/120))
            nameList.yview("scroll", delta, "units")
            statusList.yview("scroll", delta, "units")
            # this prevents default bindings from firing, which
            # would end up scrolling the widget twice
            return "break"

        # initialize everything
        root = Toplevel()
        root.geometry("300x300")
        mainFrame = Frame(root)
        topFrame = Frame(mainFrame)
        bottomFrame = Frame(mainFrame)
        scroll = Scrollbar(root, orient="vertical", command=yview)
        labelName = Label(topFrame, text="Name", font="Ariel 10 bold")
        labelStatus = Label(topFrame, text="Status", font="Ariel 10 bold")
        nameList = Listbox(bottomFrame, yscrollcommand=scroll.set)
        statusList = Listbox(bottomFrame, yscrollcommand=scroll.set)
        # binding mouse wheel to scroll, button 4 and 5 is mouse wheel for linux
        nameList.bind("<MouseWheel>", onMouseWheel)
        statusList.bind("<MouseWheel>", onMouseWheel)
        nameList.bind("<Button-4>", onMouseWheel)
        statusList.bind("<Button-4>", onMouseWheel)
        nameList.bind("<Button-5>", onMouseWheel)
        statusList.bind("<Button-5>", onMouseWheel)
        response = a.data.scan()
        # format window
        scroll.pack(side="right", fill="y")
        mainFrame.pack(fill="both", expand=True)
        topFrame.pack(side="top", fill="both", expand=True)
        bottomFrame.pack(side="bottom", fill="both", expand=True)
        labelName.pack(side="left", fill="x", expand=True)
        labelStatus.pack(side="left", fill="x", expand=True)
        nameList.pack(side="left", fill="both", expand=True)
        statusList.pack(side="left", fill="both", expand=True)
        # adding to the two lists
        for i in response['Items']:
            nameList.insert(END, i['name'])
            if i['status'] == 1:
                statusList.insert(END, "IN")
            else:
                statusList.insert(END, "OUT")

    # helper function for checkIn, adds new user to database
    def addNewUser(self, event):
        # adding user to database
        tech = []
        username = self.entryInput.get()
        newUser = {'participantID': self.uid, 'name': username, 'status': 1, 'tech': tech}
        a.add(newUser)
        # format the window
        self.buttonEnter.configure(command=lambda: self.checkIn(event=None))
        self.master.bind('<Return>', self.checkIn)
        self.buttonMainMenu.configure(state="normal")
        self.labelName.grid_forget()
        self.labelID.grid(row=2, column=1)
        self.entryInput.delete(0, 'end')
        self.greet(newUser, True)

    # helper function for change name
    def changeNameHelper(self, event):
        username = self.entryInput.get()
        a.retrievedData['name'] = username
        a.add(a.retrievedData)
        # format the window
        self.buttonMainMenu.configure(state="normal")
        self.labelName.grid_forget()
        self.entryInput.delete(0, 'end')
        self.mainMenu()
        self.popUp("User name changed to " + username)

    # helper function for tech out
    def techOutHelper(self, event):
        tech = self.entryInput.get()
        a.retrievedData['tech'].append(tech)
        a.add(a.retrievedData)
        # format the window
        self.buttonMainMenu.configure(state="normal")
        self.labelTechOut.grid_forget()
        self.entryInput.delete(0, 'end')
        self.mainMenu()
        self.popUp(tech + " checked out")

    def techInHelper(self, event):
        # remove the tech from the list
        currentTech = a.retrievedData['tech']
        techNum = int(self.entryInput.get())
        tech = currentTech[techNum]
        del currentTech[techNum]
        a.retrievedData['tech'] = currentTech
        a.add(a.retrievedData)
        # format window
        self.buttonMainMenu.configure(state="normal")
        self.labelTechIn.grid_forget()
        self.labelTechList.grid_forget()
        self.entryInput.delete(0, 'end')
        self.mainMenu()
        self.popUp(tech + " returned")

    # greets when user check in and out, newUser is either true or false
    def greet(self, data, newUser):
        # format the welcome text
        string = ""
        if newUser:
            string = "Welcome, {}!".format(data['name'].split(' ')[0])
        else:
            if data['status'] == 1:
                string = "Welcome back, {}!".format(data['name'].split(' ')[0])
            else:
                string = "See you later, {}!".format(data['name'].split(' ')[0])
        # format popup window
        win = Toplevel()
        win.configure(background="green")
        win.attributes("-fullscreen", True)
        Label(win, text=string, font="Ariel 30 bold", fg='black', bg='green').grid(column=0, row=0)
        win.columnconfigure(0, weight=1)
        win.rowconfigure(0, weight=1)
        # show the pop up window
        win.deiconify()
        # the time until pop up window disappear, in ms
        win.after(1000 * 2, win.withdraw)

    # simple pop up window
    def popUp(self, text):
        win = Toplevel()
        win.configure(background="white")
        win.attributes("-fullscreen", True)
        Label(win, text=text, font="Ariel 30 bold", fg='black', bg='white').grid(column=0, row=0)
        win.columnconfigure(0, weight=1)
        win.rowconfigure(0, weight=1)
        # show the pop up window
        win.deiconify()
        # the time until pop up window disappear, in ms
        win.after(1000 * 2, win.withdraw)


if __name__ == '__main__':
    a = attendant()
    a.loadTable()
    root = Tk()
    gui = GUI(root)
    root.mainloop()
