from federated_cloud.models import CMSCache
from federated_cloud.share_requests import ask_for_cms_ids, ask_for_cms_data, ask_for_region_data


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
