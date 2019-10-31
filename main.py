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
        self.ddb = boto3.resource('dynamodb', region_name='us-east-2')
        self.data = self.loadTable()

        # the length of what a valid uid will be
        self.validLength = 10

        # the list of commands the attendant can be issued
        self.listOfCommands =   {
                                'to' : self.techOut,
                                'c' : self.changeName,
                                'ti' : self.techIn
                                }

    # make the browser add data to the db
    def add(self, item, screen):
        self.data.put_item(Item = item)
        a.greet(item['status'], item['name'], surf)

    # change the name of the user
    def changeName(self, screen):
        # prompt the attendant to enter the revised name
        a.retrievedData['name'] = input('NEW USER NAME:\t')

        # add the new name back into the db
        a.add(a.retrievedData, screen)

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
    def techOut(self, screen):

        # pulls the currentTech field from the retrieved data for user
        currentTech = self.retrievedData['tech']
        # print out what the user checked out
        if len(currentTech) == 0:
            print("USER HAS NOTHING CHECKED OUT")
        else:
            print("CURRENTLY USER HAS THE FOLLOWING TECH CHECKED OUT:")
            for count, i in enumerate(currentTech):
                print(count, i)

        # ask the user to enter what tech is being checked out
        tech = input("ENTER TECH TO BE CHECKED OUT:\t\t")
        self.retrievedData['tech'].append(tech)
        self.add(self.retrievedData)

        return 1

    # return tech, user have to input what tech
    def techIn(self, screen):

        # pulls the currentTech field from the retrieved data for user
        currentTech = self.retrievedData['tech']

        # print out what the user checked out, stops if there is nothing to return
        if len(currentTech) == 0:
            print("USER HAS NOTHING TO RETURN")
        else:
            print("CURRENTLY USER HAS THE FOLLOWING TECH CHECKED OUT:")
            for count, i in enumerate(currentTech):
                print(count, i)

                # ask what is returned and update
                returnTech = int(input("ENTER THE NUMBER OF THE TECH BEING RETURNED:\t\t"))
                del currentTech[returnTech]
                self.retrievedData['tech'] = currentTech
                self.add(self.retrievedData)

                # print out items that still need to be returned
                if len(currentTech) == 0:
                    print("USER RETURNED EVERYTHING")
                else:
                    print("USER STILL HAS THE FOLLOWING TECH CHECKED OUT:")
                    for count, i in enumerate(currentTech):
                        print(count, i)
        return 1

    def interpretCommands(self, command, screen):
        returnedValue = self.listOfCommands[command](screen)
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

        display_box(surf, (surf.get_width() / 20), (surf.get_height() / 3 * 2), black, white, "Welcome to helloWorld!")

        try:
            userInput = input("USER ID:\t\t").split( )

            a.loadTable()

            uid = userInput[-1]
            tech = []

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
                    a.add(a.retrievedData, surf)

                # else if the user exists but there was a command issued
                elif exists and len(userInput) > 1:

                    command = userInput[0]
                    a.interpretCommands(command, surf)

                # prompt user to enter name if not already in the system
                else:
                    userName = input("USER NAME:\t\t")
                    newUser = {'participantID' : uid, 'name' : userName, 'status' : 1, 'tech' : tech}
                    a.add(newUser)
                    print(userName.split(' ')[0])
                    display_box(surf, (surf.get_width() / 10), (surf.get_height() / 3 * 2), green, black, "Welcome, {}!".format(userName.split(' ')[0]))
                    print('\n')

        except:
            print("EXCEPTON OCCURED : PLEASE TRY AGAIN")
