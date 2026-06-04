from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Hospital, Doctor, TimeSlot, Appointment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'name', 'address', 'contact_number', 'email', 'description']
        read_only_fields = ['id']

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    hospital = HospitalSerializer(read_only=True)
    hospital_id = serializers.PrimaryKeyRelatedField(
        queryset=Hospital.objects.all(),
        write_only=True,
        source='hospital'
    )

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'hospital', 'hospital_id', 'specialization', 
                 'qualifications', 'experience', 'bio', 'is_available']
        read_only_fields = ['id']

class TimeSlotSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        write_only=True,
        source='doctor'
    )

    class Meta:
        model = TimeSlot
        fields = ['id', 'doctor', 'doctor_id', 'date', 'start_time', 
                 'end_time', 'is_available']
        read_only_fields = ['id']

class AppointmentSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    time_slot = TimeSlotSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        write_only=True,
        source='doctor'
    )
    time_slot_id = serializers.PrimaryKeyRelatedField(
        queryset=TimeSlot.objects.all(),
        write_only=True,
        source='time_slot'
    )

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'doctor_id', 'time_slot', 
                 'time_slot_id', 'symptoms', 'status', 'created_at']
        read_only_fields = ['id', 'created_at'] 