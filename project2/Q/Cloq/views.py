from django.shortcuts import render_to_response
from django.shortcuts import render

from Cloq.globalvars import *

from datetime import date
from datetime import timedelta
from datetime import time
from datetime import datetime as dt

# Create your views here.

from .models import *

# Jane does these pages
def dash(request):
    # current_user = user.objects.all()[0]
    print(get_current_user().usertype)
    announcements = announcement.objects.all()
    today_times = get_todays_schedule()
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
    announcements = announcement.objects.all()
    today_times = get_todays_schedule()
    today_users = list()
    for today_time in today_times:
        today_users.append((user.objects.filter(uid=today_time.uid)[0].firstname,
                            user.objects.filter(uid=today_time.uid)[0].lastname,
                            today_time.uid,
                            today_time.start.time,
                            today_time.end.time))
    return render(
        request,
        'catalog/admin_dash.html',
        context={**{'announcements': announcements,
                    'today_sched': today_times,
                    'today_users': today_users},
                 **template()}
    )

def schedule(request, year, month, day):
    from_date = get_date(year, month, day)  # this has to update somehow??
    date_format = "%A, %B %d %Y"
    from_date_str = from_date.strftime(date_format)
    to_date = get_date(year, month, day) + timedelta(days=7)
    previous_week = get_date(year, month, day) - timedelta(days=7)
    return render(
        request,
        'catalog/schedule.html',
        context={**{'week_sched': get_week_schedule(from_date),
                    'week_start_day': from_date_str,
                    'week_end_day': to_date,
                    'previous_week': previous_week},
                 **template()}
    )


# Shane does these pages
# Note: Make sure they have the css pages they need. Sometimes there are special css pages.
# Lmk. the css for dash is implicitly included

def admin_schedule(request):
    return render(
        request,
        'catalog/admin_schedule.html',
        context={**{'week_sched': get_week_schedule_by_user()},
                 **template()}
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

def login(request):
    return render(
                  request,
                  'catalog/login.html',
                  context={}
                  )

def logout(request):
    return render(
                  request,
                  'catalog/logout.html',
                  context={}
                  )

# Helper methods
def get_current_user():
    # gets the first user right now
    return user.objects.all()[3]

def get_date(year_num:int, month_num:int, day_num:int):

    return date(year=year_num, month=month_num, day=day_num)

def get_week(convert_date: datetime):
    return convert_date.date().isocalendar()[1]  # EDIT HERE TO CHANGE USER AND SEE DIFFERENT VIEWS

def template():
    current_user = get_current_user()
    return {'current_user': current_user, 'working': get_current_working(),
            'current_day': date(year=2018, month=4, day=2),  # right now just gets from the week that we have set up in data
            'USER': USER, 'ADMIN': ADMIN,
            'OVERTIME': OVERTIME, 'NO_OVERTIME': NO_OVERTIME,
            'ALL_VIEW': ALL_VIEW, 'ADMIN_VIEW': ADMIN_VIEW,
            'PUNCH_IN': PUNCH_IN, 'PUNCH_OUT': PUNCH_OUT, 'SHIFT': SHIFT, 'UNAVAILABLE': UNAVAILABLE, 'REQUEST': REQUEST}

def get_current_working():
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

def get_todays_schedule():
    return time.objects.filter(timetype=SHIFT).\
        filter(start__date=get_date(2018, 4, 2)).\
        order_by('start')

def get_week_schedule(start_date):
    sched_objs = list()
    end_of_week = get_date(2018, 4, 2) + timedelta(days=7)
    for time_obj in time.objects.filter(timetype=SHIFT) \
    .filter(start__gt=get_date(2018, 4, 2)) \
    .filter(start__lt=end_of_week) \
    .order_by('uid'):
        # .filter(start__lt=(get_date()+datetime.timedelta(days=7))
        # this is a stupid tuple. Template parsing is not impressive.
        sched_objs.append( (user.objects.filter(uid=time_obj.uid)[0].firstname, \
                            user.objects.filter(uid=time_obj.uid)[0].lastname, \
                            time_obj.start, time_obj.end, time_obj.start.strftime("%A"), \
                            time_obj.end.strftime("%A")) )
    return sched_objs

def time_subtract(start, finish):
    d =finish - start
    d = (d.seconds)/(7*3600)*100
    return d

def get_week_schedule_by_user():
    user_scheds = []
    end_of_week = get_date(2018, 4, 2) + timedelta(days=7)
    for user_obj in user.objects.order_by('uid'):
        sched = [t for t in time.objects
                 .filter(start__date = get_date(2018, 4, 2))
                 .filter(timetype = SHIFT)
                 .filter(start__gt = get_date(2018, 4, 2))
                 .filter(start__lt = end_of_week)
                 .filter(uid = user_obj.uid)
                 .order_by('start')]
        bar_lengths = []
        if sched:
            last_t = dt(2016, 4,2,9,5,0,0,sched[0].start.tzinfo)
            for t in sched:
                bar_lengths.append([t, time_subtract(last_t, t.start),
                                    time_subtract(t.start,t.end)])
                last_t = t.end
        user_stuff = [user_obj.firstname,
        user_obj.lastname,
                      bar_lengths]
        user_scheds.append(user_stuff)
    return user_scheds
