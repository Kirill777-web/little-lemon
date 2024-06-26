from django.db import models
import datetime

# Create your models here.
# Model Bokking


class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    guest_number = models.IntegerField()
    reservation_date = models.DateField(default=datetime.date.today)
    reservation_slot = models.TimeField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name
# Model Menu


class Menu(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.CharField(max_length=1000, default='')

    def __str__(self):
        return str(self.name)

 # Comments


class UserComments(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    comment = models.CharField(max_length=1000)
