from django.shortcuts import render_to_response
from django.shortcuts import render

# Create your views here.

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
