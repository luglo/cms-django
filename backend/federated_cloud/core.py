import json

import requests

from federated_cloud.models import CMSCache, SiteCache


def sendCmsIdsRequest(domain):
    response = requests.get(domain + "/cmsIds")
    responseList = json.loads(response.text)
    return responseList


def sendCmsDataRequest(domain, cmsId):
    response = requests.get(domain + "/cmsData/" + cmsId)
    responseDict = json.loads(response)
    responseCMS = CMSCache(
        id=cmsId,
        name=responseDict["name"],
        domain=responseDict["domain"],
        public_key=responseDict["public_key"],
        useSites=True,
        askForCMSs=True,
        shareWithOthers=True
    )
    responseCMS.save()


def sendDataOfSitesRequest(cmsCache):
    response = requests.get(cmsCache.domain + "/dataOfSites")
    responseList = json.loads(response)
    for responseElement in responseList:
        SiteCache(
             parentCMS=cmsCache,
             path=responseElement["path"],
             postal_code=responseElement["postal_code"],
             prefix=responseElement["prefix"],
             name_without_prefix=responseElement["name_without_prefix"],
             aliases=responseElement["aliases"],
             latitude=responseElement["latitude"],
             longitude=responseElement["longitude"],
        ).save()


def sendOffer():
    pass

#todo error-handling
