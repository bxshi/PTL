__author__ = 'bxshi'
from mongoengine import Document
from mongoengine import EmbeddedDocument
from mongoengine import EmbeddedDocumentField
from mongoengine import StringField
from mongoengine import FloatField
from mongoengine import IntField
from mongoengine import BinaryField
from mongoengine import DateTimeField
from mongoengine import ListField
from mongoengine import ReferenceField
from mongoengine import CASCADE

from user import User

class Quiz(Document):
    creator         =   ReferenceField(User, reverse_delete_rule=CASCADE)
    info            =   ListField(EmbeddedDocumentField("QuizInfo"))
    description     =   StringField(max_length=100)
    attachment      =   ListField(EmbeddedDocumentField("QuizAttach"))
    correctanswer   =   ListField(EmbeddedDocumentField("QuizAnswer"))
    wronganswer     =   ListField(EmbeddedDocumentField("QuizAnswer"))
    manualdifficulty=   FloatField(min_value=0, max_value=1)
    autodifficulty  =   FloatField(min_value=0, max_value=1)
    checkout        =   ListField(EmbeddedDocumentField("QuizCheckcout"))
    tag             =   ListField(StringField(max_length=20))

class Test(Document):
    createdate      =   DateTimeField()             #Create datetime
    description     =   StringField()               #decription of this test
    takennumber     =   IntField()                  #the number of students who may take this test
    quiz            =   ListField(EmbeddedDocumentField('TestQuiz'))

class TestQuiz(EmbeddedDocument):
    quiz            =   ListField(ReferenceField(Quiz))
    #Reference to Quiz, if Quiz is deleted, this reference will be deleted too.
    correct         =   IntField()
    #how many students got this right

class QuizInfo(EmbeddedDocument):
    type            =   StringField()
    description     =   StringField()

class QuizAttach(EmbeddedDocument):
    file            =   BinaryField()
    description     =   StringField()

class QuizAnswer(EmbeddedDocument):
    answer          =   StringField()
    attach          =   BinaryField()

class QuizCheckout(EmbeddedDocument):
    time            =   DateTimeField()
    type            =   IntField()
    description     =   StringField()
    test            =   ReferenceField(Test)


