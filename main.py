import boto3
from boto3.dynamodb.conditions import Key, Attr

class attendant():

    def __init__(self):
        # connect to dynamodb
        self.ddb = boto3.resource('dynamodb', region_name='us-east-1',
                          endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
        self.data = self.loadTable()

    # make the browser add data to the db
    def add(self, item):
        self.data.put_item(Item = item)

    '''
    will eventually turn this into a ddb query but this is just a
    hotfix for the moment
    '''
    def checkExists(self, userID):
        retrievedData = self.data.query(KeyConditionExpression=Key('participantID').eq(userID))
        if retrievedData['Count'] == 0:
            return False
        else:
            print(retrievedData['Items'][0]['name'])
            return True

    # load the table in init and every time an action happens at the table
    def loadTable(self):
        data = self.ddb.Table('practiceAttendance')
        return data


if __name__ == '__main__':
    a = attendant()
    while True:
        userID = int(input('USER ID:\t\t'))

        a.loadTable()

        if a.checkExists(userID):
            print("Yep they exist!\n")
        else:
            userName = input("USER NAME:\t\t")
            newUser = {'participantID' : userID, 'name' : userName}
            a.add(newUser)
            print('\n')
