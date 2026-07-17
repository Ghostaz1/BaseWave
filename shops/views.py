from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST

from accounts.decorators import role_required
from .models import Listing, Shop


def browse_listings_view(request):
    shops = Shop.objects.filter(listings__is_available=True).distinct().order_by('shop_name')
    return render(request, 'shops/browse_listings.html', {'shops': shops})


def shop_detail_view(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    listings = shop.listings.filter(is_available=True)
    return render(request, 'shops/shop_detail.html', {'shop': shop, 'listings': listings})

@role_required('shop_owner')
def create_shop_view(request):
    existing_shop = Shop.objects.filter(owner=request.user).first()
    if existing_shop:
        messages.info(request, 'You already have a shop. Add listings to it below.')
        return redirect('create_listing')

    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        description = request.POST.get('description')
        contact_number = request.POST.get('contact_number')
        location = request.POST.get('location')

        if not shop_name or not contact_number or not location:
            messages.error(request, 'Shop name, contact number, and location are required.')
            return render(request, 'shops/create_shop.html')

        Shop.objects.create(
            owner=request.user,
            shop_name=shop_name,
            description=description,
            contact_number=contact_number,
            location=location,
        )
        messages.success(request, 'Shop created successfully!')
        return redirect('create_listing')

    return render(request, 'shops/create_shop.html')


@role_required('shop_owner')
def create_listing_view(request):
    shop = Shop.objects.filter(owner=request.user).first()

    if not shop:
        messages.error(request, 'You need to create a shop first before adding listings.')
        return redirect('create_shop')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        price_per_day = request.POST.get('price_per_day')

        if not title or not price_per_day:
            messages.error(request, 'Title and price per day are required.')
            return render(request, 'shops/create_listing.html', {'shop': shop})

        try:
            price_value = float(price_per_day)
            if price_value <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, 'Price per day must be a valid positive number.')
            return render(request, 'shops/create_listing.html', {'shop': shop})

        Listing.objects.create(
            shop=shop,
            title=title,
            description=description,
            category=category,
            price_per_day=price_value,
        )

        messages.success(request, 'Listing created successfully!')
        return redirect('my_listings')

    return render(request, 'shops/create_listing.html', {'shop': shop})


@role_required('admin')
def admin_shops_view(request):
    shops = Shop.objects.select_related('owner').order_by('shop_name')
    return render(request, 'shops/admin_shops.html', {'shops': shops, 'active': 'shops'})


@role_required('shop_owner')
def my_listings_view(request):
    shop = Shop.objects.filter(owner=request.user).first()

    if not shop:
        messages.info(request, 'You need to create a shop first.')
        return redirect('create_shop')

    listings = shop.listings.all()
    return render(request, 'shops/my_listings.html', {'shop': shop, 'listings': listings})


@role_required('shop_owner')
@require_POST
def toggle_listing_availability_view(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, shop__owner=request.user)
    listing.is_available = not listing.is_available
    listing.save()
    status = 'available' if listing.is_available else 'unavailable'
    messages.success(request, f'"{listing.title}" marked as {status}.')
    return redirect('my_listings')