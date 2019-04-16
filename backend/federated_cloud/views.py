import json

from django.http import HttpResponse

from cms.models import Site
from federated_cloud.models import CMSCache


def cmsIds(request):
    responseList = [cmsCacheEntry.id for cmsCacheEntry in CMSCache.objects.filter(shareWithOthers=True)]
    response = json.dumps(responseList)
    return HttpResponse(response)


def cmsData(request, cmsId):
    responseCMS = CMSCache.objects.get(id=cmsId)
    responseDict = {"name": responseCMS.name, "domain": responseCMS.domain, "public_key": responseCMS.public_key}
    return HttpResponse(json.dumps(responseDict))


def dataOfSites(request):
    sites = Site.objects.all()
    responseList = [{
        "path": "",
        "aliases": "",
        "latitude": site.latitude,
        "longitude": site.longitude,
        "postal_code": site.postal_code,
        "prefix": "",
        "name_without_prefix": "",
    } for site in sites]
    return HttpResponse(json.dumps(responseList))
