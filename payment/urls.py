from django.urls import path
from . import views

app_name = 'payment'


urlpatterns = [
    path('pay/<int:booking_id>/', views.start_payment, name='pay'),
    path('success/', views.payment_success, name='payment_success'),
    path('failed/', views.payment_failed, name='payment_failed'),

    # admin
    path('admin/', views.payment_list, name='payment_list'),
    path('admin/<int:booking_id>/', views.payment_detail, name='payment_detail'),
]
