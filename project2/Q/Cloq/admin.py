from django.contrib import admin
from django import forms
from django.contrib.auth.hashers import make_password

from .models import user, announcement, time

class userForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, help_text="Change user password (encrypted and hidden)")
    class Meta:
        model = user
        exclude = []

@admin.register(user)
class userAdmin(admin.ModelAdmin):
    list_display = ('uid', 'lastname', 'firstname')
    readonly_fields = ('uid',)
    fields = [('uid', 'usertype'), ('firstname', 'lastname'),
              ('username', 'password'), 'email', 'pronoun',
              'phone', ('overtime', 'notification')]
    exclude = []
    def save_model(self, request, obj, form, change):
        if obj.pk:
            orig_obj = user.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        obj.save()
    form = userForm

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
