from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .models import user

class MyBackEnd(object):
    def authenticate(self, **kwargs):
        try:
            existing_user = user.objects.get(username=kwargs['username'])
            print(existing_user)
            if check_password(kwargs['password'], existing_user.password):
                print("passed")
                try:
                    existing_user2 = User.objects.get(username=kwargs['username'])
                    return existing_user2
                except:
                    NewUser = User(username=kwargs['username'])
                    NewUser.save()
                    return NewUser
            else:
                return None
        except:
            print("trying auth db")
            try:
                existing_user = User.objects.get(username=kwargs['username'])
                print(existing_user)
                if check_password(kwargs['password'], existing_user.password):
                    return existing_user
                else:
                    return None
            except:
                return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
