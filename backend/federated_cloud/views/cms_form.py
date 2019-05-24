"""
Form for creating a region object
"""

from django import forms
from django.utils.text import slugify

from federated_cloud.models import CMSCache


class FederatedCMSForm(forms.ModelForm):
    """
    DjangoForm Class, that can be rendered to create deliverable HTML

    Args:
        forms : Defines the form as an Model form related to a database object
    """
    push_notification_channels = forms.CharField(required=False)

    class Meta:
        model = CMSCache
        fields = ['name', 'domain', 'use_sites', 'aks_for_cms', 'share_with_others']

    def __init__(self, *args, **kwargs):
        super(FederatedCMSForm, self).__init__(*args, **kwargs)

    def save_federated_cms(self, federated_cms_id=None):
        """Function to create or update a region
            region_slug ([Integer], optional): Defaults to None. If it's not set creates
            a region or update the region with the given region slug.
        """

        if federated_cms_id:
            # save cms
            federated_cms = CMSCache.objects.get(id=federated_cms_id)
            federated_cms.name = self.cleaned_data['name']
            federated_cms.region.domain = self.cleaned_data['domain']
            federated_cms.useSites = self.cleaned_data['use_sites']
            federated_cms_id.askForCMSs = self.cleaned_data['ask_for_cms']
            federated_cms_id.shareWithOthers = self.cleaned_data['share_with_others']
            federated_cms.save()
