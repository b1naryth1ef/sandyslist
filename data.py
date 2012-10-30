from mongoengine import *

connect('sandy', host='hydr0.com', port=27017)

class Market(Document):
    name = StringField()
    people = IntField()
    animals = BooleanField()
    pos = GeoPointField()
    phone = StringField()
    email = StringField()
    twitter = StringField()
