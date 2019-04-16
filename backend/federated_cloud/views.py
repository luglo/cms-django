from django.http import HttpResponse

from federated_cloud.models import CMSCache


def getCMSIds(request):
    responseList = list(map(lambda cmsCacheEntry: cmsCacheEntry.id, CMSCache.objects.filter(shareWithOthers=True)))
    response = "-".join(responseList)
    return HttpResponse(response)




def getCMSes(request):
    a = CMSCache.objects.filter(shareWithOthers=True)
    return HttpResponse("Dies ist eine Antwort, die ein paar CMSes enthält." + type(a))


def getSite(request):
    # aksForCMS, useSites, shareWithOthers
    CMSCache(id = "1234567", name = "Andorraqw", domain = "www.andorra.com", public_key = "qwer").save()

    a = CMSCache.objects.all()
    return HttpResponse("Dies ist eine Antwort, die ein paar Sites enthält. " + str(len(a)) + " "+ a[0].id + " " +a[1].id + " " + a[2].id + " " + a[2].name)
