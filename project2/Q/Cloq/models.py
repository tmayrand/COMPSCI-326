from django.db import models
from django import forms
from datetime import datetime
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password

class user(models.Model):
    """
    Model for users:
        uid: integer: User identification number.
        usertype: integer: User type (1 = user, 2 = admin).
        firstname: string: User's first name.
        lastname: string: User's last name.
        username: string: User's username (used to login).
        password: string: Salted and hashed user password.
        email: string: User's email address.
        notification: boolean: Whether user wants to receive email notifications.
        pronoun: string: User's preferred pronouns.
        phone: string: User's phone number.
        overtime: boolean: Whether user wants to work overtime.
    """
    uid = models.AutoField(primary_key = True, help_text="User identifier.")
    usertype = models.IntegerField(help_text = "User type (1 = user, 2 = admin).")
    firstname = models.CharField(max_length=100, help_text = "First name.")
    lastname = models.CharField(max_length=100, help_text = "Last name.")
    username = models.CharField(max_length=30, help_text = "Username.")
    password = models.CharField(max_length=255, help_text = "Hashed user password.")
    email = models.EmailField(help_text = "User email.")
    notification = models.BooleanField(help_text = "Receive email notifications?")
    pronoun = models.CharField(max_length=30,blank=True,default="they/them/theirs", help_text = "User pronouns.")
    phone_regex = RegexValidator(regex=r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$', message="Phone number must be entered in the format: '+1 (888) 888-8888'.")
    phone = models.CharField(validators=[phone_regex], max_length=20, help_text = "User phone number.", default="+1 (888) 888-8888")
    overtime = models.BooleanField(help_text = "Work overtime?")
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    def __str__(self):
        return str(self.firstname) + " " + str(self.lastname)

class announcement(models.Model):
    """
    Model for announcement:
        aid: integer: Announcement identification number.
        text: string: Announcement body string.
        time: datetime: Announcement datetime timestamp.
        usertype: integer: Viewable by (1 = all users, 2 = admins only).
        title: string: Announcement title string.
    """
    aid = models.AutoField(primary_key = True, help_text = "Announcement identifier.")
    text = models.TextField(help_text = "Announcement body.")
    time = models.DateTimeField(default=datetime.now, help_text="Announcement datetime.")
    usertype = models.IntegerField(help_text = "Viewable by (1 = all users, 2 = admins only)")
    title = models.CharField(max_length=255, help_text = "Announcement title.")

    def __str__(self):
        return str(self.title)

class time(models.Model):
    """
    Model for time:
        tid: integer: Timestamp identification number.
        timetype: integer: Time type (1 = punch in, 2 = punch out, 3 = shift, 4 = unavailable, 5 = request)
        start: datetime: Start datetime.
        end: datetime: End datetime.
        uid: integer: Associated user ID.
    """
    tid = models.AutoField(primary_key = True, help_text = "Timestamp identifier.")
    timetype = models.IntegerField(help_text = "Time type (1 = punch in, 2 = punch out, 3 = shift, 4 = unavailable, 5 = request)")
    start = models.DateTimeField(default=datetime.now, help_text = "Start datetime.")
    end = models.DateTimeField(default=datetime.now, help_text = "End datetime.")
    uid = models.IntegerField(help_text = "Associated user ID.")

    def __str__(self):
        return self.start.strftime("%m/%d/%Y (%H:%M)") + " - " + self.end.strftime("%m/%d/%Y (%H:%M)")
