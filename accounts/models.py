from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.utils.translation import gettext as _
from django.conf import settings

class CustomUser(AbstractUser):

    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(_('email address'),unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    objects = CustomUserManager()
    code = models.CharField(default = '0', max_length=75)
    verified = models.BooleanField(default = False)
    created_at = models.DateTimeField(default=timezone.now())

    def check_code_expiration(self):
        return (self.created_at + timezone.timedelta(hours=24)) > timezone.now()
    def validate_code(self, code):

        if self.code == code and self.check_code_expiration():
            return True
        else:
            return False
    def __str__(self):
        return self.email
