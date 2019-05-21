from datetime import time

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from cms.models.event import Event, EventTranslation
from cms.views.events.event_form import EventForm
from cms.views.pois.poi_form import POIForm


class EventView(LoginRequiredMixin, TemplateView):
    base_context = {'current_menu_item': 'events'}
    model = Event
    template_name = 'events/event.html'
    event_translation_id = None

    def get(self, request, *args, **kwargs):
        if self.event_translation_id:
            e = EventTranslation.objects.filter(
                id=self.event_translation_id).select_related('event').first()
            event_form = EventForm(initial={
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
            event_form = EventForm()
        return render(request, self.template_name, {
            'event_form': event_form, **self.base_context})

    def post(self, request, site_slug):
        # TODO: error handling
        event_form = EventForm(request.POST, user=request.user)
        if event_form.is_valid():
            # TODO: set status according to 'save' or 'publish'
            if request.POST.get('submit_publish', False) or request.POST.get('submit_save', False):
                # TODO: handle status

                if self.event_translation_id:
                    event_form.save_event(
                        site_slug=site_slug,
                        event_translation_id=self.event_translation_id
                    )
                else:
                    event_form.save_event(
                        site_slug=site_slug
                    )

                messages.success(request, _('Event was saved successfully.'))
            else:
                messages.success(request, _('Event was created successfully.'))
            # TODO: improve messages
        else:
            messages.error(request, _('Errors have occurred.'))

        return render(request, self.template_name, {
            'event_form': event_form, **self.base_context})
