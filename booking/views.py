from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import uuid

from .models import Booking
from amenity.models import Amenity


# =========================
# HOME
# =========================
@login_required
def home(request):
    return render(request, 'booking/home.html')


# =========================
# AMENITY LIST
# =========================
@login_required
def amenity_list(request):
    amenities = Amenity.objects.all()
    return render(request, 'amenity/amenity_list.html', {
        'amenities': amenities
    })


# =========================
# AMENITY DETAIL
# =========================
@login_required
def amenity_detail(request, amenity_id):
    amenity = get_object_or_404(Amenity, id=amenity_id)
    return render(request, 'booking/amenity_detail.html', {
        'amenity': amenity
    })


# =========================
# CREATE BOOKING
# =========================
@login_required
def create_booking(request, amenity_id):
    amenity = get_object_or_404(Amenity, id=amenity_id)

    if request.method == "POST":
        try:
            # Get data safely
           # num_tickets = int(request.POST.get('num_tickets') or 1)
           
            num_tickets = request.POST.get('num_tickets')

            print(num_tickets)

            num_tickets = int(num_tickets)
            visitor_name = request.POST.get('visitor_name') or request.user.username
            visitor_phone = request.POST.get('visitor_phone')

            # Validation
            if num_tickets <= 0:
                messages.error(request, "Invalid number of tickets.")
                return redirect('booking:create_booking', amenity_id=amenity.id)

            if not visitor_phone:
                messages.error(request, "Phone number is required.")
                return redirect('booking:create_booking', amenity_id=amenity.id)

            # Create booking
            booking = Booking.objects.create(
                user=request.user,
                amenity=amenity,
                booking_date=timezone.now().date(),
                num_tickets=num_tickets,
                amount_per_ticket=amenity.ticket_price,
                visitor_name=visitor_name,
                visitor_phone=visitor_phone,
                payment_id=str(uuid.uuid4())[:10],
                status='pending'
            )

            messages.success(request, "Booking created. Proceed to payment.")
            print("REDIRECTING TO PAYMENT PAGE")

            return redirect('payment:pay', booking_id=booking.id)

            

        except Exception as e:
            
            print(e)
            messages.error(request, "Invalid input.")
            return redirect('booking:create_booking', amenity_id=amenity.id)

    return render(request, 'booking/create_booking.html', {
        'amenity': amenity
    })


# =========================
# SUCCESS PAGE
# =========================
@login_required
def booking_success(request):
    return render(request, 'booking/booking_success.html')


# =========================
# MY BOOKINGS
# =========================
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'booking/my_booking.html', {
        'bookings': bookings
    })


# =========================
# ADMIN DASHBOARD
# =========================
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied")
        return redirect('core:home')

    context = {
        'total_bookings': Booking.objects.count(),
        'pending': Booking.objects.filter(status='pending').count(),
        'confirmed': Booking.objects.filter(status='confirmed').count(),
        'used': Booking.objects.filter(status='used').count(),
        'cancelled': Booking.objects.filter(status='cancelled').count(),
    }

    return render(request, 'booking/admin/dashboard.html', context)


# =========================
# VERIFY TICKET (ADMIN)
# =========================
@login_required
def admin_verify_ticket(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied")
        return redirect('core:home')

    booking = None

    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')

        if not payment_id:
            messages.error(request, "Enter Payment ID")
            return redirect('booking:admin_verify_ticket')

        try:
            booking = Booking.objects.get(payment_id=payment_id)

            if booking.status == 'used':
                messages.warning(request, "Ticket already used")
            elif booking.status == 'cancelled':
                messages.error(request, "Booking cancelled")
            else:
                booking.status = 'used'
                booking.save()
                messages.success(request, "Ticket verified successfully")

        except Booking.DoesNotExist:
            messages.error(request, "Invalid Payment ID")

    return render(request, 'booking/admin/verify_ticket.html', {
        'booking': booking
    })


# =========================
# ADMIN BOOKING LIST
# =========================
@login_required
def admin_booking_list(request):
    if not request.user.is_staff:
        return redirect('core:home')

    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'booking/admin/booking_list.html', {
        'bookings': bookings
    })


# =========================
# ADMIN BOOKING DETAIL
# =========================
@login_required
def admin_booking_detail(request, booking_id):
    if not request.user.is_staff:
        return redirect('core:home')

    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking/admin/booking_detail.html', {
        'booking': booking
    })





# ================= PUBLIC BOOKING VIEW =================


@login_required
def booking_success_view(request, appointment_id):
    """Show booking confirmation"""
    appointment = get_object_or_404(Appointment, id=appointment_id, patient__user=request.user)
    
    context = {
        'appointment': appointment,
    }
    return render(request, 'hospital/booking_success.html', context)


@login_required
def verify_ticket(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.is_verified = True
    booking.status = 'confirmed'
    booking.save()
    messages.success(request, "Ticket verified successfully!")
    return redirect('booking:admin_booking_detail', booking_id=booking_id)














































