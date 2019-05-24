from django.conf.urls import url

from federated_cloud import api
from federated_cloud.views.federated_cms import CMSOptionsView

urlpatterns = [
    url(r'^cms-ids/', api.cms_ids),
    url(r'^cms-data/(?P<cms_id>[0-9,a-f]+)/$', api.cms_data),
    url(r'^site-data/', api.site_data),

    url(r'^edit-cms/(?P<cms_id>[0-9,a-f]+)/$', CMSOptionsView.as_view(), name='edit_cms')
]
