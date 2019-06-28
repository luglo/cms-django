from django.conf.urls import url

from federated_cloud import api

urlpatterns = [
    url(r'^cms-ids/', api.cms_ids),
    url(r'^cms-data/(?P<cms_id>[0-9,a-f]+)/$', api.cms_data),
    url(r'^site-data/', api.site_data),
]
