from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from booking.models import Booking
from .models import Payment
from .utils import generate_pdf, send_payment_email

import uuid


# =========================
# START PAYMENT
# =========================
@login_required
def start_payment(request, booking_id):

    booking = get_object_or_404(Booking, id=booking_id)

    # If already confirmed
    if booking.status == "confirmed":
        messages.info(request, "This booking is already paid.")
        return redirect("booking:my_bookings")

    # Create payment if not exists
    payment, created = Payment.objects.get_or_create(
        booking=booking,
        defaults={
            "amount": booking.total_amount,
            "status": "pending",
            "razorpay_order_id": f"ORDER_{uuid.uuid4().hex[:10]}"
        }
    )

    return render(
        request,
        "payment/start_payment.html",
        {
            "booking": booking,
            "payment": payment,
            "amount": booking.total_amount
        }
    )


# =========================
# PAYMENT SUCCESS
# =========================
@csrf_exempt
def payment_success(request):

    if request.method != "POST":
        return redirect("core:home")

    booking_id = request.POST.get("booking_id")

    booking = get_object_or_404(Booking, id=booking_id)
    payment = get_object_or_404(Payment, booking=booking)

    # Prevent duplicate payment
    if payment.status == "completed":
        return render(
            request,
            "payment/payment_success.html",
            {
                "booking": booking
            }
        )

    # Update payment
    payment.status = "completed"
    payment.payment_id = f"PAY_{uuid.uuid4().hex[:8]}"
    payment.save()

    # Update booking
    booking.status = "confirmed"
    booking.save()

    # Generate PDF + send mail
    pdf_file = generate_pdf(booking)
    send_payment_email(booking, pdf_file)

    messages.success(request, "Payment completed successfully!")

    return render(
        request,
        "payment/payment_success.html",
        {
            "booking": booking
        }
    )


# =========================
# PAYMENT FAILED
# =========================
def payment_failed(request):

    return render(
        request,
        "payment/payment_failed.html"
    )


# =========================
# ADMIN PAYMENT LIST
# =========================
@staff_member_required
def payment_list(request):

    payments = Payment.objects.select_related(
        "booking"
    ).order_by("-created_at")

    return render(
        request,
        "payment/admin/payment_list.html",
        {
            "payments": payments
        }
    )


# =========================
# ADMIN PAYMENT DETAIL
# =========================
@staff_member_required
def payment_detail(request, booking_id):

    payment = get_object_or_404(
        Payment,
        booking__id=booking_id
    )

    return render(
        request,
        "payment/admin/payment_detail.html",
        {
            "payment": payment
        }
    )