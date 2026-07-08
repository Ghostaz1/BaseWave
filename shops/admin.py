from django.contrib import admin

from .models import Shop, Listing


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'owner', 'location', 'contact_number')
    list_filter = ('location',)
    search_fields = ('shop_name', 'owner__username', 'location')


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'shop', 'category', 'price_per_day', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('title', 'shop__shop_name')