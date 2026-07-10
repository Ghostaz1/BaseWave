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