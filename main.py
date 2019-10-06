import boto3
from boto3.dynamodb.conditions import Key, Attr

class attendant():

    def __init__(self):
        # connect to dynamodb
        self.ddb = boto3.resource('dynamodb', region_name='us-east-1',
                          endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
        self.data = self.ddb.Table('practiceAttendance')

    # make the browser add data to the db
    def add(self, item):
        self.data.put_item(Item = item)


    def checkExists(self, userID):
        exists = False
        for item in self.data.sca()['Items']['participantID']:
            if item


if __name__ == '__main__':
    a = attendant()

    item = {
            'participantID'  : 54321,
            'name' : 'Jane Doe'
            }
    a.add(item)
    print(a.data.scan()['Items'])
