__author__ = 'bxshi'
from hashlib import md5
from datetime import datetime
from django.http import HttpResponse
from Crypto.PublicKey import RSA
from Crypto import Random
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring
from django.utils.encoding import smart_str, smart_unicode, force_unicode

from database.quiz import *
from database.login import Login

class QuizParser():
    """Parse quiz xml in <quiz></quiz>

    """
    xml = None
    infolist = {}.fromkeys(('type', 'choose', 'order', 'selection number'))

    def __init__(self, quizxml=''):
        """init it, load xml

            Args:
                quizxml:   XML Element, *not string*

        """
        self.xml = quizxml

    def GetQuizInfo(self):
        """get nested xml of quiz info

            Returns:
                XML Element

        """
        return self.xml.find('quiz_info')

    def GetCreator(self):
        """return creator of this quiz

            Returns:
                String

        """
        return self.xml.find('creator').text

    def GetDescription(self):
        """return description of this quiz

            Returns:
                String

        """
        return self.xml.find('description').text

    def GetAttachments(self):
        """return nested xml elements of attachments

            Returns:
                Element

        """
        return self.xml.find('attachments')

    def GetCorrectAnswers(self):
        """return nested xml elements of correct answer

            Returns:
                Element

        """
        return self.xml.find('correct_answer')

    def GetWrongAnswers(self):
        """return nested xml elements of wrong answer

            Returns:
                Element

        """
        return self.xml.find('wrong_answer')

    def GetManualDifficulty(self):
        """return manual difficulty of this quiz

            Returns:
                String, if use it as a int, use int()

        """
        return self.xml.find('manual_difficulty').text

    def GetAutoDifficulty(self):
        """return auto difficulty of this quiz

            Returns:
                Strings, if use it as a int, use int()

        """
        return self.xml.find('auto_difficulty').text

    def GetTags(self):
        """return nested xml elements of tags

            Returns:
                Element

        """
        return self.xml.find('tags')

    def GetInfoType(self):
        """return element of info -> type

            Returns:
                Element

        """
        quizinfo = self.GetQuizInfo()
        if quizinfo is not None:
            return quizinfo.find('type')
        else:
            return None

    def GetInfoChoose(self):
        """return element of info -> choose

            Returns:
                Element

        """
        quizinfo = self.GetQuizInfo()
        if quizinfo is not None:
            return quizinfo.find('choose')
        else:
            return None

    def GetInfoOrder(self):
        """return element of info -> order

            Returns:
                Element

        """
        quizinfo = self.GetQuizInfo()
        if quizinfo is not None:
            return quizinfo.find('order')
        else:
            return None

    def GetSelectionNumber(self):
        """return element of info ->selection number

            Returns:
                Element

        """
        quizinfo = self.GetQuizInfo()
        if quizinfo is not None:
            return quizinfo.find('selection_number')
        else:
            return None

    def GetInfoDict(self):
        """return a dict of info

            Returns:
                ['type']:    info -> type

                ['choose']:  info -> choose

                ['order']:   info -> order

                ['selection number']:    info->selection_number

        """
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
        """return a list of attachments

            Returns:
                each list element contains:
                    [description]:  attachment -> description

                    [file]: attachment -> file


        """
        attachments = self.GetAttachments()
        attachmentlist = list()
        if attachments is None:
            return None

        attachmentelementlist = attachments.findall('attachment')
        if len(attachmentelementlist) > 0:
            while len(attachmentelementlist) > 0:
                attachmentdict=dict()
                tmpelement = attachmentelementlist.pop(0)
                if tmpelement.find('description') is not None:
                    attachmentdict['description'] = tmpelement.find('description').text
                if tmpelement.find('file') is not None:
                    attachmentdict['file']  =   tmpelement.find('file').text
                attachmentlist.append(attachmentdict)
        else:
            return None

        return attachmentlist

    def GetCorrectAnswerList(self):
        """return correct answer list

            Returns:
                each element contains:
                    [id]:   answer -> id

                    [string]: answer -> string

                    [attach]:   answer -> attach

        """
        answers = self.GetCorrectAnswers()
        answerlist = list()
        if answers is None:
            return None

        answerelementlist = answers.findall('answer')
        if  len(answerelementlist) > 0:
            while len(answerelementlist) > 0:
                tmpanswer = answerelementlist.pop(0)
                answerdict = dict()
                if tmpanswer.find('id') is not None:
                    answerdict['id'] = tmpanswer.find('id').text
                if tmpanswer.find('string') is not None:
                    answerdict['string'] = tmpanswer.find('string').text
                if tmpanswer.find('attach') is not None:
                    answerdict['attach']= tmpanswer.find('attach').text
                answerlist.append(answerdict)
        else:
            return None

        return answerlist

    def GetWrongAnswerList(self):
        """return wrong answer list

            Returns:
                each element contains:
                    [id]:   answer -> id

                    [string]: answer -> string

                    [attach]:   answer -> attach

        """
        answers = self.GetWrongAnswers()
        answerlist = list()
        if answers is None:
            return None

        answerelementlist = answers.findall('answer')
        if  len(answerelementlist) > 0:
            while len(answerelementlist) > 0:
                tmpanswer = answerelementlist.pop(0)
                answerdict = dict()
                if tmpanswer.find('id') is not None:
                    answerdict['id'] = tmpanswer.find('id').text
                if tmpanswer.find('string') is not None:
                    answerdict['string'] = tmpanswer.find('string').text
                if tmpanswer.find('attach') is not None:
                    answerdict['attach']= tmpanswer.find('attach').text
                if len(tmpanswer) > 0:
                    answerlist.append(answerdict)
        else:
            return None

        return answerlist

    def GetTagList(self):
        """return a list of tags

            Returns:
                list contains strings of each tag

        """
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

