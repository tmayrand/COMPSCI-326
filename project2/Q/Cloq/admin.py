from django.contrib import admin

from .models import user, announcement, time

admin.site.register(user)
admin.site.register(announcement)
admin.site.register(time)
