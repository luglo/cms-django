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

    def get(self, request, event_translation_id=None):
        if event_translation_id:
            e = EventTranslation.objects.filter(
                id=event_translation_id).select_related('event').first()
            form = EventForm(initial={
                'picture': e.event.picture,
                'start_date': e.event.start_date,
                'end_date': e.event.end_date,
                'is_all_day': e.event.is_all_day,
                'is_recurring': e.event.is_recurring,
                'has_recurring_end_date': e.event.has_recurring_end_date,
                'recurring_end_date': e.event.recurring_end_date,
                'frequency': e.event.frequency,
                'title': e.title,
                'description': e.description,
                'status': e.status,
                'language': e.language,
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
                    form.save(event_translation_id=event_translation_id)
                else:
                    form.save()

                messages.success(request, 'Event wurde erfolgreich erstellt.')
            else:
                messages.success(request, 'Event wurde erfolgreich gespeichert.')
            # TODO: improve messages
        else:
            messages.error(request, 'Es sind Fehler aufgetreten.')

        return render(request, self.template_name, {
            'form': form, **self.base_context})
