from django.http import JsonResponse, HttpResponse, HttpRequest

from cms.models import Region
from federation import settings
from federation.models import CMSCache
from federation.tools import derive_id_from_public_key


def cms_ids(request: HttpRequest):
    """
    :param request:
    :return: a JSON-response containing all region-ids in the cms
    """
    response_list = [
        cmsCacheEntry.id for cmsCacheEntry in CMSCache.objects.filter(share_with_others=True)
    ] + [settings.get_id()]
    return JsonResponse(response_list, safe=False)


def cms_data(request: HttpRequest, cms_id: str):
    """
    :param request:
    :param cms_id: The id of the cms which data is requested
    :return: a JSON-response containing name, domain and public key of the cms specified by cms_id
    """
    if cms_id == settings.get_id():
        response_dict = {
            "name": settings.get_name(),
            "domain": settings.get_domain(),
            "public_key": settings.get_public_key()
        }
    else:
        response_cms = CMSCache.objects.get(id=cms_id)
        response_dict = {
            "name": response_cms.name,
            "domain": response_cms.domain,
            "public_key": response_cms.public_key
        }
    return JsonResponse(response_dict, safe=False)


def region_data(request: HttpRequest):
    """
    :param request:
    :return: A JSON-response containing meta information of all regions of the cms
    """
    regions = Region.objects.all()
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


def receive_offer(request: HttpRequest):
    public_key: str = request.GET["public_key"]
    cms_new = CMSCache(
        id=derive_id_from_public_key(public_key),
        name=request.GET["name"],
        domain=request.GET["domain"],
        public_key=public_key
    )
    cms_new.save()
    return HttpResponse()
# todo: prefix, name_without_prefix and aliases
