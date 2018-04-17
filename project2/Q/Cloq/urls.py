from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.login, {'template_name': 'catalog/login.html'}, name="login"),
    path('dashboard', views.dash, name ='dash'),
    path('admin_dashboard', views.admin_dash, name = "admin_dash"),
    path('availability', views.availability, name = "availability"),
    path('schedule/<int:year>/<int:month>/<int:day>/', views.schedule, name="schedule"),
    path('admin_schedule', views.admin_schedule, name="admin_schedule"),
    path('settings', views.settings, name="settings"),
    path('login', auth_views.login, {'template_name': 'catalog/login.html'}, name="login"),
    path('logout', auth_views.logout, {'template_name': 'catalog/logout.html'}, name="logout"),
]
