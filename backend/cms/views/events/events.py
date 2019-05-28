from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from ...models import Language, Site, Event


class EventListView(LoginRequiredMixin, TemplateView):
    base_context = {'current_menu_item': 'events'}
    model = Event
    template_name = 'events/list_events.html'

    def get(self, request, *args, **kwargs):
        # current site
        site_slug = kwargs.get(('site_slug'))
        site = Site.objects.get(slug=site_slug)

        # current language
        language_code = kwargs.get('language_code', None)
        if language_code is not None:
            language = Language.objects.get(code=language_code)
        elif site.default_language is not None:
            return redirect('events', **{
                'site_slug': site_slug,
                'language_code': site.default_language.code
            })
        else:
            messages.error(
                request,
                _('Please create at least one language node before creating events.')
            )
            return redirect('language_tree', **{'site_slug': site_slug})

        # all events of the current site in the current language
        events = Event.get_list_view(site_slug)

        # all other languages of current site
        languages = site.languages

        return render(
            request,
            self.template_name,
            {
                **self.base_context,
                'events': events,
                'language': language,
                'languages': languages
            })
