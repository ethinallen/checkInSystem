import boto3
from boto3.dynamodb.conditions import Key, Attr
import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *
import time

white = (255, 255, 255)
black = (0, 0, 0)
green = (50,205,50)
red = (220,20,60)

def display_box(screen, width, height, bgcolor, textcolor, message):
    screen.fill(bgcolor)
    bug = pygame.image.load('bug.png')
    screen.blit(bug, ((screen.get_width() / 8), (-200)))
    fontobject=pygame.font.SysFont('Arial', 160)
    if len(message) != 0:
        print(message)
        screen.blit(fontobject.render(message, 1, textcolor), (width, height))
    pygame.display.flip()
    time.sleep(2)

def get_key():
    while True:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            return event.key


class attendant():

    def __init__(self):
        # connect to dynamodb
        self.ddb = boto3.resource('dynamodb', region_name='us-east-1',
                          endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
        self.data = self.loadTable()

        # the length of what a valid uid will be
        self.validLength = 10

        # the list of commands the attendant can be issued
        self.listOfCommands =   {
                                't' : self.checkTech,
                                'c' : self.changeName
                                }

    # make the browser add data to the db
    def add(self, item):
        self.data.put_item(Item = item)

    def changeName(self):
        # prompt the attendant to enter the revised name
        a.retrievedData['name'] = input('NEW USER NAME:\t')

        # add the new name back into the db
        a.add(a.retrievedData)

        return 1


    # queries ddb to see if the userID exists
    def checkExists(self, uid):
        self.retrievedData = self.data.query(KeyConditionExpression=Key('participantID').eq(uid))

        if self.retrievedData['Count'] == 0:
            return False
        else:
            self.retrievedData = self.retrievedData['Items'][0]
            return True

    # verify the length of the entered uid
    def verifyUID(self, uid, screen):
        if len(str(uid)) != self.validLength:
            # display_box(surf, (screen.get_width() / 10), (screen.get_height() / 3 * 2), green, black, "Welcome Back {}!".format(name))
            display_box(surf, (screen.get_width() / 100), (screen.get_height() / 3 * 2), red, black, "Error: Please scan again!")
            return False
        else:
            return True

    # load the table in init and every time an action happens at the table
    def loadTable(self):
        data = self.ddb.Table('practiceAttendance')
        return data

    # verifies if the user has checked out tech or not; raises flag if tech is checked out
    def checkTech(self):

        # pulls the currentTech field from the retrieved data for user
        currentTech = self.retrievedData['tech']

        # if the user does not have tech checked out
        if currentTech == None:
            tech = input("ENTER TECH TO BE CHECKED OUT:\t\t")
            self.retrievedData['tech'] = tech
            self.add(self.retrievedData)

        else:
            display_box(surf, (screen.get_width() / 10), (screen.get_height() / 3 * 2), red, black, "USER ALREADY HAS THE FOLLOWING TECH CHECKED OUT:\t{}".format(currentTech))

        return 1

    def interpretCommands(self, command):
        returnedValue = self.listOfCommands[command]()
        return returnedValue

    # welcome the user back / see them later
    def greet(self, status, name, screen):
        if status > 0:
            display_box(surf, (screen.get_width() / 10), (screen.get_height() / 3 * 2), green, black, "Welcome Back {}!".format(name.split(' ')[0]))
        else:
            display_box(surf, (screen.get_width() / 10), (screen.get_height() / 3 * 2), green, black, "See you later, {}!".format(name.split(' ')[0]))

if __name__ == '__main__':

    # Graphics initialization
    full_screen = False
    window_size = (1920, 1080)
    pygame.init()

    if full_screen:
        surf = pygame.display.set_mode(window_size, HWSURFACE | FULLSCREEN | DOUBLEBUF)
    else:
        surf = pygame.display.set_mode(window_size)

    # make an attendant instance
    a = attendant()

    # continuously check for checkins / outs
    while True:

        display_box(surf, (surf.get_width() / 20), (surf.get_height() / 3 * 2), black, white, "Welcome to Hello World!")

        try:
            userInput = input("USER ID:\t\t").split( )

            a.loadTable()

            uid = userInput[-1]

            # if the uid is valid length
            if a.verifyUID(uid, surf):

                # change uid to int after length is verified
                uid = int(uid)

                # try to retrieve data from ddb
                exists = a.checkExists(uid)

                # if the user exists
                if exists and len(userInput) == 1:
                    a.retrievedData['status'] *= -1
                    newStatus = int(a.retrievedData['status'])
                    name = a.retrievedData['name']
                    a.greet(newStatus, name, surf)
                    a.add(a.retrievedData)

                # else if the user exists but there was a command issued
                elif exists and len(userInput) > 1:

                    command = userInput[0]
                    a.interpretCommands(command)

                # prompt user to enter name if not already in the system
                else:
                    userName = input("USER NAME:\t\t")
                    newUser = {'participantID' : uid, 'name' : userName, 'status' : 1, 'tech' : None}
                    a.add(newUser)
                    print(userName.split(' ')[0])
                    display_box(surf, (surf.get_width() / 10), (surf.get_height() / 3 * 2), green, black, "Welcome, {}!".format(userName.split(' ')[0]))
                    print('\n')

        except:
            print("EXCEPTON OCCURED : PLEASE TRY AGAIN")
