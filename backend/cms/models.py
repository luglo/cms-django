from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models


class EndDateValidator:
    start_date = None
    message = 'Enddatum liegt nicht nach dem Startdatum!'

    def __init__(self, start_date=None):
        if start_date is not None:
            self.start_date = start_date

    def __call__(self, value):
        if value <= self.start_date:
            raise ValidationError(self.message)

    def __eq__(self, other):
        return (isinstance(other, EnddateValidator) and
                other.message == self.message and
                other.start_date == self.start_date)


class Instance(models.Model):
    STATUS = (
        ('publ', 'Public'),
        ('priv', 'Private'),
        ('arch', 'Archived'),
    )
    name = models.CharField(max_length=250)
    slug = models.CharField(max_length=60)
    status = models.CharField(max_length=4, choices=STATUS)
    pub_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


class Event(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    location = models.ForeignKey(to='POI', on_delete=models.PROTECT)
    date = models.DateTimeField()
    duration = models.DurationField(default=timedelta(hours=1))
    picture = models.ImageField()
    is_all_day = models.BooleanField(default=False)
    is_recurring = models.BooleanField(default=False)


class RecurringEvent(Event):
    has_end_date = models.BooleanField(default=False)
    end_date = models.DateField(validators=[EndDateValidator(start_date=Event.date)], default=None,
                                blank=not has_end_date)
    FREQUENCY = (
        ('daily', 'Täglich'),
        ('weekly', 'Wöchentlich'),
        ('monthly', 'Monatlich'),
        ('yearly', 'Jährlich')
    )
    frequency = models.CharField(max_length=7, choices=FREQUENCY)


class POI(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    adress = models.CharField(max_length=250)
    postcode = models.CharField(max_length=10)
    city = models.CharField(max_length=250)
    region = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
