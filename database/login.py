__author__ = 'bxshi'
from mongoengine import Document
from mongoengine import StringField

#used for login, will deleted when logout
class Login(Document):
    """Login database, temporary use. When login, add session and username, when logout, delete it in this database.

        session

        username

    """
    session     =   StringField(required=True, unique=True)
    username    =   StringField(required=True, unique=True)