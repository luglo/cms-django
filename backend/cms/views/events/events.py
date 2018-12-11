from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from cms.models.event import Event


class EventListView(LoginRequiredMixin, TemplateView):
    base_context = {'current_menu_item': 'events'}
    model = Event
    template_name = 'events/list_events.html'

    def get(self, request):
        events = Event.get_list_view()
        for event in events:
            event['location'] = event['location'].filter(language='de').first()  # Use german version of location only
        return render(request, self.template_name, {**self.base_context, 'events': events})
