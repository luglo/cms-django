from django.conf.urls import url

from federated_cloud import api, core

urlpatterns = [
    url(r'^cms-ids/', api.cms_ids),
    url(r'^cms-data/(?P<cms_id>[0-9,a-z]+)/$', api.cms_data),
    url(r'^region-data/', api.region_data),
    url(r'^offer/', api.receive_offer),
    url(r'^test/', core.test) #todo: remove test-stuff
]
