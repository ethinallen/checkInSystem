import boto3
from boto3.dynamodb.conditions import Key, Attr

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
                                'tech' : self.checkTech
                                }

    # make the browser add data to the db
    def add(self, item):
        self.data.put_item(Item = item)

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
            print("CARD READ ERROR - SCAN AGAIN")
            return False
        else:
            return True

    # load the table in init and every time an action happens at the table
    def loadTable(self):
        data = self.ddb.Table('practiceAttendance')
        return data

    def checkTech(self):
        currentTech = self.retrievedData['tech']
        if currentTech == None:
            tech = input("ENTER TECH TO BE CHECKED OUT:\t\t")
            self.retrievedData['tech'] = tech
            self.add(self.retrievedData)

        else:
            print("USER ALREADY HAS THE FOLLOWING TECH CHECKED OUT:\t{}".format(currentTech))

    def interpretCommands(self, command):
        returnedValue = self.listOfCommands[command]()
        return returnedValue

    def greet(self, status, name):
        if status > 0:
            print("Welcome Back {}!".format(name))
        else:
            print("See you later, {}!".format(name))

if __name__ == '__main__':

    # make an attendant instance
    a = attendant()

    # continuously check for checkins / outs
    while True:

        try:
            userInput = input("USER ID:\t\t").split( )

            a.loadTable()

            uid = userInput[-1]

            # if the uid is valid length
            if a.verifyUID(uid):

                # change uid to int after length is verified
                uid = int(uid)

                # try to retrieve data from ddb
                exists = a.checkExists(uid)

                # if the user exists
                if exists and len(userInput) == 1:
                    a.retrievedData['status'] *= -1
                    newStatus = int(a.retrievedData['status'])
                    name = a.retrievedData['name']
                    a.greet(newStatus, name)
                    a.add(a.retrievedData)

                # else if the user exists but there was a command issued
                elif exists and len(userInput) > 1:

                    # makes sure that they user is currently clocked into event
                    if a.retrievedData['status'] == -1:
                        print("\n\nCURRENTLY SWIPED OUT OF EVENT : PLEASE RE-ENTER TO CHECK OUT TECH\n\n")

                    # else add the user to the event and change the name of their phone
                    else:
                        command = userInput[0]
                        a.retrievedData[command] =  a.interpretCommands(command)

                # prompt user to enter name if not already in the system
                else:
                    userName = input("USER NAME:\t\t")
                    newUser = {'participantID' : uid, 'name' : userName, 'status' : 1, 'tech' : None}
                    a.add(newUser)
                    print('\n')

        except:
            print("EXCEPTON OCCURED : PLEASE TRY AGAIN")
