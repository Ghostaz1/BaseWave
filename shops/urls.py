from django.urls import path

from . import views

urlpatterns = [
    path('listings/', views.browse_listings_view, name='browse_listings'),
    path('create/', views.create_shop_view, name='create_shop'),
    path('listings/create/', views.create_listing_view, name='create_listing'),
    path('admin/shops/', views.admin_shops_view, name='admin_shops'),
]