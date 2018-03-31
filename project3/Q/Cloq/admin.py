from django.contrib import admin

from .models import user, announcement, time

@admin.register(user)
class userAdmin(admin.ModelAdmin):
    list_display = ('uid', 'lastname', 'firstname')
    readonly_fields = ('uid',)
    fields = [('uid', 'usertype'), ('firstname', 'lastname'),
              ('username', 'password'), 'email', 'pronoun',
              'phone', ('overtime', 'notification')]

@admin.register(announcement)
class announcementAdmin(admin.ModelAdmin):
    list_display = ('aid', 'title', 'time')
    readonly_fields = ('aid',)
    fields = [('title', 'aid'), 'text', 'time', 'usertype']

@admin.register(time)
class timeAdmin(admin.ModelAdmin):
    list_display = ('tid', 'start', 'end', 'timetype', 'uid')
    readonly_fields = ('tid',)
    fields = [('timetype', 'uid', 'tid'), ('start', 'end')]
