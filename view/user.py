__author__ = 'bxshi'
from hashlib import md5
from datetime import datetime
from django.http import HttpResponse
from Crypto.PublicKey import RSA
from Crypto import Random
from xml.etree.ElementTree import Element, SubElement, tostring
from django.utils.encoding import smart_str, smart_unicode

from database.user import *
from database.login import *

def UserRegister(request, username='', password=''):

    """Register Function.

     Args:
          request:  Default

          username: In URL or in POST, var name is username

          password: In URL or in POST, var name is password

     Return:
          USR LEN:  Username or password is too long

          REG OK:   Register ok

          USR DUP:  Already has that username in database

          USR EPT:  Username or password is empty

    """

    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')

    if username != '' and password != '' :
        if len(username) > 20:
            returnmsg = 'USR LEN'
        else:
            password = md5(password).hexdigest()
            #check username exists
            check = User.objects(username=username).count()
            if not check:

                rng = Random.new().read
                RSAkey = RSA.generate(1024, rng)

                newuser = User(username=username,password=password,publickey=RSAkey.publickey().exportKey(), privatekey=RSAkey.exportKey())
                newuser.save()
                returnmsg = 'REG OK'
            else:
                returnmsg = 'USR DUP'
    else:
        returnmsg = 'USR EPT'

    return HttpResponse(returnmsg)

def UserLogin(request, username='', password=''):

    """Login Function.

    Args:
          request:  Default

          username: In URL or in POST, var name is username

          password: In URL or in POST, var name is password

    Return:
          USR LEN:  Username or password is too long

          LOG OK:   Login ok

          LOG ERR:  Login error, do not show if username error or password
                    error for security reason
          USR EPT:  Username or password is empty

    """

    returnmsg = 'LOG UNKNOWN'

    if request.method == 'POST':
        username = smart_str(request.POST.get('username',''))
        password = smart_str(request.POST.get('password',''))

    if username != '' and password != '':
        if len(username) > 20:
            returnmsg = 'USR LEN'
        else:
            password = md5(password).hexdigest()
            user_exist = User.objects(username=username)
            if not user_exist:  #if the list is empty
                returnmsg = 'LOG ERR'
            else:
                for user in User.objects(username=username):
                    if user.password == password:
                        returnmsg = 'LOG OK'

                        #add session information(just a dumb, try to make sessionid appear)
                        request.session['sid'] = md5(username).hexdigest()
                        login_exist = Login.objects(username=username)
                        if login_exist:
                            login_exist.delete()
                        login = Login(session=request.session.session_key, username=username)
                        login.save()
                        user.log.append(UserLog(time=datetime.now(), ip=request.META['REMOTE_ADDR'], login=True))
                        user.save()
                    else:
                        returnmsg = 'LOG ERR'
                        user.log.append(UserLog(time=datetime.now(), ip=request.META['REMOTE_ADDR'], login=False))
                        user.save()
    else:
        returnmsg = 'USR EPT'

    return HttpResponse(returnmsg)

def UserLogout(request):

    """User logout function

    Args:
            request:    Default
    Returns:
            USR NOTLOG: Not login

            USR LOGOUT: Logout

    """
    returnmsg = "USR UNKNOWN"
    if request.session.session_key is None:
        returnmsg = "USR NOTLOG"
    else:
        login_exist = Login.objects(session=request.session.session_key)
        if not login_exist:  #if the list is empty
            returnmsg = 'USR NOTLOG'

        else:
            login_exist.delete()
            returnmsg = "USR LOGOUT"
            for key in request.session.keys():
                try:
                    del request.session[key]
                except KeyError:
                    returnmsg = 'USR NOTLOG'

    return HttpResponse(returnmsg)

def UserGetPublicKey(request):
    """get pulickey

        Returns:
            RSA public key

    """

    username = Login.objects(session=request.session.session_key).first()
    keypair = User.objects(username=username.username).first()

    pub = keypair.publickey

    if pub is not None:
        return HttpResponse(pub, mimetype="text/plain")
    else:
        return HttpResponse('GET ERR')


def UserGetPrivateKey(request):

    """Send privatekey to client, after first call of this function, server will delete private key from database

        Returns:
            RSA private key
    """
    username = smart_str(Login.objects(session=request.session.session_key).first())
    keypair = smart_str(User.objects(username=username.username).first())

    pri = keypair.privatekey

    if pri is not None:
        keypair.privatekey = "KEY NULL"
        keypair.save()
        return HttpResponse(pri, mimetype="text/plain")
    else:
        return HttpResponse('GET ERR')

def UserLoginCheck(view):

    """used for redirect other pages, check login status first

    """
    def newview(request, *args, **kwargs):
        login_exist = Login.objects(session=request.session.session_key)
        if not login_exist:  #if the list is empty
            return HttpResponse("USR NOTLOG")
        return view(request, *args, **kwargs)
    return newview

def UserLogCheck(request, loglimit='25'):

    """Output login logs for user in xml

        Args:
            request:    Django default element

            loglimit:   default 25, the max element number client wants retrieve

        Returns:
            XMl files

    """
    username = Login.objects(session=request.session.session_key).first()
    user = User.objects(username=username.username).first()

    xmlogs = Element("logs")

    i=1
    for log in reversed(user.log):

        xmlog = Element('log')
        SubElement(xmlog, "year").text = str(log.time.year)
        SubElement(xmlog, "month").text = str(log.time.month)
        SubElement(xmlog, "day").text = str(log.time.day)
        SubElement(xmlog, "hour").text = str(log.time.hour)
        SubElement(xmlog, "minute").text = str(log.time.minute)
        SubElement(xmlog, "second").text = str(log.time.second)
        SubElement(xmlog, "ip").text = str(log.ip)
        SubElement(xmlog, "login").text = str(log.login)

        xmlogs.append(xmlog)

        i+=1
        if i > int(loglimit) :
            break

    return HttpResponse(tostring(xmlogs,encoding='UTF-8'),content_type='text/xml')
