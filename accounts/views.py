from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import CustomUser
from .decorators import role_required

def home(request):
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        if role not in ('tourist', 'shop_owner'):
            role = 'tourist'
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'accounts/register.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'accounts/register.html')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=role,
        )
        messages.success(request, 'Account created! Please login.')
        return redirect('login')

    return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            remember_me = request.POST.get('remember_me')
            if remember_me:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)  # expires on browser close

            messages.success(request, f'Welcome back, {user.first_name}!')

            if user.role == 'admin' or user.is_superuser:
                return redirect('dashboard')
            elif user.role == 'shop_owner':
                from shops.models import Shop
                if Shop.objects.filter(owner=user).exists():
                    return redirect('create_listing')
                else:
                    return redirect('create_shop')
            else:
                return redirect('browse_listings')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = request.build_absolute_uri(f'/reset-password/{uid}/{token}/')

            send_mail(
                subject='Reset your Basewave password',
                message=f'Hi {user.first_name},\n\nClick the link below to reset your password:\n{reset_link}\n\nIf you didn\'t request this, ignore this email.',
                from_email=None,
                recipient_list=[email],
            )

        messages.success(request, 'If that email exists, a reset link was sent.')
        return redirect('login')

    return render(request, 'accounts/forgot_password.html')

def reset_password_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        messages.error(request, 'This reset link is invalid or has expired.')
        return redirect('forgot_password')

    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/reset_password.html')

        user.set_password(password1)
        user.save()
        messages.success(request, 'Password reset successfully! Please login.')
        return redirect('login')

    return render(request, 'accounts/reset_password.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    total_users = CustomUser.objects.count()
    tourists = CustomUser.objects.filter(role='tourist').count()
    shop_owners = CustomUser.objects.filter(role='shop_owner').count()
    recent_users = CustomUser.objects.order_by('-date_joined')[:5]
    context = {
        'user': request.user,
        'total_users': total_users,
        'tourists': tourists,
        'shop_owners': shop_owners,
        'recent_users': recent_users,
        'active': 'dashboard',
    }
    context['active'] = 'dashboard'
    return render(request, 'accounts/dashboard.html', context)
@role_required('admin')

def users_list_view(request):
    users = CustomUser.objects.order_by('-date_joined')
    return render(request, 'accounts/users_list.html', {'users': users, 'active': 'users'})