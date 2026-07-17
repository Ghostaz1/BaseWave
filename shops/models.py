from django.conf import settings
from django.db import models


class Shop(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shop',
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

    class BoardType(models.TextChoices):
        LONGBOARD = 'longboard', 'Longboard'
        SHORTBOARD = 'shortboard', 'Shortboard'

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='listings')
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    board_type = models.CharField(max_length=20, choices=BoardType.choices, blank=True, null=True)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    @property
    def price_unit(self):
        return 'hour' if self.category == self.Category.SURFBOARD else 'day'

    def __str__(self):
        return f"{self.title} ({self.shop.shop_name})"