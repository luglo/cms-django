from django import forms

from cms.models.event import EventTranslation, Event


class EventForm(forms.ModelForm):
    # General event related fields
    picture = forms.ImageField(required=False)
    start_date = forms.DateTimeField(input_formats=['%d.%m.%Y', '%d.%m.%Y %H:%M'])
    end_date = forms.DateTimeField(input_formats=['%d.%m.%Y', '%d.%m.%Y %H:%M'])
    is_all_day = forms.BooleanField(label='Ganztägiges Event')
    is_recurring = forms.BooleanField(label='Wiederkehrendes Event')
    has_recurring_end_date = forms.BooleanField(label='Wiederholung hat Enddatum')
    recurring_end_date = forms.DateTimeField(input_formats=['%d.%m.%Y', '%d.%m.%Y %H:%M'])
    frequency = forms.ChoiceField(choices=Event.FREQUENCY)

    # Event translation related fields
    status = forms.ChoiceField(choices=EventTranslation.STATUS)

    class Meta:
        model = EventTranslation
        fields = ['title', 'description', 'status', 'language']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EventForm, self).__init__(*args, **kwargs)
        # TODO: get available languages from site settings
        self.fields['language'] = forms.ChoiceField(
            choices=[('de', 'Deutsch'),
                     ('ar', 'Arabisch'),
                     ('fa', 'Farsi'),
                     ('fr', 'Französisch'),
                     ('tr', 'Türkisch')])

    def save(self, commit=True, event_translation_id=None):
        # TODO: version, active_version
        if event_translation_id:
            p = EventTranslation.objects.filter(
                id=event_translation_id).select_related('event').first()

            # save event
            event = Event.objects.get(id=p.event.id)
            event.picture = self.cleaned_data['picture']
            event.start_date = self.cleaned_data['start_date']
            event.end_date = self.cleaned_data['end_date']
            event.location = self.cleaned_data['location']
            event.is_all_day = self.cleaned_data['is_all_day']
            event.is_recurring = self.cleaned_data['is_recurring']
            event.has__recurring_end_date = self.cleaned_data['has_recurring_end_date']
            event.recurring_end_date = self.cleaned_date['recurring_end_date']
            event.frequency = self.cleaned_data['frequency']
            event.save()

            # save event translation
            event_translation = EventTranslation.objects.get(id=p.id)
            event_translation.title = self.cleaned_data['title']
            event_translation.description = self.cleaned_data['description']
            event_translation.status = self.cleaned_data['status']
            event_translation.language = self.cleaned_data['language']
            event_translation.save()
        else:
            # create event
            event = Event.objects.create(
                picture=self.cleaned_data['picture'],
                start_date=self.cleaned_data['start_date'],
                end_date=self.cleaned_data['end_date'],
                location=self.cleaned_data['location'],
                is_all_day=self.cleaned_data['is_all_day'],
                is_recurring=self.cleaned_data['is_recurring'],
                has__recurring_end_date=self.cleaned_data['has_recurring_end_date'],
                recurring_end_date=self.cleaned_date['recurring_end_date'],
                frequency=self.cleaned_data['frequency']
            )

            # create event translation
            event_translation = EventTranslation.objects.create(
                title=self.cleaned_data['title'],
                description=self.cleaned_data['description'],
                status=self.cleaned_data['status'],
                language=self.cleaned_data['language'],
                event=event,
                user=self.user
            )
