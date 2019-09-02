from backend import settings
from cms.models import Configuration
from federation.tools import derive_id_from_public_key, gen_key_pair_strings

def activate_federation_feature():
    try:
        Configuration.objects.get(key="federation_private_key")
    except:
        private_key, public_key = gen_key_pair_strings()
        Configuration(
            key="federation_public_key",
            value=public_key
        ).save()
        Configuration(
            key="federation_private_key",
            value=private_key
        ).save()

def get_id():
    return derive_id_from_public_key(get_public_key())

def get_name():
    return settings.FEDERATION["name"]

def get_domain():
    return settings.FEDERATION["domain"]

def get_public_key():
    return Configuration.objects.get(key="federation_public_key").value

def get_private_key():
    return Configuration.objects.get(key="federation_private_key").value
