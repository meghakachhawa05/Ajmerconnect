from django.db import models
from django.conf import settings


# -------------------- HOSPITAL SYSTEM --------------------

class Hospital(models.Model):
    name = models.CharField(max_length=200)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)

    experience = models.PositiveIntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.name}"


class Slot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    max_patients = models.PositiveIntegerField(default=1)
    booked_count = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    def available_slots(self):
        return self.max_patients - self.booked_count

    def __str__(self):
        return f"{self.doctor.name} - {self.date} {self.start_time}"


class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    gender = models.CharField(max_length=10, choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ])

    blood_group = models.CharField(max_length=5, blank=True)
    phone_number = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username or str(self.user.id)


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)

    date = models.DateField()   # 🔥 important

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment {self.id} - {self.patient}"
    


# -------------------- AMENITY (PLACES / TOURIST / ETC) --------------------

class Amenity(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)

    description = models.TextField()
    extra_info = models.TextField(blank=True)

    photo = models.URLField()
    map_link = models.URLField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# -------------------- TICKET SYSTEM --------------------

class Ticket(models.Model):
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    total_capacity = models.PositiveIntegerField()
    available_capacity = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.amenity.name} Ticket"


class TicketBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('used', 'Used'),
        ('expired', 'Expired'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    booking_date = models.DateField()

    quantity = models.PositiveIntegerField(default=1)

    amount_per_ticket = models.DecimalField(max_digits=8, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')

    payment_id = models.CharField(max_length=100, unique=True, null=True, blank=True)

    visitor_name = models.CharField(max_length=200)
    visitor_phone = models.CharField(max_length=15)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.amount_per_ticket * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.id} - {self.user}"