from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^cms-ids/', views.cms_ids),
    url(r'^cms-data/(?P<cms_id>[0-9,a-f]+)/$', views.cms_data),
    url(r'^site-data/', views.site_data),
]
