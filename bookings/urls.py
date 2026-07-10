from django.urls import path

from . import views

urlpatterns = [
    path('book/<int:listing_id>/', views.create_booking_view, name='create_booking'),
    path('admin/bookings/', views.admin_bookings_view, name='admin_bookings'),
]