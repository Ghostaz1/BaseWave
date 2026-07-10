from django.urls import path

from . import views

urlpatterns = [
    path('admin/payments/', views.admin_payments_view, name='admin_payments'),
]