from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from view.user import UserRegister
from view.user import UserLogin
from view.user import UserLogout
from view.user import UserGetPublicKey
from view.user import UserGetPrivateKey
from view.user import UserLoginCheck
from view.user import UserLogCheck

from view.quiz import QuizInsert
from view.quiz import QuizGet
from view.quiz import QuizEdit
from view.quiz import QuizDel

from view.welcome import Welcome

urlpatterns = patterns('',



    # register
    (r'^register/(?P<username>[^/]+)/(?P<password>[^/]+)/$', UserRegister),
    (r'^register/$', UserRegister),

    # login/out
    (r'^login/(?P<username>[^/]+)/(?P<password>[^/]+)/$', UserLogin),
    (r'^login/$', UserLogin),
    (r'^logout/$', UserLogout),

    # RSA keys
    (r'^login/getpublickey/$', UserLoginCheck(UserGetPublicKey)),
    (r'^login/getprivatekey/$', UserLoginCheck(UserGetPrivateKey)),

    # login log
    (r'^logcheck/$', UserLoginCheck(UserLogCheck)),
    (r'^logcheck/(?P<loglimit>[0-9]+)/$', UserLoginCheck(UserLogCheck)),

    #quiz
    (r'^quiz/insert/$', UserLoginCheck(QuizInsert)),
    (r'^quiz/edit/$', UserLoginCheck(QuizEdit)),
    (r'^quiz/get/$', UserLoginCheck(QuizGet)),
    (r'^quiz/getbytype/(?P<type>[0-9])/$', UserLoginCheck(QuizGet)),
    (r'^quiz/get/(?P<elementlimit>[0-9]+)/$', UserLoginCheck(QuizGet)),
    (r'^quiz/get/(?P<qid>[^/]+)/$', UserLoginCheck(QuizGet)),
    (r'quiz/del/$', UserLoginCheck(QuizDel)),

    #index
    #(r'', Welcome),

    # Examples:
    # url(r'^$', 'ptl.views.home', name='home'),
    # url(r'^ptl/', include('ptl.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
