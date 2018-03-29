from django.shortcuts import render_to_response
from django.shortcuts import render

from Cloq.globalvars import *

from datetime import date
from datetime import timedelta

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

def schedule(request):
    from_date = get_date()  # this has to update somehow??
    date_format = "%A, %B %w %Y"
    from_date_str = from_date.strftime(date_format)

    return render(
        request,
        'catalog/schedule.html',
        context={**{'week_sched': get_week_schedule(from_date),
                    'week_start_day': from_date_str},
                 **template()}
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

# Helper methods
def get_current_user():
    # gets the first user right now
    return user.objects.all()[3]

def get_date():
    # right now just gets from the week that we have set up in data
    return date(year=2018, month=4, day=2)

def get_week(convert_date: datetime):
    return convert_date.date().isocalendar()[1]

def template():
    current_user = get_current_user()
    return {"current_user": current_user, 'working': get_current_working(),
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
        filter(start__date=get_date()).\
        order_by('start')

def get_week_schedule(start_date):
    sched_objs = list()
    end_of_week = start_date + timedelta(days=7)
    for time_obj in time.objects.filter(timetype=SHIFT).filter(start__gt=start_date).filter(start__lt=end_of_week).order_by('start'):
        # .filter(start__lt=(get_date()+datetime.timedelta(days=7))
        # this is a stupid tuple. Template parsing is not impressive.
        sched_objs.append( (user.objects.filter(uid=time_obj.uid)[0].firstname, user.objects.filter(uid=time_obj.uid)[0].lastname, time_obj.start, time_obj.end, time_obj.start.strftime("%A"), time_obj.end.strftime("%A")) )
    return sched_objs


