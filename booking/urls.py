# booking/urls.py
from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [

    # Home
    path('', views.home, name='home'),

    
    # Booking flow
    #path('confirm/<int:slot_id>/', views.booking_confirm, name='booking_confirm'),
    path('success/', views.booking_success, name='booking_success'),

    # User bookings
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    #path('book/<int:slot_id>/', views.create_booking, name='create_booking'),
    # ADMIN DASHBOARD
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/verify/', views.admin_verify_ticket, name='admin_verify_ticket'),
    path('admin/bookings/', views.admin_booking_list, name='admin_booking_list'),
    path('admin/bookings/<int:booking_id>/', views.admin_booking_detail, name='admin_booking_detail'),
    path('book/<int:amenity_id>/', views.create_booking, name='create_booking'),
    path('amenities/', views.amenity_list, name='amenity_list'),
    path('admin/verify/<int:booking_id>/', views.verify_ticket, name='verify_ticket'),




]
