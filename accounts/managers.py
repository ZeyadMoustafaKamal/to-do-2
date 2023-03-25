from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError(_('You have to pass the E-mail to create a user'))
        email = self.normalize_email(email)
        user = self.model(email=email,*extra_fields)
        user.set_password(password)
        return user
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_stuff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        if extra_fields.get('is_stuff') is not True:
            raise ValueError(_('Please make sure that is_stuff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Please make sure that is_superuser=True'))
        return self.create_user(email,password,**extra_fields)