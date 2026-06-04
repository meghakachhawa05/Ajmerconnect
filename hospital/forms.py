from django import forms
from .models import Doctor, Slot, Appointment, Hospital

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'specialization', 'experience', 'consultation_fee', 'is_active']
class SlotForm(forms.ModelForm):

    class Meta:
        model = Slot

        fields = [
            'doctor',
            'date',
            'start_time',
            'end_time',
            'max_patients',
            'is_active'
        ]

        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'start_time': forms.TimeInput(
                attrs={'type': 'time'}
            ),

            'end_time': forms.TimeInput(
                attrs={'type': 'time'}
            ),
        }
#class AppointmentForm(forms.ModelForm):
 #   class Meta:
  ##     fields = ['patient', 'slot', 'status']
class AppointmentForm(forms.ModelForm):
     class Meta:
         model = Appointment
         fields = ['patient',  'date']     


class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['name', 'address', 'phone', 'email', 'latitude', 'longitude', 'admin', 'is_active']
        
class SlotEditForm(forms.ModelForm):
    class Meta:
        model = Slot
        fields = ['date', 'start_time', 'end_time', 'max_patients', 'is_active']




class AppointmentBookingForm(forms.Form):
    name = forms.CharField(max_length=100)
    contact = forms.CharField(max_length=15)
    aadhar_number = forms.CharField(max_length=12)
    age = forms.IntegerField()
    address = forms.CharField(widget=forms.Textarea)
    slot_id = forms.IntegerField(widget=forms.HiddenInput())