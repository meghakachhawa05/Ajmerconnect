from django.db import models

class Amenity(models.Model):
    AMENITY_TYPE_CHOICES = [
        ('university', 'University'),
        ('townhall', 'Townhall'),
        ('park', 'Park'),
        ('temple', 'Temple'),
        ('historical', 'Historical Place'),
        ('resort', 'Resort'),
        ('restaurant', 'Restaurant'),
        ('hotel', 'Hotel'),
        ('museum', 'Museum'),
        ('lake', 'Lake'),
        ('school', 'School'),
        ('college', 'College'),
    ]

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=AMENITY_TYPE_CHOICES)
    address = models.TextField()
    contact = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='amenities/', blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True, blank=True)
    ticket_capacity = models.PositiveIntegerField(default=100, null=True, blank=True)
    has_ticket = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"