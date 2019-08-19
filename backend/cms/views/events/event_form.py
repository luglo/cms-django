"""
Form for creating or saving event objects and their corresponding event translation objects
"""

from datetime import time

from django import forms
from django.utils.text import slugify
from django.utils.translation import ugettext as _

from ...models import Event, EventTranslation, RecurrenceRule


class EventForm(forms.ModelForm):
    """
    Form class that can be rendered to create HTML code
    Inherits from django.forms.ModelForm, corresponds to the Event model
    """
    # General event related fields
    start_date = forms.DateField(input_formats=['%d.%m.%Y'])
    start_time = forms.TimeField(input_formats=['%H:%M'], required=False)
    end_date = forms.DateField(input_formats=['%d.%m.%Y'])
    end_time = forms.TimeField(input_formats=['%H:%M'], required=False)
    frequency = forms.ChoiceField(choices=RecurrenceRule.FREQUENCY, required=False)
    interval = forms.IntegerField(min_value=1, required=False)
    weekdays_for_weekly = forms.MultipleChoiceField(choices=RecurrenceRule.WEEKDAYS,
                                                    widget=forms.CheckboxSelectMultiple,
                                                    required=False)
    weekday_for_monthly = forms.ChoiceField(choices=RecurrenceRule.WEEKDAYS, required=False)
    week_for_monthly = forms.ChoiceField(
        choices=[(1, '1.'), (2, '2.'), (3, '3.'), (4, '4.'), (5, '5.')], required=False)
    recurrence_end_date = forms.DateField(input_formats=['%d.%m.%Y'], required=False)
    is_all_day = forms.BooleanField(required=False)
    is_recurring = forms.BooleanField(required=False)
    has_recurrence_end_date = forms.BooleanField(required=False)

    class Meta:
        model = Event
        fields = ['picture']

    def __init__(self, *args, **kwargs):
        # pop kwargs to prevent error when calling super class
        self.region = kwargs.pop('region', None)
        language = kwargs.pop('language', None)
        instance = kwargs.get('instance')
        if instance is not None:
            # instantiate ModelForm with initial values
            super(EventForm, self).__init__(
                initial={'start_date': instance.start_date,
                         'end_date': instance.end_date,
                         'start_time': instance.start_time.isoformat(timespec='minutes'),
                         'end_time': instance.end_time.isoformat(timespec='minutes'),
                         'is_all_day': instance.start_time == time.min and instance.end_time == time.max,
                         # TODO: initialise other fields also
                         },
                *args, **kwargs)
        else:
            super(EventForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):

        # disable instant commit on saving because missing information would cause errors
        kwargs['commit'] = False
        event = super(EventForm, self).save(*args, **kwargs)

        if self.instance.id is None:
            # set initial values on event creation
            event.region = self.region

        event.start_date = self.cleaned_data['start_date']
        event.end_date = self.cleaned_data['end_date']
        if self.cleaned_data['is_all_day']:
            event.start_time = time.min
            event.end_time = time.max
        else:
            event.start_time = self.cleaned_data['start_time'] or time.min
            event.end_time = self.cleaned_data['end_time'] or time.min
        if self.cleaned_data['is_recurring']:
            if event.recurrence_rule is None:
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

        return event

    # def save_event(self, region_slug, language_code, event_id=None, publish=False):
    #     """
    #     Function to create or update an event
    #
    #         event_id ([Integer], optional): Defaults to None.
    #         publish ([Boolean], optional): Defaults to False. Flag for changing publication status
    #                                        via publish button.
    #
    #         Returns:
    #             event: the created or updated event
    #     """
    #
    #     slug = slugify(self.cleaned_data['title'])
    #     event_translation = EventTranslation.objects.filter(
    #         event__id=event_id,
    #         language__code=language_code
    #     ).first()
    #
    #     # guarantee a unique slug
    #     if (
    #         (
    #             (
    #                 # new event has to be created
    #                 event_id is None
    #                 or
    #                 # new translation has to be created
    #                 event_translation is None
    #             )
    #             or
    #             # slug has changed
    #             event_translation.slug != slug
    #         )
    #         and
    #         # new slug already exists
    #         EventTranslation.objects.filter(slug=slug).exists()
    #     ):
    #         old_slug = slug
    #         i = 1
    #         while True:
    #             slug = old_slug + '-' + str(i)
    #             if not EventTranslation.objects.filter(slug=slug).exists():
    #                 break
    #             i += 1
    #
    #     # TODO: version, active version
    #
    #     if publish:
    #         self.cleaned_data['public'] = True
    #
    #     if event_id is not None:
    #         # event already exists, get event object
    #         event = Event.objects.get(id=event_id)
    #     else:
    #         # event doesn't exist yet, create new event
    #         event = Event.objects.create(
    #             region=Region.objects.get(slug=region_slug)
    #         )
    #
    #     if event_translation is None:
    #         # translation doesn't exist yet, create new translation
    #         event_translation = EventTranslation.objects.create(
    #             language=Language.objects.get(code=language_code),
    #             event=event,
    #             creator=self.user
    #         )
    #
    #     # save event
    #     event.picture = self.cleaned_data['picture']
    #     event.public = self.cleaned_data['public']
    #     event.start_date = self.cleaned_data['start_date']
    #     event.end_date = self.cleaned_data['end_date']
    #     event.location = self.cleaned_data['location']
    #     if self.cleaned_data['is_all_day']:
    #         event.start_time = time(0, 0, 0, 0)
    #         event.end_time = time(23, 59, 59, 0)
    #     else:
    #         event.start_time = self.cleaned_data['start_time']
    #         event.end_time = self.cleaned_data['end_time']
    #     if self.cleaned_data['is_recurring']:
    #         if not event.recurrence_rule:
    #             event.recurrence_rule = RecurrenceRule()
    #         event.recurrence_rule.frequency = self.cleaned_data['frequency']
    #         event.recurrence_rule.interval = self.cleaned_data['interval']
    #         event.recurrence_rule.weekdays_for_weekly = self.cleaned_data['weekdays_for_weekly']
    #         event.recurrence_rule.weekday_for_monthly = self.cleaned_data['weekday_for_monthly']
    #         event.recurrence_rule.week_for_monthly = self.cleaned_data['week_for_monthly']
    #         if self.cleaned_data['has_recurrence_end_date']:
    #             event.recurrence_rule.end_date = self.cleaned_data['recurrence_end_date']
    #         event.recurrence_rule.save()
    #     event.save()
    #
    #     # save event translation
    #     event_translation.slug = slug
    #     event_translation.title = self.cleaned_data['title']
    #     event_translation.description = self.cleaned_data['description']
    #     event_translation.status = self.cleaned_data['status']
    #     event_translation.minor_edit = self.cleaned_data['minor_edit']
    #     event_translation.public = self.cleaned_data['public']
    #     event_translation.save()
    #
    #     return event


