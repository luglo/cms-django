from django import forms
from django.core.validators import RegexValidator

from cms.models import POI, POITranslation, Language


class POIForm(forms.ModelForm):
    # General POI related fields
    address = forms.CharField(max_length=250, label='Adresse')
    postcode = forms.CharField(max_length=10, validators=[
        RegexValidator(regex=r'^[0-9]{4,}$', message='Keine gültige PLZ')], label='Postleitzahl')
    city = forms.CharField(max_length=250, label='Stadt')
    region = forms.CharField(max_length=250, label='Region/Bundesland', required=False)
    country = forms.CharField(max_length=250, label='Land')
    latitude = forms.FloatField(label='Breitengrad', required=False)
    longitude = forms.FloatField(label='Längengrad', required=False)

    # POI translation related fields
    status = forms.ChoiceField(choices=POITranslation.STATUS)
    minor_edit = forms.BooleanField(required=False)
    public = forms.BooleanField(required=False)

    class Meta:
        model = POITranslation
        fields = ['title', 'description']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(POIForm, self).__init__(*args, **kwargs)
        # TODO: get available languages from site settings
        self.fields['language'] = forms.ChoiceField(
            choices=[('de', 'Deutsch'),
                     ('ar', 'Arabisch'),
                     ('fa', 'Farsi'),
                     ('fr', 'Französisch'),
                     ('tr', 'Türkisch')])

    def save_poi(self, poi_translation_id=None):
        # TODO: version, active_version
        if poi_translation_id:
            p = POITranslation.objects.filter(
                id=poi_translation_id).select_related('poi').first()
            poi = POI.objects.get(id=p.poi.id)
            poi_translation = POITranslation.objects.get(id=p.id)
        else:
            poi = POI()
            poi_translation = POITranslation()
            poi_translation.poi = poi
            poi_translation.creator = self.user

        # save POI
        poi.address = self.cleaned_data['address']
        poi.postcode = self.cleaned_data['postcode']
        poi.city = self.cleaned_data['city']
        poi.region = self.cleaned_data['region']
        poi.country = self.cleaned_data['country']
        poi.latitude = self.cleaned_data['latitude']
        poi.longitude = self.cleaned_data['longitude']
        poi.save()

        # save poi translation
        poi_translation.title = self.cleaned_data['title']
        poi_translation.description = self.cleaned_data['description']
        poi_translation.status = self.cleaned_data['status']
        poi_translation.language = Language.objects.filter(
            code=self.cleaned_data['language']).first()
        poi_translation.minor_edit = self.cleaned_data['minor_edit']
        poi_translation.public = self.cleaned_data['public']
        poi_translation.save()
