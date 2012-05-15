__author__ = 'bxshi'
from mongoengine import Document
from mongoengine import ListField
from mongoengine import EmbeddedDocument
from mongoengine import EmbeddedDocumentField
from mongoengine import DateTimeField
from mongoengine import StringField
from mongoengine import BooleanField

class User(Document):
    """User database

        username

        password

        publickey

        privatekey

        log

    """
    username    =   StringField(max_length=20, required=True, unique=True)
    #username
    password    =   StringField(max_length=32, required=True)           #md5 password
    publickey   =   StringField()                                       #RSA pubkey, optional
    privatekey  =   StringField()                                       #RSA prikey, optional
    log         =   ListField(EmbeddedDocumentField("UserLog"))         #login logs

class UserLog(EmbeddedDocument):
    """user log database, embedded in user.log

        time

        ip

        login

        newip

    """
    time        =   DateTimeField(required=True)                        #log time
    ip          =   StringField(max_length=15, required=True)           #log ip address
    login       =   BooleanField(required=True, default=False)          #True:logged in False: Not login
    #Warning! If you new create this project,
    # change required=True
    newip       =   BooleanField(default=True)                          #True: New ip address False: Used ip address
