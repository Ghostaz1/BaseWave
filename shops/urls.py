from django.urls import path

from . import views

urlpatterns = [
    path('listings/', views.browse_listings_view, name='browse_listings'),
    path('listings/shop/<int:shop_id>/', views.shop_detail_view, name='shop_detail'),
    path('create/', views.create_shop_view, name='create_shop'),
    path('listings/create/', views.create_listing_view, name='create_listing'),
    path('listings/mine/', views.my_listings_view, name='my_listings'),
    path('listings/<int:listing_id>/toggle/', views.toggle_listing_availability_view, name='toggle_listing_availability'),
    path('admin/shops/', views.admin_shops_view, name='admin_shops'),
]