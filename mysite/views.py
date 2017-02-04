# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404, HttpResponse
import datetime
import time
def home(request):
    return HttpResponse("This is Home Page")

def times(request):
    now = datetime.datetime.now()
    now1 = time.asctime( time.localtime() )
    now2 = time.strftime("%Y-%m-%d %X", time.localtime())
    html = "<html><body>It is now %s-----%s----%s.</body></html>" % (now,now1,now2)
    return HttpResponse(html)

def hours_ahead(request, offset=1):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)
