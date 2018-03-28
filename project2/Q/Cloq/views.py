from django.shortcuts import render_to_response
from django.shortcuts import render

from Cloq.globalvars import *

from datetime import date

# Create your views here.

from .models import *

# Jane does these pages
def dash(request):
    # current_user = user.objects.all()[0]
    announcements = announcement.objects.all()
    today_times = getTodaysSchedule()
    today_users = list()

    for today_time in today_times:
        today_users.append((user.objects.filter(uid=today_time.uid)[0].firstname,
                            user.objects.filter(uid=today_time.uid)[0].lastname,
                            today_time.uid,
                            today_time.start.time,
                            today_time.end.time))
    return render(
        request,
        'catalog/user_dash.html',
        context={**{'announcements': announcements,
                      'today_sched': today_times,
                      'today_users': today_users},
                   **template()}
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
            # print(user.objects.filter(uid=uid_obj)[0], " is ", uid_obj)
            working.append(uid_obj)
    return list(map(lambda x: user.objects.filter(uid=x)[0], working))

def is_working(uid_obj):
    for time_obj in time.objects.filter(uid=uid_obj).order_by('start').reverse():
        if time_obj.timetype == PUNCH_OUT:
            # print(time_obj.uid, " is not working")
            return False
        elif time_obj.timetype == PUNCH_IN:
            # print(uid_obj, " is working")
            return True
        # print(uid_obj, " has timetype ", time_obj.timetype)

    # print(time_obj.uid, " is not working")
    return False

def getTodaysSchedule():
    return time.objects.filter(timetype=SHIFT).\
        filter(start__date=date(year=2018, month=4, day=2)).\
        order_by('start')




