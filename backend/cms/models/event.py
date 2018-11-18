from django.db import models
from datetime import timedelta

class Event(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(default='')
    location = models.ForeignKey(to='POI', on_delete=models.PROTECT, null=True, blank=True)
    date = models.DateTimeField()
    duration = models.DurationField(default=timedelta(hours=1))
    picture = models.ImageField(null=True, blank=True)
    is_all_day = models.BooleanField(default=False)
    is_recurring = models.BooleanField(default=False)
    has_end_date = models.BooleanField(default=False)
    end_date = models.DateField(null=True, default=None, blank=True)
    FREQUENCY = (
        ('daily', 'Täglich'),
        ('weekly', 'Wöchentlich'),
        ('monthly', 'Monatlich'),
        ('yearly', 'Jährlich')
    )
    frequency = models.CharField(max_length=7, choices=FREQUENCY, null=True, blank=True, default=None)

    def clean(self):
        if self.end_date is not None:
            if self.end_date <= self.date.date():
                raise ValidationError('Enddatum liegt nicht nach dem Startdatum!')

    def __str__(self):
        return self.title
