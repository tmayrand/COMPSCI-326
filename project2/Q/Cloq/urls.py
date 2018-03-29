from django.urls import path
from . import views

urlpatterns = [
    path('', views.dash, name = 'home'),
    path('dashboard', views.dash, name ='dash'),
    path('admin_dashboard', views.admin_dash, name = "admin_dash"),
    path('availability', views.availability, name = "availability"),
    path('schedule', views.schedule, name = "schedule"),
    path('admin_schedule', views.admin_schedule, name = "admin_schedule"),
    path('settings', views.settings, name = "settings"),
]
