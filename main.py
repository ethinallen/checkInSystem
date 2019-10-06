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
        self.inOut = ['IN', 'OUT']

    # make the browser add data to the db
    def add(self, item):
        self.data.put_item(Item = item)

    # queries ddb to see if the userID exists
    def checkExists(self, uid):
        retrievedData = self.data.query(KeyConditionExpression=Key('participantID').eq(uid))
        if retrievedData['Count'] == 0:
            return None, False
        else:
            return retrievedData, True

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

if __name__ == '__main__':

    # make an attendant instance
    a = attendant()

    # continuously check for checkins / outs
    while True:
        uid = input('USER ID:\t\t')

        a.loadTable()

        # if the uid is valid length
        if a.verifyUID(uid):

            # change uid to int after length is verified
            uid = int(uid)

            # try to retrieve data from ddb
            retrievedData, exists = a.checkExists(uid)

            # if the user exists
            if exists:
                retrievedData['Items'][0]['status'] *= -1
                print(retrievedData['Items'][0]['status'])

                a.add(retrievedData['Items'][0])

            # if no uid associated yet
            else:
                userName = input("USER NAME:\t\t")
                newUser = {'participantID' : uid, 'name' : userName, 'status' : 1}
                a.add(newUser)
                print('\n')
