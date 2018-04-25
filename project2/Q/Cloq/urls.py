from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login, name="home"),
    path('dashboard', views.dash, name ='dash'),
    path('admin_dashboard', views.admin_dash, name = "admin_dash"),
    path('availability', views.availability, name = "availability"),
    path('schedule/<int:year>/<int:month>/<int:day>/', views.schedule, name="schedule"),
    path('admin_schedule/<int:year>/<int:month>/<int:day>/', views.admin_schedule, name="admin_schedule"),
    path('settings', views.settings, name="settings"),
    path('login', views.login, name="login"),
    path('logout', auth_views.logout, {'template_name': 'catalog/logout.html'}, name="logout"),
]