def QuizInsert(request, xml=''):
    """insert quiz into database

        Args:
            xmlstr: A xml string, the root label is root, and each quiz is enclosed by <quiz></quiz> label

        Returns:
            ERR UNKNOWN:    unknown error
            XML EPT:        xml is empty
            QUIZ ADD OK, id=%d  %d represent for id in database

    """
    returnmsg = 'ERR UNKNOWN'

    if request.method == 'GET':
        return HttpResponse('NO GET METHOD')
    if request.method == 'POST':
        xml=smart_str(request.POST.get('xml',''))

    if xml == '':
        returnmsg = "XML EPT"
    else:
        #try:
        #xml = str(xml).decode()
        #xml = str(xml).encode('UTF-8')
        quizxml = fromstring(xml)
        #except:
        #    return HttpResponse("XML ERR")
        quizall = quizxml.findall('quiz')
        while len(quizall) > 0:
            qp = QuizParser(quizall.pop(0))
            username = Login.objects(session=request.session.session_key).first()
            quiz = Quiz(creator=username.username, description=qp.GetDescription(), manualdifficulty=float(qp.GetManualDifficulty()))
            info = qp.GetInfoDict()

            #fill quiz info
            if info is not None:
                try:
                    if info['type'] is not None:
                        quiz.info.append(QuizInfo(type='type', description=info['type']))
                        quiz.type = int(info['type'])
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
                        quiz.info.append(QuizInfo(type='selection_number', description=info['selection number']))
                except KeyError:
                    pass

            #fill quiz attachments

            attch = qp.GetAttachmentList()
            if attch is not None:
                for tmpattch in attch:
                    try:
                        quiz.attachment.append(QuizAttach(description=tmpattch['description'], file=tmpattch['file']))
                    except KeyError:
                        pass

            #fill answers

            answer = qp.GetCorrectAnswerList()
            if answer is not None:
                while len(answer) > 0:
                    try:
                        tmpanswer = answer.pop(0)
                        quiz.correctanswer.append(QuizAnswer(answer=tmpanswer['string'],attach=tmpanswer['attach']))
                    except KeyError:
                        pass

            answer = qp.GetWrongAnswerList()
            if answer is not None:
                 while len(answer) > 0:
                    try:
                        tmpanswer = answer.pop(0)
                        quiz.wronganswer.append(QuizAnswer(answer=tmpanswer['string'],attach=tmpanswer['attach']))
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
            returnmsg = 'QUIZ ADD OK id='+ str(quiz.id)
    return HttpResponse(returnmsg)

