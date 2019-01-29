from datetime import time

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from cms.models.event import Event, EventTranslation
from cms.views.events.event_form import EventForm


class EventView(LoginRequiredMixin, TemplateView):
    base_context = {'current_menu_item': 'events'}
    model = Event
    template_name = 'events/event.html'
    event_translation_id = None

    def get(self, request, *args, **kwargs):
        if self.event_translation_id:
            e = EventTranslation.objects.filter(
                id=self.event_translation_id).select_related('event').first()
            form = EventForm(initial={
                'picture': e.event.picture,
                'start_date': e.event.start_date,
                'start_time': e.event.start_time,
                'end_date': e.event.end_date,
                'end_time': e.event.end_time,
                'frequency': e.event.recurrence_rule.frequency,
                'interval': e.event.recurrence_rule.interval,
                'weekdays_for_weekly': e.event.recurrence_rule.weekdays_for_weekly,
                'weekday_for_monthly': e.event.recurrence_rule.weekday_for_monthly,
                'week_for_monthly': e.event.recurrence_rule.week_for_monthly,
                'recurrence_end_date': e.event.recurrence_rule.end_date,
                'is_all_day': e.event.start_time == time(0, 0, 0, 0)
                              and e.event.end_time == time(0, 0, 0, 0),
                'is_recurring': e.event.recurrence_rule is not None,
                'has_recurrence_end_date': e.event.recurrence_rule.end_date if (
                    e.event.recurrence_rule is not None) else False,
                'title': e.title,
                'description': e.description,
                'status': e.status,
                'language': e.language.code,
            })
        else:
            form = EventForm()
        return render(request, self.template_name, {
            'form': form, **self.base_context})

    def post(self, request, event_translation_id=None):
        # TODO: error handling
        form = EventForm(request.POST, user=request.user)
        if form.is_valid():
            if form.data['submit_publish']:
                # TODO: handle status

                if event_translation_id:
                    form.save_event(event_translation_id=event_translation_id)
                else:
                    form.save_event()

                messages.success(request, 'Event wurde erfolgreich erstellt.')
            else:
                messages.success(request, 'Event wurde erfolgreich gespeichert.')
            # TODO: improve messages
        else:
            messages.error(request, 'Es sind Fehler aufgetreten.')

        return render(request, self.template_name, {
            'form': form, **self.base_context})
