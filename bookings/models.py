from django.conf import settings
from django.db import models

from shops.models import Listing


def is_listing_available(listing, start_date, end_date, exclude_booking_item_id=None):
    conflicts = BookingItem.objects.filter(
        listing=listing,
        booking__status__in=[Booking.Status.PENDING, Booking.Status.CONFIRMED],
        start_date__lt=end_date,
        end_date__gt=start_date,
    )
    if exclude_booking_item_id:
        conflicts = conflicts.exclude(id=exclude_booking_item_id)
    return not conflicts.exists()


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'
        COMPLETED = 'completed', 'Completed'

    tourist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        limit_choices_to={'role': 'tourist'},
    )
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"Booking #{self.pk} - {self.tourist.username} ({self.status})"


class BookingItem(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='items')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='booking_items')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.listing.title} ({self.start_date} to {self.end_date})"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.end_date <= self.start_date:
            raise ValidationError('end_date must be after start_date.')