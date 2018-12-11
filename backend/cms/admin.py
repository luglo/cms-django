from django.contrib import admin

from .models.site import Site

'''
# Commented out these lines because of changes in the models
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'get_location_name')
    list_filter = ['start_date', 'location__name']
    search_fields = ['title', 'description', 'get_location_name']

    def get_location_name(self, obj):
        loc = obj.location
        return 'Unknown' if loc is None else loc.name

    get_location_name.short_description = 'Location'
    get_location_name.admin_order_field = 'location__name'


class POIAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country')
    list_filter = ['country', 'region', 'city']
    search_fields = ['name', 'description', 'adress', 'postcode', 'city', 'country', 'region']


admin.site.register(POI, POIAdmin)
admin.site.register(Event, EventAdmin)
'''

admin.site.register(Site)
