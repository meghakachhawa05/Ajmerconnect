import requests
from django.conf import settings
from typing import Tuple, Optional
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # ROLE BASED REDIRECTION
            if user.role == "super_admin":
                return redirect("superadmin_dashboard")

            elif user.role == "hospital_admin":
                return redirect("hospital_dashboard")

            elif user.role == "ticket_admin":
                return redirect("ticket_dashboard")

            else:
                return redirect("user_home")

        else:
            messages.error(request, "Invalid username or password!")

    return render(request, "login.html")


def geocode_address(address: str) -> Optional[Tuple[float, float]]:
    """
    Convert address to latitude and longitude using Google Geocoding API
    Returns tuple of (latitude, longitude) or None if geocoding fails
    """
    try:
        # You'll need to add GOOGLE_MAPS_API_KEY to your settings
        api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', None)
        if not api_key:
            return None
            
        url = f"https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            'address': f"{address}, Ajmer, Rajasthan, India",
            'key': api_key
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['status'] == 'OK' and data['results']:
            location = data['results'][0]['geometry']['location']
            return (location['lat'], location['lng'])
        
        return None
        
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two points using Haversine formula
    Returns distance in kilometers
    """
    import math
    
    R = 6371  # Earth's radius in kilometers
    
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

def get_nearby_places(latitude: float, longitude: float, radius_km: float = 5.0):
    """
    Get places within specified radius from given coordinates
    """
    from amenity.models import Amenity
    from hospital.models import Hospital
    
    nearby_amenities = []
    nearby_hospitals = []
    
    # Get amenities within radius
    for amenity in Amenity.objects.filter(latitude__isnull=False, longitude__isnull=False):
        distance = calculate_distance(latitude, longitude, float(amenity.latitude), float(amenity.longitude))
        if distance <= radius_km:
            nearby_amenities.append({
                'amenity': amenity,
                'distance': round(distance, 2)
            })
    
    # Get hospitals within radius
    for hospital in Hospital.objects.filter(latitude__isnull=False, longitude__isnull=False):
        distance = calculate_distance(latitude, longitude, float(hospital.latitude), float(hospital.longitude))
        if distance <= radius_km:
            nearby_hospitals.append({
                'hospital': hospital,
                'distance': round(distance, 2)
            })
    
    return {
        'amenities': sorted(nearby_amenities, key=lambda x: x['distance']),
        'hospitals': sorted(nearby_hospitals, key=lambda x: x['distance'])
    } 