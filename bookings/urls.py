from django.urls import path

from . import views

urlpatterns = [
    path('book/<int:listing_id>/', views.create_booking_view, name='create_booking'),
    path('admin/bookings/', views.admin_bookings_view, name='admin_bookings'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking_view, name='cancel_booking'),
    path('shop-bookings/', views.shop_bookings_view, name='shop_bookings'),
    path('shop-bookings/<int:booking_id>/status/<str:new_status>/', views.update_booking_status_view, name='update_booking_status'),
]