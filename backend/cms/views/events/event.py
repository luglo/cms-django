from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from .event_form import EventForm, EventTranslationForm
from ...decorators import region_permission_required
from ...models import Site, Language, Event, EventTranslation


@method_decorator(region_permission_required, name='dispatch')
class EventView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'cms.view_events'
    raise_exception = True

    template_name = 'events/event.html'
    base_context = {'current_menu_item': 'events'}

    def get(self, request, *args, **kwargs):
        site = Site.objects.get(slug=kwargs.get('site_slug'))
        language = Language.objects.get(code=kwargs.get('language_code'))

        # get event and event translation objects if they exist, otherwise objects are None
        event = Event.objects.filter(id=kwargs.get('event_id')).first()
        event_translation = EventTranslation.objects.filter(
            event=event,
            language=language
        ).first()

        event_form = EventForm(
            instance=event,
            site=site,
            language=language
        )
        event_translation_form = EventTranslationForm(
            instance=event_translation
        )

        # poi_form = POIForm(initial={
        #     'address': l.address,
        #     'postcode': l.postcode,
        #     'city': l.city,
        #     'region': l.region,
        #     'country': l.country,
        #
        # })
        return render(request, self.template_name, {
            'event_form': event_form,
            'event_translation_form': event_translation_form,
            'event': event,
            'language': language,
            'languages': site.languages,
            **self.base_context
        })

    def post(self, request, *args, **kwargs):
        site = Site.objects.get(slug=kwargs.get('site_slug'))
        language = Language.objects.get(code=kwargs.get('language_code'))

        event_instance = Event.objects.filter(id=kwargs.get('event_id')).first()
        event_translation_instance = EventTranslation.objects.filter(
            event=event_instance,
            language=language,
        ).first()

        event_form = EventForm(
            request.POST,
            instance=event_instance,
            site=site,
            language=language,
        )
        event_translation_form = EventTranslationForm(
            request.POST,
            instance=event_translation_instance,
            site=site,
            language=language
        )
        # TODO: error handling
        # poi_form = POIForm(request.POST, user=request.user)
        if event_form.is_valid() and event_translation_form.is_valid():# or poi_form.is_valid():

            event = event_form.save()
            event_translation = event_translation_form.save(
                event=event,
                user=request.user,
            )

            if event_form.has_changed() or event_translation_form.has_changed():
                published = event_translation.public \
                            and 'public' in event_translation_form.changed_data
                if not event_instance:
                    if published:
                        messages.success(request,
                                         _('Event was successfully created and published.'))
                    else:
                        messages.success(request, _('Event was successfully created.'))
                elif not event_translation_instance:
                    if published:
                        messages.success(request,
                                         _('Translation was successfully created and published.'))
                    else:
                        messages.success(request, _('Translation was successfully created.'))
                else:
                    if published:
                        messages.success(request, _('Translation was successfully published.'))
                    else:
                        messages.success(request, _('Translation was successfully saved.'))
            else:
                messages.info(request, _('No changes detected.'))

            return redirect('edit_event', **{
                'event_id': event.id,
                'site_slug': site.slug,
                'language_code': language.code,
            })

        messages.error(request, _('Errors have occurred.'))

        return render(request, self.template_name, {
            **self.base_context,
            'event_form': event_form,
            'event_translation_form': event_translation_form,
            'event': event_instance,
            'language': language,
            'languages': site.languages,
        })
