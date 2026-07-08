from django.conf import settings
from django.db import models


class Shop(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shops',
        limit_choices_to={'role': 'shop_owner'},
    )
    shop_name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    contact_number = models.CharField(max_length=15)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.shop_name


class Listing(models.Model):
    class Category(models.TextChoices):
        MOTORBIKE = 'motorbike', 'Motorbike'
        SURFBOARD = 'surfboard', 'Surfboard'
        ROOM = 'room', 'Room'
        TOUR = 'tour', 'Tour'
        OTHER = 'other', 'Other'

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='listings')
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.shop.shop_name})"