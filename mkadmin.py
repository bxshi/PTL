__author__ = 'bxshi'
#!/usr/bin/env python
from wsgi import *
from django.contrib.auth.models import User
u, created = User.objects.get_or_create(username='ptl')
if created:
    u.set_password('ptlserver')
    u.is_superuser = True
    u.is_staff = True
    u.save()