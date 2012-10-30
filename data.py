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
