import os

from federated_cloud.models import CMSCache
from federated_cloud.tools import derive_id_from_public_key


def activate_federated_cloud_feature(name: str, domain: str):
    public_key = os.urandom(32)  # todo: Generate key-pair properly
    id = derive_id_from_public_key(public_key)


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


def update_cms(cms_id: str, name_new: str, domain_new: str, useRegion_new: str, askForCMSs_new: str, shareWithOthers_new: str):
    pass
