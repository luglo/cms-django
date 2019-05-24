from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView
from django.shortcuts import render

from federated_cloud.models import CMSCache
from federated_cloud.views.cms_form import FederatedCMSForm


@method_decorator(login_required, name='dispatch')
class CMSListView(TemplateView):
    template_name = 'fed_cms_list.html'
    base_context = {'current_menu_item': 'regions'}

    def get(self, request, *args, **kwargs):
        regions = CMSCache.objects.all()

        return render(
            request,
            self.template_name,
            {
                **self.base_context,
                'regions': regions
            }
        )


@method_decorator(login_required, name='dispatch')
class CMSOptionsView(TemplateView):
    template_name = 'cms_options.html'
    base_context = {'current_menu_item': 'regions'}
    cms_id = None

    def get(self, request, *args, **kwargs):
        self.cms_id = self.kwargs.get('cms_id', None)
        if self.cms_id:
            fed_cms = CMSCache.objects.get(slug=self.cms_id)
            form = FederatedCMSForm(initial={
                'name': fed_cms.name,
                'domain': fed_cms.domain,
                'use_sites': fed_cms.useSites,
                'aks_for_cms': fed_cms.aksForCMSs,
                'share_with_others': fed_cms.shareWithOthers
            })
        else:
            form = FederatedCMSForm()
            # TODO: create fedCMS???
        return render(request, self.template_name, {
            'form': form, **self.base_context})

    def post(self, request, federated_cms_id=None):
        # TODO: error handling
        form = FederatedCMSForm(request.POST)
        if form.is_valid():
            if federated_cms_id:
                form.save_region(federated_cms_id=federated_cms_id)
                messages.success(request, _('CMS saved successfully.'))
            else:
                #TODO: create fedCMS???
                form.save_region()
                messages.success(request, _('CMS created successfully'))
            # TODO: improve messages
        else:
            messages.error(request, _('Errors have occurred.'))

        return render(request, self.template_name, {
            'form': form, **self.base_context})
