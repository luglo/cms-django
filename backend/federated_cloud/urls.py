from django.conf.urls import url

from federated_cloud import sharing, tests

urlpatterns = [
    url(r'^cms-ids/', sharing.cms_ids),
    url(r'^cms-data/(?P<cms_id>[0-9,a-z]+)/$', sharing.cms_data),
    url(r'^region-data/', sharing.region_data),
    url(r'^offer/', sharing.receive_offer),
    url(r'^test/', tests.test) #todo: remove test-stuff
]
