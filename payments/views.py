from django.shortcuts import render

from accounts.decorators import role_required
from .models import Payment


@role_required('admin')
def admin_payments_view(request):
    payments = Payment.objects.select_related('booking__tourist').order_by('-last_updated')
    return render(request, 'payments/admin_payments.html', {'payments': payments, 'active': 'payments'})