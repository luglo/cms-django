from django.http import HttpResponse

from federated_cloud.settings import *
from federated_cloud.share_requests import send_offer, ask_for_cms_data
from federated_cloud.update_checker import update_cms_data


def test(request):
    print(get_id())


    print(get_name())


    print(get_domain())

    print(get_public_key())

    print(get_private_key())
    return HttpResponse("asdf")

def test_activate(request):
    name = "thomas"
    domain = "thomas-ist-cool.de"
    activate_federated_cloud_feature(name, domain)
    return HttpResponse("FedCloud-Feature aktiviert.")

def test_send_offer(request):
    domain="localhost:8000"
    send_offer(domain)
    return HttpResponse("Angebot gesendet.")

def test_update(reqeust):
    update_cms_data()
    return HttpResponse("Alles upgedatet.")

def test_ask(request):
    domain = "localhost:8000"
    id = "bdd9bfbd9742d81a1680"
    ask_for_cms_data(domain, id)
    return HttpResponse("Anfrage gestellt.")