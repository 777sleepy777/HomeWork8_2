from mongoengine import *

class Task(Document):
    completed = BooleanField(default=False)
    consumer_fullname = StringField(max_length=150)
    email =  StringField(max_length=150)
