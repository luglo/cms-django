import json

import requests

from federated_cloud.models import CMSCache, RegionCache

def update_cms_data():
    """
    Asks all known CMSs for new cms_ids and asks for data of the new CMSs
    """
    cms_list = CMSCache.objects.all()
    cms_ids = [cms.id for cms in cms_list]
    for cms in cms_list:
        response_list = ask_for_cms_ids(cms.domain)
        for response in response_list:
            if response not in cms_ids:
                cms_ids.append(response)
                ask_for_cms_data(cms.domain, response)

def update_cms_content():
    """
    Updates all RegionCaches of all known CMSs
    """
    cms_list = CMSCache.objects.all()
    for cms in cms_list:
        ask_for_region_data(cms)


def addCMS(cms_id, name, domain, public_key, useRegions, askForCMSs, shareWithOthers):
    cms_new = CMSCache(
        id=cms_id,
        name=name,
        domain=domain,
        public_key=public_key,
        useRegions=useRegions,
        askForCMSs=askForCMSs,
        shareWithOthers=shareWithOthers
    )
    cms_new.save()


def send_federated_cloud_request(domain:str, tail:str) -> str:
    return requests.get("http://" + domain + "/federated-cloud/" + tail).text


def ask_for_cms_ids(domain):
    response = send_federated_cloud_request(domain, "cms-ids")
    response_list = json.loads(response)
    return response_list


def ask_for_cms_data(domain, cms_id):
    response = send_federated_cloud_request(domain, "cms-data/" + str(cms_id))
    response_dict = json.loads(response)
    response_cms = CMSCache(
        id=cms_id,
        name=response_dict["name"],
        domain=response_dict["domain"],
        public_key=response_dict["public_key"],
    )
    response_cms.save()


def ask_for_region_data(cms_cache):
    response = send_federated_cloud_request(cms_cache.domain, "region-data")
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


def send_offer():
    pass

# todo error-handling

def test(request):
    #print(ask_for_cms_data("localhost:8000", "asdf"))
    #print(ask_for_cms_ids("localhost:8000"))
    send_offer()
    from django.http import HttpResponse
    return HttpResponse("asdf")
