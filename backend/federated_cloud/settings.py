import os
import json

from cms.models import Configuration
from federated_cloud.models import CMSCache
from federated_cloud.tools import derive_id_from_public_key, gen_key_pair_strings, bytes_to_string

config_file_path = "backend/federated_cloud/fed_cloud_config.json"


def activate_federated_cloud_feature(name: str, domain: str):
    private_key, public_key = gen_key_pair_strings()
    Configuration(
        key="federated_cloud_name",
        value=name
    ).save()
    Configuration(
        key="federated_cloud_domain",
        value=domain
    ).save()
    # todo: are name and domain already saved in other location?
    Configuration(
        key="federated_cloud_public_key",
        value=public_key
    ).save()
    Configuration(
        key="federated_cloud_private_key",
        value=private_key
    ).save()


def add_cms(name: str, domain: str, public_key: str, useRegions: bool, askForCMSs: bool, shareWithOthers: bool):
    cms_new = CMSCache(
        id=derive_id_from_public_key(public_key),
        name=name,
        domain=domain,
        public_key=public_key,
        useRegions=useRegions,
        askForCMSs=askForCMSs,
        shareWithOthers=shareWithOthers
    )
    cms_new.save()


def update_cms_settings(cms_id: str, useRegion_new: str, askForCMSs_new: str, shareWithOthers_new: str):
    cms = CMSCache.objects.get(id=cms_id)
    cms.useRegions = useRegion_new
    cms.askForCMSs = askForCMSs_new
    cms.shareWithOthers = shareWithOthers_new
    cms.save()


def get_id():
    public_key = get_public_key()
    return derive_id_from_public_key(public_key)

def get_name():
    return Configuration.objects.get(key="federated_cloud_name").value

def get_domain():
    return Configuration.objects.get(key="federated_cloud_domain").value

def get_public_key():
    return Configuration.objects.get(key="federated_cloud_public_key").value

def get_private_key():
    return Configuration.objects.get(key="federated_cloud_private_key").value
