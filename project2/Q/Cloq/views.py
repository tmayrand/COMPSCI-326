from django.shortcuts import render_to_response
from django.shortcuts import render

from Cloq.globalvars import *

# Create your views here.

from .models import *

# Jane does these pages
def dash(request):
    current_user = user.objects.all()[0]
    announcements = announcement.objects.all()
    return render(
        request,
        'catalog/user_dash.html',
        context = {**{'announcements': announcements}, **template()}
    )

def admin_dash(request):
    return render(
        request,
        'catalog/admin_dash.html',
        context={}
    )

def schedule(request):
    return render(
        request,
        'catalog/schedule.html',
        context={}
    )


# Shane does these pages
# Note: Make sure they have the css pages they need. Sometimes there are special css pages.
# Lmk. the css for dash is implicitly included

def admin_schedule(request):
    return render(
        request,
        'catalog/admin_schedule.html',
        context={}
    )

def settings(request):
    return render(
        request,
        'catalog/user_settings.html',
        context={}
    )

def availability(request):
    return render(
        request,
        'catalog/availability.html',
        context={}
    )

def template():
    current_user = user.objects.all()[0]
    times = time.objects.all()[0]

    return {"current_user": current_user, 'working': getCurrentWorking()}

def getCurrentWorking():
    working = list()
    uids = set()
    for time_obj in time.objects.all():
        uids.add(time_obj.uid)
    for uid_obj in uids:
        if is_working(uid_obj):
            print(uid_obj, " is working")
            working.append(uid_obj)
    return list(map(lambda x: user.objects.filter(uid=x)[0], working))

def is_working(uid_obj):
    for time_obj in time.objects.filter(uid=uid_obj).order_by('start').reverse():
        if time_obj.timetype == PUNCH_OUT:
            print(time_obj.uid, " is not working")
            return False
        elif time_obj.timetype == PUNCH_IN:
            return True
    print(time_obj.uid, " is not working")
    return False






