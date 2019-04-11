from django.http import HttpResponse
import requests

from federated_cloud.models import CMSCache


def getCMSIds(request):
    responseList = list(map(lambda cmsCacheEntry: cmsCacheEntry.id, CMSCache.objects.filter(shareWithOthers=True)))
    response = "-".join(responseList)
    return HttpResponse(response)




def getCMSes(request):
    return HttpResponse("Dies ist eine Antwort, die ein paar CMSes enthält.")


def getSite(request):
    r=requests.get("http://localhost:8000/federated-cloud/getCMSes/")
    return HttpResponse("Dies ist eine Antwort, die ein paar Sites enthält. " + str(r.text))
