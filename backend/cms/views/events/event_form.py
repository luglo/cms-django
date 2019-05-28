"""
Form for creating or saving event objects and their corresponding event translation objects
"""

from datetime import time

from django import forms
from django.utils.text import slugify
from django.utils.translation import ugettext as _

from ...models import Language, Site, Event, EventTranslation, RecurrenceRule


class EventForm(forms.ModelForm):
    """
    Form class that can be rendered to create HTML code
    Inherits from django.forms.ModelForm, corresponds to the Event and EventTranslation models
    """
    # General event related fields
    picture = forms.ImageField(required=False)
    start_date = forms.DateField(input_formats=['%d.%m.%Y'], label=_('Start (date)'))
    start_time = forms.TimeField(input_formats=['%H:%M'], label=_('Start (time)'))
    end_date = forms.DateField(input_formats=['%d.%m.%Y'], label=_('End (date)'))
    end_time = forms.TimeField(input_formats=['%H:%M'], label=_('End (time)'))
    frequency = forms.ChoiceField(choices=RecurrenceRule.FREQUENCY, label=_('Frequency'),
                                  required=False)
    interval = forms.IntegerField(min_value=1, required=False)
    weekdays_for_weekly = forms.MultipleChoiceField(choices=RecurrenceRule.WEEKDAYS,
                                                    widget=forms.CheckboxSelectMultiple,
                                                    required=False)
    weekday_for_monthly = forms.ChoiceField(choices=RecurrenceRule.WEEKDAYS, required=False)
    week_for_monthly = forms.ChoiceField(
        choices=[(1, '1.'), (2, '2.'), (3, '3.'), (4, '4.'), (5, '5.')], required=False)
    recurrence_end_date = forms.DateField(input_formats=['%d.%m.%Y'], label=_('Repetition end date'),
                                          required=False)
    is_all_day = forms.BooleanField(label=_('Whole day'), required=False)
    is_recurring = forms.BooleanField(label=_('Repeats'), required=False)
    has_recurrence_end_date = forms.BooleanField(label=_('Repetition ends'), required=False)

    # Event translation related fields
    status = forms.ChoiceField(choices=EventTranslation.STATUS)
    minor_edit = forms.BooleanField(required=False)
    public = forms.BooleanField(required=False)

    # Event location related fields

    class Meta:
        model = EventTranslation
        fields = ['title', 'description']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EventForm, self).__init__(*args, **kwargs)

    def save_event(self, site_slug, language_code, event_id=None, publish=False):
        """
        Function to create or update an event

            event_id ([Integer], optional): Defaults to None.
            publish ([Boolean], optional): Defaults to False. Flag for changing publication status
                                           via publish button.

            Returns:
                event: the created or updated event
        """

        slug = slugify(self.cleaned_data['title'])
        event_translation = EventTranslation.objects.filter(
            event__id=event_id,
            language__code=language_code
        ).first()

        # guarantee a unique slug
        if (
            (
                (
                    # new event has to be created
                    event_id is None
                    or
                    # new translation has to be created
                    event_translation is None
                )
                or
                # slug has changed
                event_translation.slug != slug
            )
            and
            # new slug already exists
            EventTranslation.objects.filter(slug=slug).exists()
        ):
            old_slug = slug
            i = 1
            while True:
                slug = old_slug + '-' + str(i)
                if not EventTranslation.objects.filter(slug=slug).exists():
                    break
                i += 1

        #TODO: version, active version

        if publish:
            self.cleaned_data['public'] = True

        if event_id is not None:
            # event already exists, get event object
            event = Event.objects.get(id=event_id)
        else:
            # event doesn't exist yet, create new event
            event = Event.objects.create(
                site=Site.objects.get(slug=site_slug)
            )

        if event_translation is None:
            # translation doesn't exist yet, create new translation
            event_translation = EventTranslation.objects.create(
                language=Language.objects.get(code=language_code),
                event=event,
                creator=self.user
            )

        # save event
        event.picture = self.cleaned_data['picture']
        event.public = self.cleaned_data['public']
        event.start_date = self.cleaned_data['start_date']
        event.end_date = self.cleaned_data['end_date']
        event.location = self.cleaned_data['location']
        if self.cleaned_data['is_all_day']:
            event.start_time = time(0, 0, 0, 0)
            event.end_time = time(23, 59, 59, 0)
        else:
            event.start_time = self.cleaned_data['start_time']
            event.end_time = self.cleaned_data['end_time']
        if self.cleaned_data['is_recurring']:
            if not event.recurrence_rule:
                event.recurrence_rule = RecurrenceRule()
            event.recurrence_rule.frequency = self.cleaned_data['frequency']
            event.recurrence_rule.interval = self.cleaned_data['interval']
            event.recurrence_rule.weekdays_for_weekly = self.cleaned_data['weekdays_for_weekly']
            event.recurrence_rule.weekday_for_monthly = self.cleaned_data['weekday_for_monthly']
            event.recurrence_rule.week_for_monthly = self.cleaned_data['week_for_monthly']
            if self.cleaned_data['has_recurrence_end_date']:
                event.recurrence_rule.end_date = self.cleaned_data['recurrence_end_date']
            event.recurrence_rule.save()
        event.save()

        # save event translation
        event_translation.slug = slug
        event_translation.title = self.cleaned_data['title']
        event_translation.description = self.cleaned_data['description']
        event_translation.status = self.cleaned_data['status']
        event_translation.minor_edit = self.cleaned_data['minor_edit']
        event_translation.public = self.cleaned_data['public']
        event_translation.save()

        return event
