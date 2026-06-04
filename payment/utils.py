# payment/utils.py

from reportlab.pdfgen import canvas
from django.conf import settings
import os
from django.core.mail import EmailMessage


def generate_pdf(booking):
    """
    Generate ticket PDF for booking
    """
    folder = os.path.join(settings.MEDIA_ROOT, "tickets")
    os.makedirs(folder, exist_ok=True)

    file_path = os.path.join(folder, f"ticket_{booking.id}.pdf")

    c = canvas.Canvas(file_path)
    c.setFont("Helvetica", 12)

    c.drawString(50, 800, "AJMER CONNECT - TICKET")
    c.drawString(50, 770, f"Booking ID: {booking.id}")
    c.drawString(50, 750, f"Name: {booking.visitor_name}")
    c.drawString(50, 730, f"Amount Paid: ₹{booking.total_amount}")
    c.drawString(50, 710, "Status: CONFIRMED")

    c.showPage()
    c.save()

    return file_path


def send_payment_email(booking, pdf_path):
    """
    Send ticket email (can be console email in dev)
    """
    email = EmailMessage(
        subject="Your Ajmer Connect Ticket",
        body=f"Hi {booking.visitor_name},\n\nYour booking is confirmed.",
        to=[booking.user.email]
    )

    if pdf_path:
        email.attach_file(pdf_path)

    email.send()
