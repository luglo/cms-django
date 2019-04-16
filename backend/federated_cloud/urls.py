from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^cmsIds/', views.cmsIds),
    url(r'^cmsData/(?P<cmsId>[0-9,a-f]+)/$', views.cmsData),
    url(r'^dataOfSites/', views.dataOfSites),
]
