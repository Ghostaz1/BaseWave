from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('bookings/', include('bookings.urls')),
    path('shops/', include('shops.urls')),
    path('payments/', include('payments.urls')),
]