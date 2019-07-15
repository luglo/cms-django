from django.contrib import admin

from federated_cloud.models import CMSCache, RegionCache

admin.site.register(CMSCache)
admin.site.register(RegionCache)
