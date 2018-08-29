
import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password

logger = logging.getLogger('django.console')
User = get_user_model()


class SettingsBackend(ModelBackend):
    username = 'ivan'
    #username = 'client'
    email = 'agestart@gmail.com'
    password = 'pbkdf2_sha256$36000$mNhod7KctYUD$Yh7RJB8zYKpJuuTEGpaRyre1EzOKnctOReNeHqzZ3zY='

    def authenticate(self, request, username=None, password=None, **kwargs):
        login_valid = (self.username == username)

        if not login_valid:
            email = kwargs.get('email', username)
            email_valid = (self.email == email)
        else:
            email = self.email
            email_valid = True

        pwd_valid = check_password(password, self.password)

        if (login_valid or email_valid) and pwd_valid:
            try:
                user = User.objects.get(email=email)
                logger.debug('SettingsBackend login admin')
            except User.DoesNotExist:
                # Create a new user. There's no need to set a password
                # because only the password from settings.py is checked.
                user = User(name=self.username, email=self.email, password=self.password)
                user.is_active = True
                user.is_admin = True
                user.save()
                logger.debug('SettingsBackend admin create and login')
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
