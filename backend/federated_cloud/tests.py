from federated_cloud.share_requests import send_offer


def test(request):
    #print(ask_for_cms_data("localhost:8000", "asdf"))
    #print(ask_for_cms_ids("localhost:8000"))
    send_offer()
    from django.http import HttpResponse
    return HttpResponse("asdf")