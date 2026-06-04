from django.urls import path
from . import views

app_name = "hospital"

urlpatterns = [

    

    # ===== PUBLIC =====
    path("list/", views.public_hospital_list, name="public_list"),
    path("detail/<int:pk>/", views.public_hospital_detail, name="public_detail"),
    
    # ===== BOOKING =====
    path("book/<int:hospital_id>/", views.book_appointment_view, name="book_appointment"),
    path("booking/success/<int:appointment_id>/", views.booking_success_view, name="booking_success"),

    # ===== DOCTORS =====
    path("doctors/", views.doctor_list, name="doctor_list"),
    path("doctors/add/", views.doctor_create, name="doctor_create"),
    path("doctors/edit/<int:pk>/", views.doctor_edit, name="doctor_edit"),

    # ===== SLOTS =====
    path("slots/", views.slot_list, name="slot_list"),
    path("slots/add/", views.slot_create, name="slot_create"),
    path("slots/edit/<int:pk>/", views.slot_edit, name="slot_edit"),

    # ===== DASHBOARD SLOTS =====
    path("dashboard/slots/", views.slot_manage, name="slot_manage"),
    path("dashboard/slots/create/", views.slot_create, name="create_slot"),
    path("dashboard/slots/edit/<int:slot_id>/", views.edit_slot, name="edit_slot"),
    path("dashboard/", views.dashboard_home, name="dashboard_home"),

    # ===== DASHBOARD APPOINTMENTS =====
    path("dashboard/appointments/", views.appointment_list, name="appointment_list"),
    path("dashboard/appointments/update/<int:appointment_id>/<str:status>/", views.update_appointment_status, name="update_appointment_status"),

    # ===== HOSPITAL ADMIN =====
    path("hospitals/", views.hospital_list, name="hospital_list"),
    path("hospitals/add/", views.hospital_create, name="hospital_create"),
    path("doctors/<int:pk>/",views.doctor_details,name="doctor_details"),
]