from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from bookings.models import Booking
from .models import Payment


@role_required('admin')
def admin_payments_view(request):
    payments = Payment.objects.select_related('booking__tourist').order_by('-last_updated')
    return render(request, 'payments/admin_payments.html', {'payments': payments, 'active': 'payments'})


@role_required('tourist')
def make_payment_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, tourist=request.user)

    if booking.status != Booking.Status.CONFIRMED:
        messages.error(request, 'This booking is not ready for payment yet.')
        return redirect('my_bookings')

    if Payment.objects.filter(booking=booking, payment_status=Payment.PaymentStatus.PAID).exists():
        messages.info(request, 'This booking is already paid.')
        return redirect('my_bookings')

    total_amount = sum(
        item.listing.price_per_day * (item.end_date - item.start_date).days
        for item in booking.items.all()
    )

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        valid_methods = [choice[0] for choice in Payment.PaymentMethod.choices]
        if payment_method not in valid_methods:
            messages.error(request, 'Please select a valid payment method.')
            return render(request, 'payments/make_payment.html', {'booking': booking, 'total_amount': total_amount})

        Payment.objects.create(
            booking=booking,
            amount_paid=total_amount,
            payment_status=Payment.PaymentStatus.PAID,
            payment_method=payment_method,
        )
        messages.success(request, 'Payment recorded successfully!')
        return redirect('my_bookings')

    return render(request, 'payments/make_payment.html', {'booking': booking, 'total_amount': total_amount})