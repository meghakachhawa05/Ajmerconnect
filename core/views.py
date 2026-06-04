from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse

from .models import PasswordReset
from amenity.models import Amenity
from hospital.models import Hospital, Doctor
from booking.models import Booking
import json
import requests
from hospital.models import Appointment
from core.models import CustomUser


User = get_user_model()

# =========================
# HOME
# =========================
def home(request):
    context = {
        'hospital_count': Hospital.objects.count(),
        'doctor_count': Doctor.objects.count(),
        'amenity_count': Amenity.objects.count(),
        'booking_count': Booking.objects.count(),
        'featured_amenities': Amenity.objects.filter(is_featured=True)[:6] or Amenity.objects.all()[:6]
    }
    
    return render(request, 'core/home.html', context)


# =========================
# MAP VIEW
# =========================
def map_view(request):
    amenities = Amenity.objects.filter(latitude__isnull=False, longitude__isnull=False)
    hospitals = Hospital.objects.filter(latitude__isnull=False, longitude__isnull=False, is_active=True)

    places = []
    amenity_types = set()

    for amenity in amenities:
        amenity_types.add(amenity.type)
        places.append({
            'name': amenity.name,
            'latitude': float(amenity.latitude),
            'longitude': float(amenity.longitude),
            'type': amenity.type,
            'amenity_type': amenity.type,
            'address': amenity.address,
            'description': amenity.description or "Amenity in Ajmer",
            'detail_url': reverse('amenity:detail', args=[amenity.pk]),
            'book_url': '',
        })

    for hospital in hospitals:
        places.append({
            'name': hospital.name,
            'latitude': float(hospital.latitude),
            'longitude': float(hospital.longitude),
            'type': 'hospital',
            'amenity_type': 'hospital',
            'address': hospital.address,
            'description': f"Hospital in Ajmer — {hospital.phone}",
            'detail_url': reverse('hospital:public_detail', args=[hospital.pk]),
            'book_url': reverse('hospital:public_detail', args=[hospital.pk]),
        })

    context = {
        'places': json.dumps(places),
        'amenity_types': sorted(amenity_types),
    }
    return render(request, 'core/map.html', context)


def nominatim_search(request):
    query = request.GET.get('q', '')
    url = f"https://nominatim.openstreetmap.org/search?q={query}+Ajmer+Rajasthan&format=json&limit=5&addressdetails=1"
    response = requests.get(url, headers={'User-Agent': 'AjmerConnect/1.0'})
    from django.http import JsonResponse
    return JsonResponse(response.json(), safe=False)


# =========================
# ROLE BASED DASHBOARD REDIRECT
# =========================
@login_required
def dashboard_router(request):
    user = request.user

    if user.role == "super_admin":
        return redirect("/admin/")

    elif user.role == "hospital_admin":
        return redirect("hospital:dashboard_home")  # ✅ Fixed

    elif user.role == "ticket_admin":
        return redirect("dashboard:dashboard_home")

    else:
        return redirect("core:home")


# =========================
# REGISTER
# =========================


def register_view(request):
    if request.method == 'POST':

        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        aadhar_no = request.POST.get('aadhar_no')
        age = request.POST.get('age')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('core:register')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('core:register')

        user = CustomUser.objects.create_user(
            username=email,
            first_name=full_name,
            email=email,
            password=password,
            contact=contact,
            age=age if age else None,
            aadhar_no=aadhar_no,
            address=address,
            role="user"
        )

        messages.success(request, "Account created successfully")
        return redirect('core:user_login')

    return render(request, 'core/register.html')
# LOGIN
# =========================
def login_view(request):
    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user:

            login(request, user)

            # ===== NEXT URL CHECK =====
            next_url = request.GET.get('next')

            if next_url:
                return redirect(next_url)

            # ===== ROLE BASED REDIRECT =====
            if user.role == "super_admin":
                return redirect("/admin/")

            elif user.role == "hospital_admin":
                return redirect("hospital:dashboard_home")

            elif user.role == "ticket_admin":
                    return redirect("booking:admin_dashboard")

            else:
                return redirect("core:home")

        messages.error(request, "Invalid credentials")

    return render(request, 'core/login.html')

# =========================
# LOGOUT
# =========================
def logout_view(request):
    logout(request)
    return redirect('core:home')


# =========================
# PASSWORD RESET
# =========================
def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
            reset = PasswordReset.objects.create(user=user)

            reset_url = reverse('core:reset_password', kwargs={'reset_id': reset.reset_id})
            full_url = f"{request.scheme}://{request.get_host()}{reset_url}"

            EmailMessage(
                "Reset Password",
                f"Click below link to reset password:\n\n{full_url}",
                settings.EMAIL_HOST_USER,
                [email]
            ).send()

            return redirect('core:password_reset_sent', reset_id=reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, "Email not found")

    return render(request, 'core/forgot_password.html')


def password_reset_sent(request, reset_id):
    return render(request, 'core/password_reset_sent.html')


def reset_password(request, reset_id):
    try:
        reset = PasswordReset.objects.get(reset_id=reset_id)

        if timezone.now() > reset.created_when + timezone.timedelta(minutes=10):
            reset.delete()
            messages.error(request, "Reset link expired")
            return redirect('core:forgot_password')

        if request.method == "POST":
            password = request.POST.get('password')
            confirm = request.POST.get('confirm_password')

            if password != confirm or len(password) < 5:
                messages.error(request, "Password invalid")
                return redirect('core:reset_password', reset_id=reset_id)

            user = reset.user
            user.set_password(password)
            user.save()
            reset.delete()

            messages.success(request, "Password reset successful")
            return redirect('core:user_login')

    except PasswordReset.DoesNotExist:
        messages.error(request, "Invalid reset link")
        return redirect('core:forgot_password')

    return render(request, 'core/reset_password.html')


# =========================
# STATIC PAGES
# =========================
def about_view(request):
    return render(request, 'core/about.html')


def contact_view(request):
    return render(request, 'core/contact.html')


# =========================
# SAFE HOSPITAL REDIRECT
# =========================
def hospital_redirect(request):
    return redirect('hospital:hospital_list')



from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from hospital.models import Patient, Appointment
from booking.models import Booking


@login_required
def my_account(request):

    appointments = []
    tickets = []

    # ===== HOSPITAL APPOINTMENTS =====
    try:
        patient = Patient.objects.get(user=request.user)

        appointments = Appointment.objects.filter(
            patient=patient
        ).order_by('-id')

    except Patient.DoesNotExist:
        appointments = []

    # ===== TICKETS =====
    tickets = Booking.objects.filter(
        user=request.user
    ).order_by('-id')

    context = {
        'appointments': appointments,
        'tickets': tickets,
    }

    return render(request, 'core/my_account.html', context)