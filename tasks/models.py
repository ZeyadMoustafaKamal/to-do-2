from django.db import models
from django.conf import settings
class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    is_done = models.BooleanField(default=False)
