from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'amount_paid', 'payment_status', 'payment_method', 'last_updated')
    list_filter = ('payment_status', 'payment_method')
    search_fields = ('booking__id',)