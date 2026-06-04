from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Amenity
from .forms import AmenityForm, SimpleAmenityForm
from django.views.decorators.http import require_POST

# Create your views here.

def amenity_list(request):
    amenity_type = request.GET.get('type')
    if amenity_type:
        amenities = Amenity.objects.filter(type=amenity_type)
    else:
        amenities = Amenity.objects.all()
    return render(request, 'amenity/amenity_list.html', {
        'amenities': amenities,
        'amenity_type': amenity_type,
    })

def amenity_detail(request, pk):
    amenity = get_object_or_404(Amenity, pk=pk)
    return render(request, 'amenity/amenity_details.html', {
        'amenity': amenity,
    })

def amenity_search(request):
    query = request.GET.get('q', '')
    amenities = []
    
    if query:
        amenities = Amenity.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(type__icontains=query) |
            Q(address__icontains=query)
        )
    
    return render(request, 'amenity/amenity_list.html', {
        'amenities': amenities,
        'query': query,
    })

def amenity_create(request):
    if request.method == 'POST':
        form = AmenityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('amenity:list')
    else:
        form = AmenityForm()
    return render(request, 'amenity/amenity_form.html', {'form': form})

def amenity_edit(request, pk):
    amenity = get_object_or_404(Amenity, pk=pk)
    if request.method == 'POST':
        form = AmenityForm(request.POST, request.FILES, instance=amenity)
        if form.is_valid():
            form.save()
            return redirect('amenity:detail', pk=amenity.pk)
    else:
        form = AmenityForm(instance=amenity)
    return render(request, 'amenity/amenity_form.html', {'form': form, 'amenity': amenity})

def add_to_map(request):
    if request.method == 'POST':
        form = SimpleAmenityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:map')  # Redirect to map page after adding
    else:
        form = SimpleAmenityForm()
    return render(request, 'amenity/add_to_map.html', {'form': form})
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('core:home')

    context = {
        'total_amenities': Amenity.objects.count(),
        'featured_count': Amenity.objects.filter(is_featured=True).count(),
    }
    return render(request, 'amenity/admin/dashboard.html', context)


@login_required
def admin_amenity_list(request):
    if not request.user.is_staff:
        return redirect('core:home')

    amenities = Amenity.objects.all()
    return render(request, 'amenity/admin/amenity_list.html', {
        'amenities': amenities
    })


@login_required
def admin_amenity_add(request):
    if not request.user.is_staff:
        return redirect('core:home')

    if request.method == 'POST':
        form = AmenityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('amenity:admin_list')
    else:
        form = AmenityForm()

    return render(request, 'amenity/admin/amenity_form.html', {'form': form})


from django.views.decorators.http import require_POST

@login_required
@require_POST
def admin_amenity_delete(request, pk):
    if not request.user.is_staff:
        return redirect('core:home')

    amenity = get_object_or_404(Amenity, pk=pk)
    amenity.delete()
    return redirect('amenity:admin_list')
