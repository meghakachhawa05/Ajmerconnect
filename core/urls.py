from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='user_login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('map/', views.map_view, name='map'),
    path('hospital/', views.hospital_redirect, name='hospital'),
    path('my-account/', views.my_account, name='my_account'),

    # Amenity URLs
    path('amenity/', include('amenity.urls')),

    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('password-reset-sent/<str:reset_id>/', views.password_reset_sent, name='password_reset_sent'),
    path('reset-password/<str:reset_id>/', views.reset_password, name='reset_password'),
    path("dashboard/", views.dashboard_router, name="dashboard_router"),
    path('nominatim-search/', views.nominatim_search, name='nominatim_search'),

]
