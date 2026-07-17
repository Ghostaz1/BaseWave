from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from shops.models import Listing
from .models import Booking, BookingItem, is_listing_available


@role_required('tourist')
def create_booking_view(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if not start_date or not end_date:
            messages.error(request, 'Please provide both start and end dates.')
            return render(request, 'bookings/create_booking.html', {'listing': listing})

        if start_date >= end_date:
            messages.error(request, 'End date must be after start date.')
            return render(request, 'bookings/create_booking.html', {'listing': listing})

        if not is_listing_available(listing, start_date, end_date):
            messages.error(request, 'This listing is already booked for those dates.')
            return render(request, 'bookings/create_booking.html', {'listing': listing})

        booking = Booking.objects.create(tourist=request.user)
        BookingItem.objects.create(
            booking=booking,
            listing=listing,
            start_date=start_date,
            end_date=end_date,
        )
        messages.success(request, 'Booking created successfully!')
        return redirect('dashboard')

    return render(request, 'bookings/create_booking.html', {'listing': listing})


@role_required('admin')
def admin_bookings_view(request):
    bookings = Booking.objects.select_related('tourist').prefetch_related('items__listing').order_by('-booking_date')
    return render(request, 'bookings/admin_bookings.html', {'bookings': bookings, 'active': 'bookings'})


@role_required('tourist')
def my_bookings_view(request):
    bookings = Booking.objects.filter(tourist=request.user).prefetch_related('items__listing', 'payments').order_by('-booking_date')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings, 'active': 'my_bookings'})


@role_required('tourist')
def cancel_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, tourist=request.user)

    if booking.status in ('cancelled', 'completed'):
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('my_bookings')

    if request.method == 'POST':
        booking.status = Booking.Status.CANCELLED
        booking.save()
        messages.success(request, 'Booking cancelled.')
        return redirect('my_bookings')

    return redirect('my_bookings')


@role_required('shop_owner')
def shop_bookings_view(request):
    booking_items = BookingItem.objects.filter(
        listing__shop__owner=request.user
    ).select_related('booking', 'listing', 'booking__tourist').order_by('-booking__booking_date')

    return render(request, 'bookings/shop_bookings.html', {'booking_items': booking_items, 'active': 'shop_bookings'})


@role_required('shop_owner')
def update_booking_status_view(request, booking_id, new_status):
    booking = get_object_or_404(Booking, id=booking_id, items__listing__shop__owner=request.user)

    valid_statuses = [choice[0] for choice in Booking.Status.choices]
    if new_status not in valid_statuses:
        messages.error(request, 'Invalid status.')
        return redirect('shop_bookings')

    if request.method == 'POST':
        booking.status = new_status
        booking.save()
        messages.success(request, f'Booking marked as {new_status}.')
        return redirect('shop_bookings')

    return redirect('shop_bookings')