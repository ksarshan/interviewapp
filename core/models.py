from django.db import models

# Create your models here.
from users.models import User


class RegisterTimeSlots(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    from_time = models.TimeField()
    to_time = models.TimeField()
    objects = models.Manager()

    class Meta:
        unique_together = ('user', 'date', 'from_time', 'to_time')

