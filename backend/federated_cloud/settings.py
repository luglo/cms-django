import os
import json

from federated_cloud.models import CMSCache
from federated_cloud.tools import derive_id_from_public_key, bytes_to_string

config_file_path = "fed_cloud_config.json"


def activate_federated_cloud_feature(name: str, domain: str):
    public_key = os.urandom(32)  # todo: Generate key-pair properly
    private_key = os.urandom(64)
    id = derive_id_from_public_key(public_key)
    with open(config_file_path, 'w') as file:
        file.write(json.dumps({"id": id, "name": name, "domain": domain, "private_key": bytes_to_string(private_key), "public_key": bytes_to_string(public_key)}))


def add_cms(name: str, domain: str, public_key: bytes, useRegions: bool, askForCMSs: bool, shareWithOthers: bool):
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
    pass


def get_domain():
    pass


def get_public_key():
    pass


def get_private_key():
    pass

