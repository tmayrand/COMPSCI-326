from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib.auth import (login as auth_login,  authenticate)
from django.contrib.auth import logout
from django.shortcuts import redirect

from Cloq.globalvars import *

from datetime import date
from datetime import timedelta
from datetime import time
from datetime import datetime as dt

# Create your views here.

from .models import *

# Jane does these pages
def dash(request):
    if not request.user.is_authenticated:
        return redirect("login")
    popup = False
    popupdata = ""
    if request.method == 'POST':
        clock_type = request.POST['clocktype'] #"in" if clock in, "out" if clock out

        if clock_type== 'in':
            popup = True
            popupdata = "Clocked In!"
            print("clockin %s", request.user.username)
            NewTime = time(timetype=PUNCH_IN, start=datetime.now(), end=datetime.now(), uid=get_current_user(request).uid)
            NewTime.save()

        elif request.POST == 'out':
            popup = True
            popupdata = "Clocked Out!"
            print("clockout %s", request.user.username)
            NewTime = time(timetype=PUNCH_OUT, start=datetime.now(), end=datetime.now(), uid=get_current_user(request).uid)
            NewTime.save()
        else:
            return redirect("login")




    # current_user = get_current_user(request)
    #print(get_current_user().usertype)
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
                      'today_users': today_users,
                    'popup':popup,
                    'popupdata':popupdata},
                   **template(request)}
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
                 **template(request)}
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
                 **template(request)}
    )


# Shane does these pages
# Note: Make sure they have the css pages they need. Sometimes there are special css pages.
# Lmk. the css for dash is implicitly included

def admin_schedule(request):
    return render(
        request,
        'catalog/admin_schedule.html',
        context={**{'week_sched': get_week_schedule_by_user()},
                 **template(request)}
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

# Troy - Views for login/logout pages
def login(request):
    if request.user.is_authenticated:
        return redirect("dash")
    _message = 'Please sign in'
    if request.method == 'POST':
        _username = request.POST['username']
        _password = request.POST['password']
        xuser = authenticate(username=_username, password=_password)
        if xuser is not None:
            if xuser.is_active:
                try:
                    dbuser = user.objects.get(username=_username)
                except:
                    return render(request, 'catalog/login.html', {'message': 'No account exists.'})
                auth_login(request, xuser)
                return redirect('dash')
            else:
                _message = 'Your account is not activated'
        else:
            _message = 'Invalid login, please try again.'
    context = {'message': _message}
    return render(request, 'catalog/login.html', context)
    #return render(request, 'catalog/user_dash.html', context)

def logout(request):
    return render(
                  request,
                  'catalog/logout.html',
                  context={}
                  )

# Helper methods
def get_current_user(request):
    if request.user.is_authenticated:
        try:
            return user.objects.get(username=request.user.username)
        except:
            try:
                return User.objects.get(username=request.user.username)
            except:
                return None
            return None
    else:
        return None

def get_date(year_num:int, month_num:int, day_num:int):

    return date(year=year_num, month=month_num, day=day_num)

def get_week(convert_date: datetime):
    return convert_date.date().isocalendar()[1]  # EDIT HERE TO CHANGE USER AND SEE DIFFERENT VIEWS

def template(request):
    current_user = get_current_user(request)
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
