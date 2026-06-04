from django.contrib import admin
from .models import Doctor, Slot, Appointment, Hospital, Patient


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'hospital', 'experience', 'consultation_fee', 'is_active']


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'date', 'start_time', 'end_time', 'max_patients', 'booked_count', 'is_active']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'slot', 'status', 'created_at']


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ['name', 'admin', 'phone', 'email', 'is_active']


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'blood_group', 'phone_number', 'emergency_contact']