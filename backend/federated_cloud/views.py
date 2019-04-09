from django.http import HttpResponse
import requests


def getCMSes(request):
    return HttpResponse("Dies ist eine Antwort, die ein paar CMSes enthält.")


def getSite(request):
    r=requests.get("http://localhost:8000/federated-cloud/getCMSes/")
    return HttpResponse("Dies ist eine Antwort, die ein paar Sites enthält. " + str(r.text))
