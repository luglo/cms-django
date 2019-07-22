from django.http import HttpResponse

from federated_cloud.settings import *
from federated_cloud.share_requests import send_offer


def test(request):
    print(get_id())


    print(get_name())


    print(get_domain())

    print(get_public_key())

    print(get_private_key())
    return HttpResponse("asdf")