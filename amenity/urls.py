# amenity/urls.py
from django.urls import path
from . import views

app_name = 'amenity'  # important for namespacing

urlpatterns = [
    path('', views.amenity_list, name='list'),                  # List all amenities
    path('<int:pk>/', views.amenity_detail, name='detail'),     # Detail page
    path('create/', views.amenity_create, name='create'),       # Create page
    path('<int:pk>/edit/', views.amenity_edit, name='edit'),    # Edit page
    path('search/', views.amenity_search, name='search'),       # Search
    path('map/add/', views.add_to_map, name='add_to_map'),      # Add to map
    path('delete/<int:pk>/', views.admin_amenity_delete, name = 'delete'),
    # Admin
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/list/', views.admin_amenity_list, name='admin_list'),
    path('admin/add/', views.admin_amenity_add, name='admin_add'),
]
