from django.contrib import admin

from .models import Booking, BookingItem


class BookingItemInline(admin.TabularInline):
    model = BookingItem
    extra = 1


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'tourist', 'status', 'booking_date')
    list_filter = ('status',)
    search_fields = ('tourist__username',)
    inlines = [BookingItemInline]