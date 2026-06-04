from django.test import TestCase
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from booking.models import Booking
from .models import Payment
from unittest.mock import patch

# Create your tests here.

class PaymentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()
        self.client.login(username='testuser', password='testpass')
        # Create a dummy amenity if required by your Booking model
        from amenity.models import Amenity
        self.amenity = Amenity.objects.create(
            name='Test Park', type='park', address='Test Address', latitude=26.0, longitude=74.0
        )
        self.booking = Booking.objects.create(
            user=self.user,
            amenity=self.amenity,
            booking_date='2024-12-31',
            num_tickets=1,
            amount_per_ticket=100,
            total_amount=100,
            visitor_name='Test Visitor',
            visitor_phone='1234567890',
        )

    def test_payment_model_creation(self):
        payment = Payment.objects.create(
            user=self.user,
            order_id='order_test123',
            amount=100,
            status='created',
            booking=self.booking
        )
        self.assertEqual(str(payment), f"{self.user.username} - order_test123 - created")

    @patch('razorpay.Client')
    def test_initiate_payment_view_logged_in(self, mock_razorpay_client):
        mock_order = {'id': 'order_test123'}
        mock_razorpay_client.return_value.order.create.return_value = mock_order
        response = self.client.get(reverse('pyment:pay', args=[self.booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pyment/payment.html')
        self.assertIn('payment', response.context)
        self.assertIn('booking', response.context)
        self.assertTrue(Payment.objects.filter(order_id='order_test123').exists())

    def test_initiate_payment_view_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('pyment:pay', args=[self.booking.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    @patch('razorpay.Client')
    def test_initiate_payment_view_nonexistent_booking(self, mock_razorpay_client):
        response = self.client.get(reverse('pyment:pay', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_payment_success_view(self):
        payment = Payment.objects.create(
            user=self.user,
            order_id='order_test123',
            amount=100,
            status='created',
            booking=self.booking
        )
        data = {
            'razorpay_order_id': 'order_test123',
            'razorpay_payment_id': 'pay_test123',
            'razorpay_signature': 'sig_test123',
        }
        response = self.client.post(reverse('pyment:payment_success'), data)
        payment.refresh_from_db()
        self.booking.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(payment.status, 'paid')
        self.assertEqual(payment.payment_id, 'pay_test123')
        self.assertEqual(self.booking.status, 'paid')
        self.assertTemplateUsed(response, 'pyment/payment_success.html')

    def test_payment_success_view_invalid_order(self):
        data = {
            'razorpay_order_id': 'invalid_order',
            'razorpay_payment_id': 'pay_test123',
            'razorpay_signature': 'sig_test123',
        }
        response = self.client.post(reverse('pyment:payment_success'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pyment/payment_failed.html')

    def test_double_payment_attempt(self):
        payment = Payment.objects.create(
            user=self.user,
            order_id='order_test123',
            amount=100,
            status='paid',
            booking=self.booking
        )
        data = {
            'razorpay_order_id': 'order_test123',
            'razorpay_payment_id': 'pay_test123',
            'razorpay_signature': 'sig_test123',
        }
        response = self.client.post(reverse('pyment:payment_success'), data)
        payment.refresh_from_db()
        self.assertEqual(payment.status, 'paid')  # Should remain paid, not error

    def test_payment_for_already_paid_booking(self):
        self.booking.status = 'paid'
        self.booking.save()
        @patch('razorpay.Client')
        def _test(mock_razorpay_client):
            mock_order = {'id': 'order_test123'}
            mock_razorpay_client.return_value.order.create.return_value = mock_order
            response = self.client.get(reverse('pyment:pay', args=[self.booking.id]))
            self.assertEqual(response.status_code, 200)
            # You may want to add logic to prevent payment for already paid bookings
        _test()

