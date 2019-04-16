"""
File routing to the admin site
"""


from django.contrib import admin

from .models import Site
from federated_cloud.models import CMSCache

admin.site.register(Site)
admin.site.register(CMSCache)
