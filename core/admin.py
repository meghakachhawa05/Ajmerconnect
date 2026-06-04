from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import PasswordReset, Patient, Doctor, Slot, Booking

CustomUser = get_user_model()


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'contact',
        'age',
        'aadhar_no',
        'is_staff',
        'date_joined'
    )

    search_fields = (
        'username',
        'email',
        'contact',
        'aadhar_no',
    )

    list_filter = ('is_staff', 'is_active', 'date_joined')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'contact',
                'age',
                'aadhar_no',
                'address',
            )
        }),
        ('Permissions', {
            'fields': (
                'role',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ('user', 'reset_id', 'created_when')
    search_fields = ('user__username', 'user__email')
    list_filter = ('created_when',)
    readonly_fields = ('reset_id', 'created_when')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'age')
    search_fields = ('name', 'contact')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'speciality')
    search_fields = ('name', 'speciality')


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'time_from', 'time_to', 'slots')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'slot', 'booking_time')