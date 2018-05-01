from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib.auth import (login as auth_login,  authenticate)
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.db.models import Q
from django.db.models import *
from django.contrib.auth.hashers import make_password
from Cloq.globalvars import *

from datetime import date
from datetime import timedelta
from datetime import time as tm
from datetime import datetime as dt

# Create your views here.
from .forms import *
from .models import *

# Jane does these pages
def dash(request):
    if (not request.user.is_authenticated) or get_current_user(request) == None:
        return redirect("login")
    popup = False
    popupdata = "" 
    punch_status = ""

    last_name = request.user.username[1:].capitalize()
    current_worker = user.objects.all().filter(Q(lastname=last_name))[0]
    time_shift = time.objects.all().filter(Q(uid=current_worker.uid), Q(timetype=1) | Q(timetype=2)).order_by("-tid")
    if len(time_shift) == 0:
      punch_status = "clocked out"
    elif time_shift[0].timetype == 1:
      punch_status = "clocked in"
    else: 
      punch_status = "clocked out"
     


    if request.method == 'POST':
        #current_user = user.objects.filter(username=get_current_user(request).username)[0]
        current_user = get_current_user(request)
        # clock_type = request.POST['clocktype'] #"in" if clock in, "out" if clock out

        if request.POST.get("clocktype", "") == 'in':
            popup = True
            popupdata = "Clocked In!"
            punch_status = "clocked in"
            print("clockin ", current_user.username)
            NewTime = time(timetype=PUNCH_IN, start=datetime.now(), end=datetime.now(), uid=current_user.uid)
            NewTime.save()

        elif request.POST.get("clocktype", "") == 'out':
            popup = True
            popupdata = "Clocked Out!"
            punch_status = "clocked out"
            print("clockout ", current_user.username)
            NewTime = time(timetype=PUNCH_OUT, start=datetime.now(), end=datetime.now(), uid=current_user.uid)
            NewTime.save()
        else:
            return redirect("logout")

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
                    'popup': popup,
                    'popupdata': popupdata,
                    'punch_status': punch_status},
                    **template(request)}
    )

def admin_dash(request):
    if (not request.user.is_authenticated) or get_current_user(request) == None:
        return redirect("login")
    last_name = request.user.username[1:].capitalize()
    current_worker = user.objects.all().filter(Q(lastname=last_name))[0]
    usertype = ""
    if current_worker.usertype == 1:
      return redirect("dash")
    if request.method == "POST":
      if request.POST.get('usertype') == "Admins Only":
        usertype = 2
      else:
        usertype = 1
      post_copy = request.POST.copy()
      post_copy["usertype"] = usertype;
      form = annoucementsForm(post_copy)
      if form.is_valid():
        form.save()
        return redirect('admin_dash')
      

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
    if (not request.user.is_authenticated) or get_current_user(request) == None:
        return redirect("login")
    from_date = get_date(year, month, day)  # this has to update somehow??
    date_format = "%A, %B %d %Y"
    from_date_str = from_date.strftime(date_format)
    to_date = get_date(year, month, day) + timedelta(days=7)
    previous_week = get_date(year, month, day) - timedelta(days=7)
    return render(
        request,
        'catalog/schedule.html',
        context={**{'week_sched': get_week_schedule(from_date, get_current_user(request)),
                    'week_start_day': from_date_str,
                    'week_end_day': to_date,
                    'previous_week': previous_week},
                 **template(request)}
    )


# Shane does these pages
# Note: Make sure they have the css pages they need. Sometimes there are special css pages.
# Lmk. the css for dash is implicitly included

def admin_schedule(request, year, month, day):
    if (not request.user.is_authenticated) or get_current_user(request) == None:
        return redirect("login")
    date = get_date(year, month, day)  # this has to update somehow??
    date_format = "%A, %B %d %Y"
    date_str = date.strftime(date_format)
    previous_date = get_date(year, month, day) - timedelta(days=1)
    next_date = get_date(year, month, day) + timedelta(days=1)
    return render(
        request,
        'catalog/admin_schedule.html',
        context={**{'day_sched': get_day_schedule_by_user(date),
                    'day': date_str,
                    'yesterday': previous_date,
                    'tomorrow': next_date},
                 **template(request)}
    )

