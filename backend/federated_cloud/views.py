from django.http import JsonResponse

from cms.models import Site
from federated_cloud.models import CMSCache


def cmsIds(request):
    responseList = [
        cmsCacheEntry.id for cmsCacheEntry in CMSCache.objects.filter(shareWithOthers=True)
    ]
    return JsonResponse(responseList, safe=False)


def cmsData(request, cmsId):
    responseCMS = CMSCache.objects.get(id=cmsId)
    responseDict = {
        "name": responseCMS.name,
        "domain": responseCMS.domain,
        "public_key": responseCMS.public_key
    }
    return JsonResponse(responseDict, safe=False)


def dataOfSites(request):
    sites = Site.objects.all()
    responseList = [{
        "path": site.name,
        "aliases": "",
        "latitude": site.latitude,
        "longitude": site.longitude,
        "postal_code": site.postal_code,
        "prefix": "",
        "name_without_prefix": site.title,
    } for site in sites]
    return JsonResponse(responseList)

    #todo: prefix, name_without_prefix and aliases
