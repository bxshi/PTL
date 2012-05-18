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
    """Quiz database

        creator

        info

        description

        attachment

        correctanswer

        wronganswer

        manualdifficulty

        autodifficulty

        checkout

        tag

    """
    creator         =   StringField(max_length=100, required=True)
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
    """Test database

        createdate  Create datetime

        description decription of this test

        takenumber  the number of students who may take this test

        quiz    embeded TestQuiz

    """
    createdate      =   DateTimeField()             #Create datetime
    description     =   StringField()               #decription of this test
    takennumber     =   IntField()                  #the number of students who may take this test
    quiz            =   ListField(EmbeddedDocumentField('TestQuiz'))

class TestQuiz(EmbeddedDocument):
    """TestQuiz, embedded in test.quiz

        quiz    link to quiz

        correct how many students got this right

    """
    quiz            =   ListField(ReferenceField(Quiz))
    #Reference to Quiz, if Quiz is deleted, this reference will be deleted too.
    correct         =   IntField()
    #how many students got this right

class QuizInfo(EmbeddedDocument):
    """QuizInfo, embedded in quiz.info

        type

        description

    """
    type            =   StringField()
    description     =   StringField()

class QuizAttach(EmbeddedDocument):
    """QuizAttach, embedded in quiz.attachment

        file

        description

    """
    file            =   BinaryField()
    description     =   StringField()

class QuizAnswer(EmbeddedDocument):
    """QuizAnswer, embedded in quiz.rightanswer and quiz.wronganswer

        answer

        attach

    """
    answer          =   StringField()
    attach          =   BinaryField()

class QuizCheckout(EmbeddedDocument):
    """QuizCheckout, embedded in quiz.checkout

        time

        type

        description

        test

    """
    time            =   DateTimeField()
    type            =   IntField()
    description     =   StringField()
    test            =   ReferenceField(Test)


