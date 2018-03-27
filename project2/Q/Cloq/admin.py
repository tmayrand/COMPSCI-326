from django.contrib import admin

from .models import user, announcement, time

@admin.register(user)
class userAdmin(admin.ModelAdmin):
    list_display = ('uid', 'lastname', 'firstname')
    fields = ['usertype', ('firstname', 'lastname'),
              ('username', 'password'), 'email', 'pronoun',
              'phone', ('overtime', 'notification')]

@admin.register(announcement)
class announcementAdmin(admin.ModelAdmin):
    list_display = ('aid', 'title', 'time')
    fields = ['title', 'text', 'time', 'usertype']

@admin.register(time)
class timeAdmin(admin.ModelAdmin):
    list_display = ('tid', 'start', 'end', 'timetype', 'uid')
    fields = [('timetype', 'uid'), ('start', 'end')]
