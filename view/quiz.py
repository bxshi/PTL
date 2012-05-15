__author__ = 'bxshi'
from hashlib import md5
from datetime import datetime
from django.http import HttpResponse
from Crypto.PublicKey import RSA
from Crypto import Random
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring

from database.quiz import *

class QuizParser():

    xml = None
    infolist = {}.fromkeys(('type', 'choose', 'order', 'selection number'))

    def __init__(self, quizxml=''):
        self.xml = quizxml

    def GetQuizInfo(self):
        return self.xml.find('quiz_info')

    def GetCreator(self):
        return self.xml.find('creator').text

    def GetDescription(self):
        return self.xml.find('description').text

    def GetAttachments(self):
        return self.xml.find('attachments')

    def GetCorrectAnswers(self):
        return self.xml.find('correct_answer')

    def GetWrongAnswers(self):
        return self.xml.find('wrong_answer')

    def GetManualDifficulty(self):
        return self.xml.find('manual_difficulty').text

    def GetAutoDifficulty(self):
        return self.xml.find('auto_difficulty').text

    def GetTags(self):
        return self.xml.find('tags')

    def GetInfoType(self):
        quizinfo = self.GetQuizInfo()
        if quizinfo is not None:
            return quizinfo.find('type')
        else:
            return None

    def GetInfoChoose(self):
        quizinfo = self.GetQuizInfo()
        if quizinfo is not None:
            return quizinfo.find('choose')
        else:
            return None

    def GetInfoOrder(self):
        quizinfo = self.GetQuizInfo()
        if quizinfo is not None:
            return quizinfo.find('order')
        else:
            return None

    def GetSelectionNumber(self):
        quizinfo = self.GetQuizInfo()
        if quizinfo is not None:
            return quizinfo.find('selection_number')
        else:
            return None

    def GetInfoDict(self):
        quizinfo = self.GetQuizInfo()
        if quizinfo is None:
            return None

        if quizinfo.find('type') is not None:
            self.infolist['type'] = quizinfo.find('type').text
        if quizinfo.find('choose') is not None:
            self.infolist['choose'] = quizinfo.find('choose').text
        if quizinfo.find('order') is not None:
            self.infolist['order'] = quizinfo.find('order').text
        if quizinfo.find('selection_number') is not None:
            self.infolist['selection number'] = quizinfo.find('selection_number').text
        return self.infolist

    def GetAttachmentList(self):
        attachments = self.GetAttachments()
        attachmentlist = list()
        if attachments is None:
            return None

        attachmentelementlist = attachments.findall('attachment')
        if not attachmentelementlist:
            while len(attachmentelementlist) > 0:
                tmpelement = attachmentelementlist.pop(0)
                attachmentdict = dict({'description' : tmpelement.find('description').text, 'file' : tmpelement.find('file').text})
                attachmentlist.append(attachmentdict)
        else:
            return None

        return attachmentlist

    def GetCorrectAnswerList(self):
        answers = self.GetCorrectAnswers()
        answerlist = list()
        if answers is None:
            return None

        answerelementlist = answers.findall('answer')
        if  len(answerelementlist) > 0:
            while len(answerelementlist) > 0:
                tmpanswer = answerelementlist.pop(0)
                answerdict = dict({"id":tmpanswer.find('id').text,"string":tmpanswer.find('string').text,"attach":tmpanswer.find('attach').text})
                answerlist.append(answerdict)
        else:
            return None

        return answerlist

    def GetWrongAnswerList(self):
        answers = self.GetWrongAnswers()
        answerlist = list()
        if answers is None:
            return None

        answerelementlist = answers.findall('answer')
        if  len(answerelementlist) > 0:
            while len(answerelementlist) > 0:
                tmpanswer = answerelementlist.pop(0)
                answerdict = dict({"id": tmpanswer.find('id').text,"string": tmpanswer.find('string').text,"attach": tmpanswer.find('attach').text})
                answerlist.append(answerdict)
        else:
            return None

        return answerlist

    def GetTagList(self):
        tags = self.GetTags()
        taglist = list()

        if tags is None:
            return None

        tagelementlist = tags.findall('tag')

        if  len(tagelementlist) > 0:
            while len(tagelementlist) > 0:
                tmptag = tagelementlist.pop(0)
                taglist.append(tmptag.text)
        else:
            return None

        return taglist

def QuizInsert(request, xmlstr=''):
    returnmsg = 'ERR UNKNOWN'

    if request.method is not 'POST':
        return HttpResponse('NO GET METHOD')

    xmlstr=request.POST.get('xml','')

    if xmlstr == '':
        returnmsg = "XML EPT"
    else:
        quizxml = fromstring(xmlstr)
        qp = QuizParser(quizxml.find('quiz'))
        quiz = Quiz(creator=qp.GetCreator(), description=qp.GetDescription(), manualdifficulty=int(qp.GetManualDifficulty()), autodifficulty=qp.GetAutoDifficulty())
        info = qp.GetInfoDict()

        #fill quiz info
        if info is not None:
            try:
                if info['type'] is not None:
                    quiz.info.append(QuizInfo(type='type', description=info['type']))
            except KeyError:
                pass
            try:
                if info['choose'] is not None:
                    quiz.info.append(QuizInfo(type='choose', description=info['choose']))
            except KeyError:
                pass
            try:
                if info['order'] is not None:
                    quiz.info.append(QuizInfo(type='order', description=info['order']))
            except KeyError:
                pass
            try:
                if info['selection number'] is not None:
                    quiz.info.append(QuizInfo(type='selection number', description=info['selection number']))
            except KeyError:
                pass

        #fill quiz attachments

        attch = qp.GetAttachmentList()
        if attch is not None:
            while len(attch) > 0:
                try:
                    tmpattch = attch.pop(0)
                    quiz.attachment.append(QuizAttach(description=tmpattch['description'], file=tmpattch['file']))
                except KeyError:
                    pass

        #fill answers

        answer = qp.GetCorrectAnswerList()
        if answer is not None:
            while len(answer) > 0:
                try:
                    tmpanswer = answer.pop(0)
                    quiz.correctanswer.append(answer=tmpanswer['string'],attach=tmpanswer['attach'])
                except KeyError:
                    pass

        answer = qp.GetWrongAnswerList()
        if answer is not None:
             while len(answer) > 0:
                try:
                    tmpanswer = answer.pop(0)
                    quiz.wronganswer.append(answer=tmpanswer['string'],attach=tmpanswer['attach'])
                except KeyError:
                    pass

        #fill tags
        tags = qp.GetTagList()
        if tags is not None:
            while len(tags) > 0:
                try:
                    tmptags = tags.pop(0)
                    quiz.tag.append(tmptags)
                except KeyError:
                    pass
        quiz.save()
        returnmsg = 'QUIZ ADD OK id='+ quiz.id
    return HttpResponse(returnmsg)

def main():
    #f = open('quiz.xml')
    qp = QuizParser(fromstring(f.read()).find('quiz'))

    print qp.GetCreator()
    print qp.GetInfoDict()
    print qp.GetDescription()
    print qp.GetAttachmentList()
    print qp.GetCorrectAnswerList()
    print qp.GetWrongAnswerList()
    print qp.GetManualDifficulty()
    print qp.GetAutoDifficulty()
    print qp.GetTagList()

if __name__ == '__main__':
    main()