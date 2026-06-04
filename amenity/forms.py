from django import forms
from .models import Amenity

class AmenityForm(forms.ModelForm):
    class Meta:
        model = Amenity
        fields = ['name', 'type', 'address', 'contact', 'website', 'description', 'latitude', 'longitude']

class SimpleAmenityForm(forms.ModelForm):
    class Meta:
        model = Amenity
        fields = ['name', 'latitude', 'longitude'] 
        


