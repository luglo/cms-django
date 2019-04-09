from django.conf.urls import  url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^getCMSes/', views.getCMSes),
    url(r'^getSite/', views.getSite),
]