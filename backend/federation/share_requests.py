import json
from federation.models import CMSCache, RegionCache
from federation.settings import get_name, get_domain, get_public_key
from federation.tools import send_federation_request


def ask_for_cms_ids(domain):
    response = send_federation_request(domain, "cms-ids")
    response_list = json.loads(response)
    return response_list


def ask_for_cms_data(domain, cms_id):
    response = send_federation_request(domain, "cms-data/" + str(cms_id))
    response_dict = json.loads(response)
    response_cms = CMSCache(
        id=cms_id,
        name=response_dict["name"],
        domain=response_dict["domain"],
        public_key=response_dict["public_key"],
    )
    response_cms.save()


def ask_for_region_data(cms_cache):
    response = send_federation_request(cms_cache.domain, "region-data")
    response_list = json.loads(response)
    for responseElement in response_list:
        RegionCache(
            parentCMS=cms_cache,
            path=responseElement["path"],
            postal_code=responseElement["postal_code"],
            prefix=responseElement["prefix"],
            name_without_prefix=responseElement["name_without_prefix"],
            aliases=responseElement["aliases"],
            latitude=responseElement["latitude"],
            longitude=responseElement["longitude"],
        ).save()


def send_offer(domain: str):
    send_federation_request(domain, "offer", {"name": get_name(), "domain": get_domain(), "public_key": get_public_key()})

# todo error-handling
