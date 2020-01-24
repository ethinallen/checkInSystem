from tkinter import *
from tkinter import ttk

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
        #self.master.state("zoomed")
        self.diet = IntVar()
        self.initUI()

    def initUI(self):
        # button sizes
        BUTTON_WIDTH = int(self.master.winfo_screenwidth() / 75)
        BUTTON_HEIGHT = int(self.master.winfo_screenheight() / 150)
        # background and icon
        self.master.title("CUhackit Check In System")
        self.master.configure(background="white")
        self.background = PhotoImage(file="bg.png")
        Label(self.master, image=self.background, bg="white").grid(row=0, columnspan=4)
        Label(self.master, bg="white").grid(rowspan=7, column=0)
        Label(self.master, bg="white").grid(rowspan=7, column=3)

        # Label
        self.labelTitle = Label(self.master, text="Check In System", bg="white", font="Ariel 30 bold")
        self.labelSubtitle = Label(self.master, font="Ariel 20 bold", bg="white")
        self.labelTechList = Label(self.master, font="Ariel 20 bold", bg="white", anchor='w')

        # buttons for attendance, tech check, status check
        self.buttonAttend = Button(self.master, text="Check In", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                   command=lambda: self.checkInMenu())
        self.buttonCName = Button(self.master, text="Change Name", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                  command=lambda: self.changeNameMenu())
        self.buttonTO = Button(self.master, text="Check Out Tech", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                               command=lambda: self.techOutMenu())
        self.buttonTI = Button(self.master, text="Return Tech", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                               command=lambda: self.techInMenu())
        self.buttonMeal = Button(self.master, text="Swipe Meal", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                 command=lambda: self.mealGUI())
        self.buttonStatus = Button(self.master, text="Show Status", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                   command=lambda: self.checkStatus())
        self.buttonWorkshop = Button(self.master, text="Workshop", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                     command=lambda: self.workshopGUI())
        self.buttonMainMenu = Button(self.master, text="Back", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                     command=lambda: self.mainMenu())
        self.buttonEnter = Button(self.master, text="Enter", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, )
        self.CheckButtonDiet = Checkbutton(self.master, text="Dietary Restriction", bg="white", variable=self.diet)

        # entry for inputs
        self.entryInput = Entry(self.master, font="Aerial 30")

        # resize widget based on window size
        for i in range(5):
            self.master.grid_columnconfigure(i, weight=1)
        for i in range(6):
            self.master.grid_rowconfigure(i, weight=1)

        # default grid setup
        self.labelTitle.grid(row=1, column=1, columnspan=2)
        self.mainMenuWidget(True)

    def mainMenu(self):
        # change menu title
        self.labelTitle.configure(text="Check In System")
        # add main menu buttons
        self.mainMenuWidget(True)
        # remove other menu widgets
        self.labelSubtitle.grid_forget()
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
        self.mainMenuWidget(False)
        # add checkInMenu widgets
        self.buttonMainMenu.grid(row=5, column=0)
        self.buttonEnter.grid(row=3, column=3, sticky=W)
        self.entryInput.grid(row=3, column=1, columnspan=2)
        self.labelSubtitle.configure(text="Enter ID")
        self.labelSubtitle.grid(row=2, column=1, columnspan=2)
        # make sure keyboard focus on the entry
        self.entryInput.focus_set()
        # set keys
        self.buttonEnter.configure(command=lambda: self.checkIn(event=None))
        self.master.bind('<Return>', self.checkIn)

    def changeNameMenu(self):
        # change menu title
        self.labelTitle.configure(text="Change Name")
        # get rid of main menu widgets
        self.mainMenuWidget(False)
        # add checkInMenu widgets
        self.buttonMainMenu.grid(row=5, column=0)
        self.buttonEnter.grid(row=3, column=3, sticky=W)
        self.entryInput.grid(row=3, column=1, columnspan=2)
        self.labelSubtitle.configure(text="Enter ID")
        self.labelSubtitle.grid(row=2, column=1, columnspan=2)
        # make sure keyboard focus on the entry
        self.entryInput.focus_set()
        # set keys
        self.buttonEnter.configure(command=lambda: self.changeName(event=None))
        self.master.bind('<Return>', self.changeName)

    def techOutMenu(self):
        # change menu title
        self.labelTitle.configure(text="Check Out Tech")
        # get rid of main menu widgets
        self.mainMenuWidget(False)
        # add checkInMenu widgets
        self.buttonMainMenu.grid(row=5, column=0)
        self.buttonEnter.grid(row=3, column=3, sticky=W)
        self.entryInput.grid(row=3, column=1, columnspan=2)
        self.labelSubtitle.configure(text="Enter ID")
        self.labelSubtitle.grid(row=2, column=1, columnspan=2)
        # set keys
        self.buttonEnter.configure(command=lambda: self.techOut(event=None))
        self.master.bind('<Return>', self.techOut)

    def techInMenu(self):
        # change menu title
        self.labelTitle.configure(text="Return Tech")
        # get rid of main menu widgets
        self.mainMenuWidget(False)
        # add checkInMenu widgets
        self.buttonMainMenu.grid(row=5, column=0)
        self.buttonEnter.grid(row=3, column=3, sticky=W)
        self.entryInput.grid(row=3, column=1, columnspan=2)
        self.labelSubtitle.configure(text="Enter ID")
        self.labelSubtitle.grid(row=2, column=1, columnspan=2)
        # set keys
        self.buttonEnter.configure(command=lambda: self.techIn(event=None))
        self.master.bind('<Return>', self.techIn)

    # main function for adding new user, checking in and out old users
    def checkIn(self, event):
        if a.verifyUID(self.entryInput.get()):
            self.uid = self.entryInput.get()
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
                self.labelSubtitle.configure(text="Enter Name")
                # diet check box
                self.diet.set(0)
                self.CheckButtonDiet.grid(row=4, column=1, columnspan=2)
        else:
            self.popUp("Error: Invalid ID", "red")

        self.entryInput.delete(0, 'end')

    # main function for changing name of an existing user
    def changeName(self, event):
        if a.verifyUID(self.entryInput.get()):
            self.uid = self.entryInput.get()
            if a.checkExists(self.uid):
                self.buttonEnter.configure(command=lambda: self.changeNameHelper(event=None))
                self.master.bind('<Return>', self.changeNameHelper)
                self.entryInput.delete(0, 'end')
                self.buttonMainMenu.configure(state="disabled")
                self.labelSubtitle.configure(text="Enter Name")
                self.diet.set(0)
                self.CheckButtonDiet.grid(row=4, column=1, columnspan=2)
            else:
                self.popUp("Error: User does not exist", "red")
        else:
            self.popUp("Error: Invalid ID", "red")

        self.entryInput.delete(0, 'end')

    # main function for checking out tech
    def techOut(self, event):
        if a.verifyUID(self.entryInput.get()):
            self.uid = self.entryInput.get()
            if a.checkExists(self.uid):
                self.buttonEnter.configure(command=lambda: self.techOutHelper(event=None))
                self.master.bind('<Return>', self.techOutHelper)
                self.entryInput.delete(0, 'end')
                self.buttonMainMenu.configure(state="disabled")
                self.labelSubtitle.configure(text="Enter Tech to be Checked Out")
            else:
                self.popUp("Error: User does not exist", "red")
        else:
            self.popUp("Error: Invalid ID", "red")

        self.entryInput.delete(0, 'end')

    # main function for returning tech
    def techIn(self, event):
        if a.verifyUID(self.entryInput.get()):
            self.uid = self.entryInput.get()
            if a.checkExists(self.uid):
                if len(a.retrievedData['tech']) != 0:
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
                    self.labelTechList.grid(row=2, column=1, columnspan=2)
                    self.labelSubtitle.configure(text="Enter the Number of the Tech")
                    self.labelSubtitle.grid(row=3, column=1, columnspan=2)
                    self.entryInput.grid(row=4, column=1, columnspan=2)
                    self.buttonEnter.grid(row=4, column=3, sticky=W)
                else:
                    self.popUp("Error: User has no item checked out", "red")
            else:
                self.popUp("Error: User does not exist", "red")
        else:
            self.popUp("Error: Invalid ID", "red")

        self.entryInput.delete(0, 'end')

    # check status for all users in the database
    # used pack to format because it's easier for this situation
    # if you can, convert it to grid
    def checkStatus(self):
        # helper method for scroll bar
        def yview(*args):
            for i in listCollection:
                i.yview(*args)

        # helper method for scrolling outside the bar
        def onMouseWheel(event):
            # event 4 and 5 are for linux, not tested
            # else is for windows, tested
            if event.num == 4:
                delta = int(-1 * (event.delta / 120))
            elif event.num == 5:
                delta = int((event.delta / 120))
            else:
                delta = int(-1 * (event.delta / 120))
            for i in listCollection:
                i.yview("scroll", delta, "units")
            # this prevents default bindings from firing, which
            # would end up scrolling the widget twice
            return "break"

        # initialize everything
        root = Toplevel()
        root.geometry("1200x240")
        mainFrame = Frame(root)
        topFrame = Frame(mainFrame)
        bottomFrame = Frame(mainFrame)
        scroll = Scrollbar(root, orient="vertical", command=yview)
        labelName = Label(topFrame, text="Name", font="Ariel 10 bold")
        labelID = Label(topFrame, text="ID", font="Ariel 10 bold")
        labelStatus = Label(topFrame, text="Status", font="Ariel 10 bold")
        labelDiet = Label(topFrame, text="Diet Restriction", font="Ariel 10 bold")
        labelMeal1 = Label(topFrame, text="Meal 1", font="Ariel 10 bold")
        labelMeal2 = Label(topFrame, text="Meal 2", font="Ariel 10 bold")
        labelMeal3 = Label(topFrame, text="Meal 3", font="Ariel 10 bold")
        labelMeal4 = Label(topFrame, text="Meal 4", font="Ariel 10 bold")
        labelMeal5 = Label(topFrame, text="Meal 5", font="Ariel 10 bold")
        nameList = Listbox(bottomFrame, yscrollcommand=scroll.set)
        iDList = Listbox(bottomFrame, yscrollcommand=scroll.set)
        statusList = Listbox(bottomFrame, yscrollcommand=scroll.set)
        dietList = Listbox(bottomFrame, yscrollcommand=scroll.set)
        meal1List = Listbox(bottomFrame, yscrollcommand=scroll.set)
        meal2List = Listbox(bottomFrame, yscrollcommand=scroll.set)
        meal3List = Listbox(bottomFrame, yscrollcommand=scroll.set)
        meal4List = Listbox(bottomFrame, yscrollcommand=scroll.set)
        meal5List = Listbox(bottomFrame, yscrollcommand=scroll.set)
        listCollection = [nameList, iDList, statusList, dietList, meal1List, meal2List, meal3List, meal4List, meal5List]
        labelCollection = [labelName, labelID, labelStatus, labelDiet, labelMeal1, labelMeal2, labelMeal3, labelMeal4,
                           labelMeal5]
        # binding mouse wheel to scroll, button 4 and 5 is mouse wheel for linux
        for i in listCollection:
            i.bind("<MouseWheel>", onMouseWheel)
            i.bind("<Button-4>", onMouseWheel)
            i.bind("<Button-5>", onMouseWheel)
        response = a.data.scan()
        # format window
        scroll.pack(side="right", fill="y")
        mainFrame.pack(fill="both", expand=True)
        topFrame.pack(side="top", fill="both", expand=True)
        bottomFrame.pack(side="bottom", fill="both", expand=True)
        for i in labelCollection:
            i.pack(side="left", fill="x", expand=True)
        for i in listCollection:
            i.pack(side="left", fill="both", expand=True)
        # adding to the two lists
        for i in response['Items']:
            nameList.insert(END, i['name'])
            iDList.insert(END, i['participantID'])
            if i['status'] == 1:
                statusList.insert(END, "IN")
            else:
                statusList.insert(END, "OUT")
            if i['diet'] == 1:
                dietList.insert(END, "YES")
            else:
                dietList.insert(END, "NO")
            for j in range(5):
                if i['meal'][j] == 1:
                    listCollection[j + 4].insert(END, "Not Used")
                else:
                    listCollection[j + 4].insert(END, "Used")

    # helper function for checkIn, adds new user to database
    def addNewUser(self, event):
        # adding user to database
        # a list containing tech, empty at first
        tech = []
        # a list containing meal swipe, 1 for not used, -1 for used
        meal = [1, 1, 1, 1, 1]
        # a list containing workshop info, 1 for attended, 0 for not attend
        workshop = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        username = self.entryInput.get()
        diet = self.diet.get()
        newUser = {'participantID': self.uid, 'name': username, 'status': 1, 'tech': tech, 'meal': meal,
                   'workshop': workshop, 'diet': diet}
        a.add(newUser)
        # format the window
        self.buttonEnter.configure(command=lambda: self.checkIn(event=None))
        self.master.bind('<Return>', self.checkIn)
        self.buttonMainMenu.configure(state="normal")
        self.labelSubtitle.configure(text="Enter ID")
        self.CheckButtonDiet.grid_forget()
        self.diet.set(0)
        self.entryInput.delete(0, 'end')
        self.greet(newUser, True)

    # helper function for change name
    def changeNameHelper(self, event):
        username = self.entryInput.get()
        diet = self.diet.get()
        a.retrievedData['name'] = username
        a.retrievedData['diet'] = diet
        a.add(a.retrievedData)
        # format the window
        self.buttonMainMenu.configure(state="normal")
        self.entryInput.delete(0, 'end')
        self.diet.set(0)
        self.CheckButtonDiet.grid_forget()
        self.mainMenu()
        self.popUp("User name changed to " + username, "green")

    # helper function for tech out
    def techOutHelper(self, event):
        tech = self.entryInput.get()
        if len(tech) > 0:
            a.retrievedData['tech'].append(tech)
            a.add(a.retrievedData)
            # format the window
            self.buttonMainMenu.configure(state="normal")
            self.entryInput.delete(0, 'end')
            self.mainMenu()
            self.popUp(tech + " checked out", "green")

    # helper function for tech in
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
        self.labelTechList.grid_forget()
        self.entryInput.delete(0, 'end')
        self.mainMenu()
        self.popUp(tech + " returned", "green")

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
    def popUp(self, text, color):
        win = Toplevel()
        win.configure(background=color)
        win.attributes("-fullscreen", True)
        Label(win, text=text, font="Ariel 30 bold", fg='black', bg=color).grid(column=0, row=0)
        win.columnconfigure(0, weight=1)
        win.rowconfigure(0, weight=1)
        # show the pop up window
        win.deiconify()
        # the time until pop up window disappear, in ms
        win.after(1000 * 2, win.withdraw)

    # another popup window for meal swipe
    def mealGUI(self):
        self.mealNum = None

        # helper for button
        # day = true if day, day = false if meal

        def buttonHelper(num, button):
            self.mealNum = num
            buttonSatLunch.configure(bg='white')
            buttonSatDinner.configure(bg='white')
            buttonSnack.configure(bg='white')
            buttonSunBF.configure(bg='white')
            buttonSunLunch.configure(bg='white')
            button.configure(bg='grey')

        # meal helper function
        def mealHelper(event):
            if a.verifyUID(entryMeal.get()):
                self.uid = entryMeal.get()
                if a.checkExists(self.uid):
                    if a.retrievedData['meal'][self.mealNum - 1] == 1:
                        a.retrievedData['meal'][self.mealNum - 1] = -1
                        a.add(a.retrievedData)
                        if a.retrievedData['diet'] == 1:
                            self.popUp("Meal Swiped (Dietary Restriction)", 'yellow')
                        else:
                            self.popUp("Meal Swiped", 'green')
                    else:
                        self.popUp("Error: Meal Already Swiped", "red")
                else:
                    self.popUp("Error: User does not exist", "red")
            else:
                self.popUp("Error: Invalid ID", "red")
            entryMeal.delete(0, 'end')

        win = Toplevel()
        win.configure(background="white")
        #win.state('zoomed')
        # set up buttons
        buttonSatLunch = Button(win, text="Saturday Lunch", font="Ariel 30 bold", fg='black', bg='white',
                                command=lambda: buttonHelper(1, buttonSatLunch))
        buttonSatDinner = Button(win, text="Saturday Dinner", font="Ariel 30 bold", fg='black', bg='white',
                                 command=lambda: buttonHelper(2, buttonSatDinner))
        buttonSnack = Button(win, text="Midnight Snack", font="Ariel 30 bold", fg='black', bg='white',
                             command=lambda: buttonHelper(3, buttonSnack))
        buttonSunBF = Button(win, text="Sunday Breakfast", font="Ariel 30 bold", fg='black', bg='white',
                             command=lambda: buttonHelper(4, buttonSunBF))
        buttonSunLunch = Button(win, text="Sunday Lunch", font="Ariel 30 bold", fg='black', bg='white',
                                command=lambda: buttonHelper(5, buttonSunLunch))
        # set up entry box
        entryMeal = Entry(win, font="Aerial 30")
        # set up label
        labelID = Label(win, text="Enter ID", font="Aerial 30", bg="white")
        # format widgets
        buttonSatLunch.grid(row=0, column=0, columnspan=3, sticky=E + W)
        buttonSatDinner.grid(row=0, column=3, columnspan=3, sticky=E + W)
        buttonSnack.grid(row=1, column=0, columnspan=2, sticky=E + W)
        buttonSunBF.grid(row=1, column=2, columnspan=2, sticky=E + W)
        buttonSunLunch.grid(row=1, column=4, columnspan=2, sticky=E + W)
        labelID.grid(row=2, column=2, columnspan=2, pady=60)
        entryMeal.grid(row=3, column=2, columnspan=2)
        entryMeal.focus_set()
        win.bind('<Return>', mealHelper)
        # for grid widget format
        for i in range(6):
            win.grid_columnconfigure(i, weight=1)
        for i in range(4):
            win.master.grid_rowconfigure(i, weight=1)

    # popup window for workshop check in
    def workshopGUI(self):
        # workshop GUI helper
        def workshopHelper(event):
            if (dropMenuWorkshop.get() == "Select a Workshop"):
                self.popUp("Error: Select a Workshop", "red")
            else:
                workshopNum = 0
                if a.verifyUID(entryWorkshop.get()):
                    self.uid = entryWorkshop.get()
                    if a.checkExists(self.uid):
                        # find the current workshop
                        for i in workshopList:
                            if dropMenuWorkshop.get() == i:
                                break;
                            workshopNum += 1
                        a.retrievedData['workshop'][workshopNum] = 1
                        a.add(a.retrievedData)
                        self.popUp("User Checked In", "green")
                    else:
                        self.popUp("Error: User does not exist", "red")
                else:
                    self.popUp("Error: Invalid ID", "red")
            entryWorkshop.delete(0, 'end')

        win = Toplevel()
        win.configure(background="white")
        #win.state('zoomed')
        workshopList = ["Build an App with AWS", "Splunk Challenge Intro (11AM)", "Introduction to Git and Github",
                        "Introduction to Arduino", "Introduction to Python", "Data Science with Bioinformatics",
                        "Introduction to RESTful API", "Introduction to Web Development", "Machine Learning with AWS",
                        "Getting Started with Angular and Bootstrap", "Splunk Challenge Intro (5PM)",
                        "Working at AWS"]
        # label
        labelTitle = Label(win, text='Workshop Check In', font="Ariel 30 bold", fg='black', bg='white')
        labelSubtitle = Label(win, text='Enter ID', font="Ariel 30 bold", fg='black', bg='white')
        # set up workshop drop menu
        dropMenuWorkshop = ttk.Combobox(win, value=workshopList, state="readonly")
        dropMenuWorkshop.set("Select a Workshop")
        # input box
        entryWorkshop = Entry(win, font="Aerial 30")
        # widget format
        labelTitle.grid(row=0, column=1, sticky=W+E)
        dropMenuWorkshop.grid(row=1, column=1, pady=60, sticky=W+E)
        labelSubtitle.grid(row=2, column=1, sticky=W+E)
        entryWorkshop.grid(row=3, column=1, pady=60, sticky=W+E)
        entryWorkshop.focus_set()
        win.bind('<Return>', workshopHelper)
        # for grid widget format
        for i in range(3):
            win.grid_columnconfigure(i, weight=1)
        for i in range(4):
            win.master.grid_rowconfigure(i, weight=1)

    # helper method to grid all the main menu widgets
    # if add = true, add widgets, else remove
    def mainMenuWidget(self, add):
        if add:
            self.buttonAttend.grid(row=2, column=1, sticky=E)
            self.buttonCName.grid(row=2, column=2, sticky=W)
            self.buttonTO.grid(row=3, column=1, sticky=E)
            self.buttonTI.grid(row=3, column=2, sticky=W)
            self.buttonMeal.grid(row=4, column=1, sticky=E)
            self.buttonWorkshop.grid(row=4, column=2, sticky=W)
            self.buttonStatus.grid(row=5, column=1, sticky=E)
        else:
            self.buttonAttend.grid_forget()
            self.buttonCName.grid_forget()
            self.buttonTO.grid_forget()
            self.buttonTI.grid_forget()
            self.buttonMeal.grid_forget()
            self.buttonWorkshop.grid_forget()
            self.buttonStatus.grid_forget()


if __name__ == '__main__':
    a = attendant()
    a.loadTable()
    root = Tk()
    gui = GUI(root)
    root.mainloop()
