from mongoengine import *
from datetime import datetime
from mongoenginepagination import Document
import os

connect('heroku_app8846523', host=os.getenv('MONGOLAB_URI', 'mongodb://localhost:27017'))

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
