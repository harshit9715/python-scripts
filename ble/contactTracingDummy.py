from uuid import uuid4 as v4
import random
import json
import boto3
from datetime import datetime, tzinfo, timedelta

# resource = boto3.resource('dynamodb', region_name='us-east-1')


matches = lambda : random.choice([0]+[random.randrange(i) for i in range(1,random.choice([1,1,1,1,1,1,10,10,25,50]))])

days = lambda : [[[v4().hex for i in range(matches())] for i in range(24)] for i in range(15)]

class simple_utc(tzinfo):
    def tzname(self,**kwargs):
        return "UTC"
    def utcoffset(self, dt):
        return timedelta(0)
gettime = lambda : datetime.utcnow().replace(tzinfo=simple_utc()).isoformat()[:-9]+'Z'

createDbItem = lambda: {
    'PutRequest': {
        'Item': {
            "Partition": "Contact",
            "CreationTime": gettime(),
            "Data": {
                "days": days(),
                "startDay": 18521
            }
        }
    }
}

li = [["createDbItem()" for i in range(25)] for i in range(2000)]


# try:
#     resource.batch_write_item(RequestItems={
#         'CovidApp-Interactions': tabledata
#     })
#     print(f'resource, specify all types : write succeeded.')
# except Exception as e:
#     print(f'resource, specify all types : write failed: {e}')
