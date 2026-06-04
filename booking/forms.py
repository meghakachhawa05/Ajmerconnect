from django import forms
from django import forms
from .models import Appointment, Slot, Patient
from django.contrib.auth.models import User


class AppointmentBookingForm(forms.Form):
    """Simplified booking form - User fills personal details directly"""
    
    # Personal Details
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your full name'})
    )
    contact = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Enter contact number'})
    )
    aadhar_number = forms.CharField(
        max_length=12,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Aadhar number (optional)'})
    )
    age = forms.IntegerField(
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter age'})
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter address'})
    )
    
    # Slot Selection (filled by radio button in template)
    slot_id = forms.IntegerField(widget=forms.HiddenInput())

    def clean_slot_id(self):
        slot_id = self.cleaned_data.get('slot_id')
        try:
            slot = Slot.objects.get(id=slot_id, is_active=True)
            if slot.available_slots() <= 0:
                raise forms.ValidationError('This slot is fully booked.')
            return slot_id
        except Slot.DoesNotExist:
            raise forms.ValidationError('Invalid slot selected.')