from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    HospitalViewSet, DoctorViewSet, TimeSlotViewSet, AppointmentViewSet,
    HospitalInfoViewSet, PatientInfoViewSet
)

router = DefaultRouter()
router.register(r'hospitals', HospitalViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'time-slots', TimeSlotViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'hospital-info', HospitalInfoViewSet, basename='hospital-info')
router.register(r'patient-info', PatientInfoViewSet, basename='patient-info')

urlpatterns = [
    path('', include(router.urls)),
] 