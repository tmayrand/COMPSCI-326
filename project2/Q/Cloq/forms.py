from django import forms
from .models import *
class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = user
        widgets = {'password': forms.PasswordInput(),}
        fields = ['password']

class settingsForm(forms.ModelForm):
    overtime = forms.TypedChoiceField(coerce=lambda x: x == 'True',choices=((False, 'False'), (True, 'True')),widget=forms.RadioSelect)
    class Meta:
        model = user
        #fields = ['firstname']
        fields = ['firstname','lastname','username','password','email','notification','pronoun','phone','overtime']
