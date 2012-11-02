from mongoengine import *
from datetime import datetime
from mongoenginepagination import Document
import os

if os.getenv('USE_MLAB'):
    print 'A'
    connect('heroku_app8846523', host=os.getenv('MONGOLAB_URI', 'mongodb://localhost:27017'))
else:
    print 'B'
    connect('sandy', host='hydr0.com') #Dev server

class Request(Document):
    name = StringField()
    request = StringField()
    location = StringField()
    contact = StringField()
    urgent = BooleanField()
    time = DateTimeField(default=datetime.now)
    responses = ListField(ReferenceField('FollowUp'))
    valid = BooleanField(default=True)
    connected = BooleanField(default=False)

class FollowUp(Document):
    name = StringField()
    cangive = StringField()
    contact = StringField()
    time = DateTimeField(default=datetime.now)
    entry = ReferenceField(Request)
    valid = BooleanField(default=False)
    connected = BooleanField(default=False)
