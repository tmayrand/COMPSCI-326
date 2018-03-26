from django.shortcuts import render_to_response
from django.shortcuts import render

# Create your views here.

# Jane does these pages
def dash(request):

    return render(
        request,
        'catalog/user_dash.html',
        context={}
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
