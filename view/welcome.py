from django.template.loader import get_template

__author__ = 'bxshi'

from django.http import HttpResponseRedirect

def Welcome(request):
    return HttpResponseRedirect('/static/index.html')