class EventTranslationForm(forms.ModelForm):
    """
    Form class that can be rendered to create HTML code
    Inherits from django.forms.ModelForm, corresponds to the EventTranslation model
    """

    PUBLIC_CHOICES = (
        (True, _('Public')),
        (False, _('Private'))
    )

    class Meta:
        model = EventTranslation
        fields = ['title', 'slug', 'description', 'status', 'public']

    def __init__(self, *args, **kwargs):
        # pop kwargs to prevent error when calling super class
        self.region = kwargs.pop('region', None)
        self.language = kwargs.pop('language', None)

        # to set the public value through the submit button, we have to overwrite the field value
        # for public. We could also do this in the save() function, but this would mean that it is
        # not recognized in changed_data. Check if POST data was submitted and the publish button
        # was pressed
        if len(args) == 1 and 'submit_publish' in args[0]:
            # copy QueryDict because it is immutable
            post = args[0].copy()
            # remove the old public value (might be False and update() does only append, not
            # overwrite)
            post.pop('public')
            # update the POST field with True (has to be a string to make sure the field is
            # recognized as changed)
            post.update({'public': 'True'})
            # set the args to POST again
            args = (post,)

        # instantiate ModelForm
        super(EventTranslationForm, self).__init__(*args, **kwargs)

        self.fields['public'].widget = forms.Select(choices=self.PUBLIC_CHOICES)

    def save(self, *args, **kwargs):

        # pop kwargs to prevent error when calling super class
        event = kwargs.pop('event', None)
        user = kwargs.pop('user', None)
        if self.instance.id is None:
            # disable instant commit on saving because missing information would cause error
            kwargs['commit'] = False

        event_translation = super(EventTranslationForm, self).save(*args, **kwargs)

        if self.instance.id is None:
            # set initial values for new events
            event_translation.event = event
            event_translation.creator = user
            event_translation.language = self.language

        # finally save event_translation to database
        event_translation.save()

        return event_translation

    def clean_slug(self):

        slug = self.cleaned_data['slug']
        # if slug is empty, generate from title
        if not slug:
            # slugify to remove/convert special characters, whitespace, etc.
            slug = slugify(self.cleaned_data['title'])

        # make sure slug is unique per region and language
        unique_slug = slug
        i = 1
        while True:
            # add counter to the end of the slug and increment counter until unique slug was found
            other_event_translation = EventTranslation.objects.filter(
                event__region=self.region,
                language=self.language,
                slug=unique_slug
            ).exclude(id=self.instance.id)
            if not other_event_translation.exists():
                break
            i += 1
            unique_slug = f"{slug}-{i}"

        return unique_slug
