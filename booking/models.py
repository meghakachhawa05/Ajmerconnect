from django.db import models
from django.conf import settings


class Booking(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('used', 'Used'),
    ]

    # =========================
    # USER
    # =========================
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ticket_bookings',
        null=True,
        blank=True
    )

    # =========================
    # AMENITY / HOSPITAL
    # =========================
    amenity = models.ForeignKey(
        'amenity.Amenity',
        on_delete=models.SET_NULL,
        related_name='ticket_bookings',
        null=True,
        blank=True
    )

    hospital = models.ForeignKey(
        'hospital.Hospital',
        on_delete=models.SET_NULL,
        related_name='ticket_bookings',
        null=True,
        blank=True
    )

    # =========================
    # BOOKING DETAILS
    # =========================
    booking_date = models.DateField()

    slot_time = models.TimeField(
        null=True,
        blank=True
    )

    num_tickets = models.PositiveIntegerField(default=1)

    amount_per_ticket = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # =========================
    # PAYMENT
    # =========================
    payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # =========================
    # STATUS
    # =========================
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    is_verified = models.BooleanField(default=False)

    # =========================
    # VISITOR INFO
    # =========================
    visitor_name = models.CharField(max_length=200)

    visitor_phone = models.CharField(max_length=15)

    # =========================
    # CREATED
    # =========================
    created_at = models.DateTimeField(auto_now_add=True)

    # =========================
    # SAVE
    # =========================
    def save(self, *args, **kwargs):
        self.total_amount = self.num_tickets * self.amount_per_ticket
        super().save(*args, **kwargs)

    # =========================
    # STRING
    # =========================
    def __str__(self):
        return f"{self.visitor_name} - {self.status}"