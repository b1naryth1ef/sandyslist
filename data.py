from mongoengine import *
from datetime import datetime

connect('sandy', host='hydr0.com', port=27017)

class Request(Document):
    name = StringField()
    request = StringField()
    location = StringField()
    contact = StringField()
    urgent = BooleanField()
    time = DateTimeField(default=datetime.now)
    responses = ListField(ReferenceField('FollowUp'))
    valid = BooleanField(default=True)

class FollowUp(Document):
    name = StringField()
    cangive = StringField()
    contact = StringField()
    time = DateTimeField(default=datetime.now)
    entry = ReferenceField(Request)
    valid = BooleanField(default=False)
    connected = BooleanField(default=False)