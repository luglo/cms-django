from django.http import JsonResponse

from cms.models import Site
from federated_cloud.models import CMSCache


def cms_ids(request):
    """
    :param request:
    :return: a JSON-response containing all region-ids in the cms
    """
    response_list = [
        cmsCacheEntry.id for cmsCacheEntry in CMSCache.objects.filter(shareWithOthers=True)
    ]
    return JsonResponse(response_list, safe=False)


def cms_data(request, cms_id):
    """
    :param request:
    :param cms_id: The id of the cms which data is requested
    :return: a JSON-response containing name, domain and public key of the cms specified by cms_id
    """
    response_cms = CMSCache.objects.get(id=cms_id)
    response_dict = {
        "name": response_cms.name,
        "domain": response_cms.domain,
        "public_key": response_cms.public_key
    }
    return JsonResponse(response_dict, safe=False)


def region_data(request):
    """
    :param request:
    :return: A JSON-response containing meta information of all regions of the cms
    """
    regions = Site.objects.all()
    response_list = [{
        "path": region.slug,
        "aliases": "",
        "latitude": region.latitude,
        "longitude": region.longitude,
        "postal_code": region.postal_code,
        "prefix": "",
        "name_without_prefix": region.name,
    } for region in regions]
    return JsonResponse(response_list, safe=False)

# todo: prefix, name_without_prefix and aliases
