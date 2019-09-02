from backend import settings
from cms.models import Configuration
from federation.tools import derive_id_from_public_key, derive_public_key_from_private_key, generate_private_key

def activate_federation_feature():
    try:
        Configuration.objects.get(key="federation_private_key")
    except:
        Configuration(
            key="federation_private_key",
            value=generate_private_key()
        ).save()

def get_id():
    return derive_id_from_public_key(get_public_key())

def get_name():
    return settings.FEDERATION["name"]

def get_domain():
    return settings.FEDERATION["domain"]

def get_public_key():
    return derive_public_key_from_private_key(get_private_key())

def get_private_key():
    return Configuration.objects.get(key="federation_private_key").value
