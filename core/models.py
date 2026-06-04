from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid


# =====================================================
# Custom User Model
# =====================================================

class CustomUser(AbstractUser):
    contact = models.CharField(max_length=15, null=True, blank=True, default="")
    age = models.PositiveIntegerField(null=True, blank=True)
    aadhar_no = models.CharField(max_length=12, null=True, blank=True, default="")
    address = models.TextField(null=True, blank=True)

    is_email_verified = models.BooleanField(default=False)

    ROLE_CHOICES = (
        ('hospital_admin', 'Hospital Admin'),
        ('ticket_admin', 'Ticket Admin'),
        ('super_admin', 'Super Admin'),
        ('user', 'User'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user'
    )

    def is_hospital_admin(self):
        return self.role == 'hospital_admin'

    def is_ticket_admin(self):
        return self.role == 'ticket_admin'

    def is_super_admin(self):
        return self.role == 'super_admin'

    def __str__(self):
        return self.username


# =====================================================
# Password Reset Model
# =====================================================

class PasswordReset(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='password_resets'   # ✅ FIXED (no conflict)
    )
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.username}"


# =====================================================
# Hospital System Models
# =====================================================

class Patient(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15, null=True, blank=True, default="")
    aadhar_number = models.CharField(max_length=12, null=True, blank=True, default="")
    age = models.PositiveIntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Slot(models.Model):
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='slots'
    )
    time_from = models.TimeField()
    time_to = models.TimeField()
    slots = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.doctor.name} — {self.time_from} to {self.time_to}"


class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hospital_bookings',   # ✅ UNIQUE
        null=True,
        blank=True
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='bookings',
        null=True,
        blank=True
    )

    slot = models.ForeignKey(
        Slot,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.patient:
            return f"Booking for {self.patient.name}"
        return f"Booking by {self.user}"