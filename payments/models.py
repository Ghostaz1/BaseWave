from django.db import models

from bookings.models import Booking


class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PAID = 'paid', 'Paid'
        FAILED = 'failed', 'Failed'
        REFUNDED = 'refunded', 'Refunded'

    class PaymentMethod(models.TextChoices):
        CARD = 'card', 'Card'
        GCASH = 'gcash', 'GCash'
        PAYMAYA = 'paymaya', 'PayMaya'
        CASH = 'cash', 'Cash'

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.GCASH)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment #{self.pk} for Booking #{self.booking_id} - {self.payment_status}"