def settings(request):
    if (not request.user.is_authenticated) or get_current_user(request) == None:
        return redirect("login")
    curuser = get_current_user(request)
    request.POST._mutable = True
    passWarning = "none"
    passSuccess = "none"
    if "password" in request.POST:
        if request.POST["password"] == '':
            request.POST["password"] = curuser.password
        else:
            if request.POST["password"] == request.POST["cpassword"]:
                request.POST["password"] = make_password(request.POST["password"])
                passSuccess = "inherit"
            else:
                passWarning = "inherit"
    if "username" in request.POST:
        request.POST["username"] = curuser.username
    form = settingsForm(request.POST or None, instance=curuser)
    if form.is_valid():
        form.save()
    ot = "checked"
    notot = ""
    notif = "checked"
    if(not curuser.overtime):
        ot = ""
        notot = "checked"
    if(not curuser.notification):
        notif = ""
    return render(
        request,
        'catalog/user_settings.html',
        context={**{'firstname': curuser.firstname,
            'lastname': curuser.lastname,
            'username': curuser.username,
            'email': curuser.email,
            'pronoun': curuser.pronoun,
            'phone': curuser.phone,
            'overtime': ot,
            'notovertime': notot,
            'notification': notif,
            'form': form,
            'warn': passWarning,
            'success': passSuccess},**template(request)}
    )

def admin_settings(request):
    if (not request.user.is_authenticated) or get_current_user(request) == None:
        return redirect("login")
    curuser = get_current_user(request)

    print("checking form")
    new_user_fail = "none"
    new_user_success = "none"
    if ("inputUsername" in request.POST):
        if len(user.objects.filter(username=request.POST["inputUsername"])) > 0:
            print("User Already Exists")
            new_user_fail = "inherit"
        else:
            print("New User!!")
            newUID = list(map(lambda x: x.uid, user.objects.all())).sort()
            checkBox: BooleanField = 1 in request.POST.getlist('gridCheck')
            newUser = user(username=request.POST["inputUsername"],
                           usertype=1,
                           uid=newUID,
                           firstname=request.POST["inputFName"],
                           lastname=request.POST["inputLName"],
                           password=request.POST["inputPassword"],
                           email=request.POST["inputEmailAddress"],
                           notification=checkBox,
                           pronoun=request.POST["inputPronoun"],
                           phone=request.POST["inputPhone"],
                           overtime=request.POST["overtimeModal"]
                           )
            newUser.save()
            new_user_success = "inherit"

    request.POST._mutable = True
    passWarning = "none"
    passSuccess = "none"
    if "password" in request.POST:
        if request.POST["password"] == '':
            request.POST["password"] = curuser.password
        else:
            if request.POST["password"] == request.POST["cpassword"]:
                request.POST["password"] = make_password(request.POST["password"])
                passSuccess = "inherit"
            else:
                passWarning = "inherit"
    if "username" in request.POST:
        request.POST["username"] = curuser.username

    form = settingsForm(request.POST or None, instance=curuser)
    if form.is_valid():
        form.save()





    ot = "checked"
    notot = ""
    notif = "checked"
    if(not curuser.overtime):
        ot = ""
        notot = "checked"
    if(not curuser.notification):
        notif = ""
    return render(
        request,
        'catalog/admin_settings.html',
        context={**{'firstname': curuser.firstname,
            'lastname': curuser.lastname,
            'username': curuser.username,
            'email': curuser.email,
            'pronoun': curuser.pronoun,
            'phone': curuser.phone,
            'overtime': ot,
            'notovertime': notot,
            'notification': notif,
            'form': form,
            'warn': passWarning,
            'success': passSuccess,
            'warn_newu': new_user_fail,
            'success_newu': new_user_success},**template(request)}
    )

