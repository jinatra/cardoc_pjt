from django.db import models

from core.models import TimeStampModel


class User(TimeStampModel):
    email    = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=1000)
    nickname = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'users'