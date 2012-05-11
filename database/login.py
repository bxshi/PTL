__author__ = 'bxshi'
from mongoengine import Document
from mongoengine import StringField

#used for login, will deleted when logout
class Login(Document):
    session     =   StringField(required=True, unique=True)
    username    =   StringField(required=True, unique=True)