from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'amenity',
        'hospital',
        'booking_date',
        'slot_time',
        'num_tickets',
        'total_amount',
        'status'
    )

    list_filter = (
        'status',
        'booking_date',
        'amenity',
        'hospital'
    )

    search_fields = (
        'visitor_name',
        'visitor_phone',
        'payment_id'
    )