def QuizGet(request, elementlimit=-1, qid=None, type="-1"):
    """get quiz

        Args:
            request:    Django default parameter

            elementlimit:   -1 for unlimited, other positive number is the max element client wants to retrive

        Returns:
            XML file, the example could be seen in ../samples/quiz.xml

    """

    if request.method == 'POST':
        elementlimit = int(request.POST.get('elementlimit', ''))

    username = Login.objects(session=request.session.session_key).first()

    xml = Element("root")
    i = 0
    if qid is not None:
        quizset = Quiz.objects(id=qid, creator=username.username)
    elif type == "-1":
        quizset = Quiz.objects(creator=username.username)
    else:
        quizset = Quiz.objects(creator=username.username, type=int(type))
    for quiz in quizset:
        xmlquiz = Element('quiz')
        SubElement(xmlquiz, 'creator').text = smart_unicode(quiz.creator)
        SubElement(xmlquiz, 'id').text = smart_unicode(str(quiz.id))

        quiz_info = Element('quiz_info')
        while len(quiz.info) > 0:
            quizinfo = quiz.info.pop(0)
            try:
                SubElement(quiz_info, smart_str(quizinfo.type)).text = smart_unicode(quizinfo.description)
            except KeyError:
                pass

        xmlquiz.append(quiz_info)

        SubElement(xmlquiz, 'description').text = smart_unicode(quiz.description)

        attachments = Element('attachments')
        SubElement(xmlquiz,"attnum").text = str(len(quiz.attachment))
        for attach in quiz.attachment:
            xmlatt = Element("attachment")
            SubElement(xmlatt, "description").text = smart_unicode(attach.description)
            SubElement(xmlatt, "file").text = smart_unicode(attach.file)
            attachments.append(xmlatt)
        xmlquiz.append(attachments)

        correct_answer = Element('correct_answer')
        for answer in quiz.correctanswer:
            xmlans = Element('answer')
            SubElement(xmlans, 'string').text = smart_unicode(answer.answer)
            SubElement(xmlans, 'attach').text = smart_unicode(answer.attach)
            correct_answer.append(xmlans)
        xmlquiz.append(correct_answer)

        wrong_answer = Element('wrong_answer')
        for answer in quiz.wronganswer:
            xmlans = Element('answer')
            SubElement(xmlans, 'string').text = smart_unicode(answer.answer)
            SubElement(xmlans, 'attach').text = smart_unicode(answer.attach)
            wrong_answer.append(xmlans)
        xmlquiz.append(wrong_answer)

        SubElement(xmlquiz, 'manual_difficulty').text = smart_unicode(quiz.manualdifficulty)
        SubElement(xmlquiz, 'auto_difficulty').text = smart_unicode(quiz.autodifficulty)

        tags = Element('tags')
        while len(quiz.tag) > 0:
            tag = quiz.tag.pop(0)
            SubElement(tags, 'tag').text = smart_unicode(tag)
        xmlquiz.append(tags)

        xml.append(xmlquiz)

        i += 1
        if elementlimit != -1 and i >= elementlimit:
            break

    return HttpResponse(smart_unicode(tostring(xml,encoding='UTF-8')),content_type='text/xml')

def QuizDel(request, qid=None):
    returnmsg = None
    if request.method == 'POST':
        qid = request.POST.get('qid', '')

    if qid is not None:
        quiz = Quiz.objects(id=qid)
        returnmsg = quiz.delete()
    else:
        returnmsg = "QID ERR"
    return HttpResponse(returnmsg)

def QuizEdit(request, xmlstr='', qid=None):
    returnmsg = None

    if request.method == 'POST':
        qid = request.POST.get('qid','')
    else:
        returnmsg = 'GET NOT SUPPORT'
    if qid is None:
        returnmsg = 'ID EPT'
    else:
        quiz = Quiz.objects(id=qid)
        quiz.delete()
        QuizInsert(request, xmlstr=xmlstr)
    return HttpResponse(returnmsg)

def main():
    """test for QuizParser

    """
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