def availability(request):
    if (not request.user.is_authenticated) or get_current_user(request) == None:
        return redirect("login")
    availability_sched = get_availability_for_user(get_current_user(request))
    return render(
        request,
        'catalog/availability.html',
        context={**{'availability_sched':availability_sched},**template(request)}
    )

# Troy - Views for login/logout pages
def login(request):
    if request.user.is_authenticated and not (get_current_user(request) == None):
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
            #try:
            #    return User.objects.get(username=request.user.username)
            #except:
            #    return None
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
            'current_day': date(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day),  # right now just gets from the week that we have set up in data
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
        filter(start__date=get_date(datetime.now().year, datetime.now().month, datetime.now().month)).\
        order_by('start')

def get_week_schedule(start_date, current_user):
    sched_objs = list()
    end_of_week = start_date + timedelta(days=7)
    for time_obj in time.objects.filter(timetype=SHIFT, uid=current_user.uid) \
    .filter(start__gt=start_date) \
    .filter(start__lt=end_of_week) \
    .order_by('start'):
        # .filter(start__lt=(get_date()+datetime.timedelta(days=7))
        # this is a stupid tuple. Template parsing is not impressive.
        sched_objs.append((time_obj.start, \
                            time_obj.end, \
                            time_obj.start.strftime("%A"), \
                            time_obj.end.strftime("%A")))
    return sched_objs

def time_subtract(start, finish):

    d = finish - start
    d = (d.seconds)
    return d

def get_day_schedule_by_user(date):
    user_scheds = []
    for user_obj in user.objects.order_by('uid'):
        sched = [t for t in time.objects
                 .filter(start__date = date)
                 .filter(timetype = SHIFT)
                 .filter(uid = user_obj.uid)
                 .order_by('start')]
        bar_lengths = []
        if sched:
            start_of_day = dt.combine(date,tm(9,0,0,0,sched[0].start.tzinfo))
            end_of_day  = dt.combine(date,tm(17,0,0,0,sched[0].start.tzinfo))
            last_t = start_of_day
            for t in sched:
                tstart = t.start - timedelta(hours=4)
                if tstart.hour < start_of_day.hour:
                    tstart = start_of_day
                tend = t.end - timedelta(hours = 4)
                if tend.hour >= end_of_day.hour:
                    tend = end_of_day
                bar_lengths.append([[tstart.time, tend.time], (time_subtract(last_t, tstart)),
                                    (time_subtract(tstart,tend))])
                last_t = tend
                final_time = t

            bar_lengths.append([[final_time.start.time, 0],(time_subtract(last_t, \
                                                                          end_of_day)), 0])
        user_stuff = [user_obj.firstname,
        user_obj.lastname,
                      bar_lengths]
        user_scheds.append(user_stuff)
    return user_scheds

def get_availability_for_user(current_user):
    # Note: Availability and Conflicts are in the week of April 1

    start_date = date(year=2018,month=4,day=1)
    end_date = start_date+timedelta(days=7)
    shifts = time.objects.filter(uid=current_user.uid). \
        filter(start__gt=start_date).filter(end__lt=end_date).exclude(timetype=PUNCH_IN).exclude(timetype=PUNCH_OUT).exclude(timetype=SHIFT).order_by('start')

    # returning list weekdays with times in each. Starts with Monday
    week_tuples = [[None]]*7

    for shift in shifts:
        week_tuples[shift.start.date().weekday()].append( (timetype_to_string(shift.timetype), shift.start, shift.end) )

    return week_tuples

def timetype_to_string(x: int):
    return {
        1: "PUNCH_IN",
        2: "PUNCH_OUT",
        3: "SHIFT",
        4: "UNAVAILABLE",
        5: "REQUEST"
    }.get(x, "NONE")
