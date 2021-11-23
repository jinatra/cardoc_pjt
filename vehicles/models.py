from django.db                       import models
from django.db.models.fields.related import ForeignKey

from core.models import TimeStampModel
from users.models import User

class Vehicle(TimeStampModel):
    model_name = models.CharField(max_length=50)
    user       = ForeignKey(User, on_delete=models.CASCADE)
    front_tire = ForeignKey('FrontTire', null=True ,on_delete=models.SET_NULL)
    rear_tire  = ForeignKey('RearTire', null=True ,on_delete=models.SET_NULL)

    class Meta:
        db_table = 'vehicles'

class FrontTire(TimeStampModel):
    width        = models.PositiveSmallIntegerField()
    aspect_ratio = models.PositiveSmallIntegerField()
    wheel_size   = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'front_tires'

class RearTire(TimeStampModel):
    width        = models.PositiveSmallIntegerField()
    aspect_ratio = models.PositiveSmallIntegerField()
    wheel_size   = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'rear_tires'