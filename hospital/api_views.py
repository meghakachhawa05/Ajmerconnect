from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Hospital, Doctor, TimeSlot, Appointment
from .serializers import (
    HospitalSerializer, DoctorSerializer, TimeSlotSerializer,
    AppointmentSerializer
)
from .services import HospitalAPIService

class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'hospital_admin'):
            return Hospital.objects.filter(hospital_admin=self.request.user)
        return Hospital.objects.all()

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'hospital_admin'):
            return Doctor.objects.filter(hospital__hospital_admin=self.request.user)
        return Doctor.objects.filter(is_available=True)

    @action(detail=True, methods=['get'])
    def time_slots(self, request, pk=None):
        doctor = self.get_object()
        time_slots = TimeSlot.objects.filter(
            doctor=doctor,
            date__gte=timezone.now().date(),
            is_available=True
        )
        serializer = TimeSlotSerializer(time_slots, many=True)
        return Response(serializer.data)

class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'hospital_admin'):
            return TimeSlot.objects.filter(doctor__hospital__hospital_admin=self.request.user)
        return TimeSlot.objects.filter(is_available=True)

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'hospital_admin'):
            return Appointment.objects.filter(doctor__hospital__hospital_admin=self.request.user)
        return Appointment.objects.filter(patient=self.request.user)

    def perform_create(self, serializer):
        time_slot = serializer.validated_data['time_slot']
        if not time_slot.is_available:
            raise serializers.ValidationError("This time slot is not available")
        
        time_slot.is_available = False
        time_slot.save()
        
        serializer.save(patient=self.request.user, status='Pending')

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        appointment = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status or new_status not in ['Pending', 'Confirmed', 'Cancelled', 'Completed']:
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        appointment.status = new_status
        appointment.save()
        
        if new_status == 'Cancelled':
            time_slot = appointment.time_slot
            time_slot.is_available = True
            time_slot.save()
        
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)

class HospitalInfoViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_service = HospitalAPIService()

    @action(detail=True, methods=['get'])
    def bed_availability(self, request, pk=None):
        """Get real-time bed availability for a hospital"""
        hospital = get_object_or_404(Hospital, pk=pk)
        data = self.api_service.get_available_beds(hospital.id)
        if data:
            return Response(data)
        return Response(
            {'error': 'Unable to fetch bed availability'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    @action(detail=True, methods=['get'])
    def emergency_status(self, request, pk=None):
        """Get emergency department status"""
        hospital = get_object_or_404(Hospital, pk=pk)
        data = self.api_service.get_emergency_status(hospital.id)
        if data:
            return Response(data)
        return Response(
            {'error': 'Unable to fetch emergency status'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    @action(detail=True, methods=['get'])
    def ot_status(self, request, pk=None):
        """Get operation theater status"""
        hospital = get_object_or_404(Hospital, pk=pk)
        data = self.api_service.get_operation_theater_status(hospital.id)
        if data:
            return Response(data)
        return Response(
            {'error': 'Unable to fetch OT status'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    @action(detail=True, methods=['get'])
    def pharmacy_inventory(self, request, pk=None):
        """Get pharmacy inventory status"""
        hospital = get_object_or_404(Hospital, pk=pk)
        data = self.api_service.get_pharmacy_inventory(hospital.id)
        if data:
            return Response(data)
        return Response(
            {'error': 'Unable to fetch pharmacy inventory'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    @action(detail=True, methods=['get'])
    def ambulance_status(self, request, pk=None):
        """Get ambulance availability status"""
        hospital = get_object_or_404(Hospital, pk=pk)
        data = self.api_service.get_ambulance_status(hospital.id)
        if data:
            return Response(data)
        return Response(
            {'error': 'Unable to fetch ambulance status'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    @action(detail=True, methods=['get'])
    def blood_bank_status(self, request, pk=None):
        """Get blood bank inventory status"""
        hospital = get_object_or_404(Hospital, pk=pk)
        data = self.api_service.get_blood_bank_status(hospital.id)
        if data:
            return Response(data)
        return Response(
            {'error': 'Unable to fetch blood bank status'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

class PatientInfoViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_service = HospitalAPIService()

    @action(detail=True, methods=['get'])
    def lab_results(self, request, pk=None):
        """Get patient lab results"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        data = self.api_service.get_lab_results(request.user.id)
        if data:
            return Response(data)
        return Response(
            {'error': 'Unable to fetch lab results'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        ) 