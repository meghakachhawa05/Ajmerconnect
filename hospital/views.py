from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from datetime import date

from .models import Doctor, Slot, Appointment, Hospital, Patient
from .forms import (
    DoctorForm,
    SlotForm,
    SlotEditForm,
    HospitalForm,
    AppointmentBookingForm
)


# ================= PUBLIC VIEWS =================

def public_hospital_list(request):
    hospitals = Hospital.objects.filter(is_active=True)

    return render(request, 'hospital/public_hospital_list.html', {
        'hospitals': hospitals
    })


def public_hospital_detail(request, pk):

    hospital = get_object_or_404(
        Hospital,
        pk=pk,
        is_active=True
    )

    doctors = Doctor.objects.filter(
        hospital=hospital,
        is_active=True
    )

    slots = Slot.objects.filter(
        doctor__hospital=hospital,
        is_active=True,
        date__gte=date.today(),
        booked_count__lt=F('max_patients')
    ).select_related('doctor')

    context = {
        'hospital': hospital,
        'doctors': doctors,
        'slots': slots,
    }

    return render(request, 'hospital/public_hospital_detail.html', context)


# ================= DOCTOR =================

@login_required
def doctor_list(request):

    hospitals = Hospital.objects.filter(admin=request.user)

    doctors = Doctor.objects.filter(
        hospital__in=hospitals
    )

    return render(request, 'hospital/doctor_list.html', {
        'doctors': doctors
    })


@login_required
def doctor_create(request):

    hospital = Hospital.objects.filter(
        admin=request.user
    ).first()

    form = DoctorForm(request.POST or None)

    if form.is_valid():

        doctor = form.save(commit=False)

        doctor.hospital = hospital

        doctor.save()

        return redirect('hospital:doctor_list')

    return render(request, 'hospital/doctor_form.html', {
        'form': form
    })


@login_required
def doctor_edit(request, pk):

    hospitals = Hospital.objects.filter(
        admin=request.user
    )

    doctor = get_object_or_404(
        Doctor,
        pk=pk,
        hospital__in=hospitals
    )

    form = DoctorForm(
        request.POST or None,
        instance=doctor
    )

    if form.is_valid():

        form.save()

        return redirect('hospital:doctor_list')

    return render(request, 'hospital/doctor_form.html', {
        'form': form
    })
@login_required
def doctor_details(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'hospital/doctor_detail.html', {'doctor': doctor})

# ================= SLOT =================

@login_required
def slot_list(request):

    hospitals = Hospital.objects.filter(
        admin=request.user
    )

    slots = Slot.objects.filter(
        doctor__hospital__in=hospitals
    )

    return render(request, 'hospital/slot_list.html', {
        'slots': slots
    })


@login_required
def slot_create(request):

    doctors = Doctor.objects.filter(
        hospital__admin=request.user
    )

    if request.method == 'POST':

        form = SlotForm(request.POST)

        form.fields['doctor'].queryset = doctors

        if form.is_valid():

            form.save()

            return redirect('hospital:slot_manage')

        else:

            print(form.errors)

    else:

        form = SlotForm()

        form.fields['doctor'].queryset = doctors

    return render(request, 'hospital/dashboard/create_slot.html', {
        'form': form
    })


@login_required
def slot_edit(request, pk):

    hospitals = Hospital.objects.filter(
        admin=request.user
    )

    slot = get_object_or_404(
        Slot,
        pk=pk,
        doctor__hospital__in=hospitals
    )

    form = SlotForm(
        request.POST or None,
        instance=slot
    )

    if form.is_valid():

        form.save()

        return redirect('hospital:slot_list')

    return render(request, 'hospital/slot_form.html', {
        'form': form
    })


# ================= HOSPITAL =================

@login_required
def hospital_list(request):

    hospitals = Hospital.objects.filter(
        admin=request.user
    )

    return render(request, 'hospital/hospital_list.html', {
        'hospitals': hospitals
    })


@login_required
def hospital_create(request):

    form = HospitalForm(request.POST or None)

    if form.is_valid():

        hospital = form.save(commit=False)

        hospital.admin = request.user

        hospital.save()

        return redirect('hospital:hospital_list')

    return render(request, 'hospital/hospital_form.html', {
        'form': form
    })


# ================= DASHBOARD SLOT =================

@login_required
def slot_manage(request):

    hospitals = Hospital.objects.filter(
        admin=request.user
    )

    slots = Slot.objects.filter(
        doctor__hospital__in=hospitals
    )

    return render(request, 'hospital/dashboard/slot_manage.html', {
        'slots': slots
    })


@login_required
def edit_slot(request, slot_id):

    hospitals = Hospital.objects.filter(
        admin=request.user
    )

    slot = get_object_or_404(
        Slot,
        id=slot_id,
        doctor__hospital__in=hospitals
    )

    if request.method == 'POST':

        form = SlotEditForm(
            request.POST,
            instance=slot
        )

        if form.is_valid():

            form.save()

            return redirect('hospital:slot_manage')

    else:

        form = SlotEditForm(instance=slot)

    return render(request, 'hospital/dashboard/edit_slot.html', {
        'form': form
    })


# ================= DASHBOARD APPOINTMENT =================

@login_required
def appointment_list(request):

    hospitals = Hospital.objects.filter(
        admin=request.user
    )

    appointments = Appointment.objects.filter(
        slot__doctor__hospital__in=hospitals
    ).order_by('-created_at')

    return render(request, 'hospital/dashboard/appointment_list.html', {
        'appointments': appointments
    })


@login_required
def update_appointment_status(request, appointment_id, status):

    hospitals = Hospital.objects.filter(
        admin=request.user
    )

    if status not in dict(Appointment.STATUS_CHOICES):

        return redirect('hospital:appointment_list')

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        slot__doctor__hospital__in=hospitals
    )

    appointment.status = status

    appointment.save()

    return redirect('hospital:appointment_list')


# ================= DASHBOARD HOME =================

@login_required
def dashboard_home(request):

    hospital = Hospital.objects.filter(
        admin=request.user
    ).first()

    if not hospital:

        return render(request, "hospital/no_hospital.html")

    doctors = Doctor.objects.filter(
        hospital=hospital
    )

    appointments = Appointment.objects.filter(
        slot__doctor__hospital=hospital
    ).order_by("-id")[:10]

    context = {
        "hospital": hospital,
        "doctors": doctors,
        "appointments": appointments
    }

    return render(request, "hospital/dashboard.html", context)


# ================= APPOINTMENT BOOKING =================

@login_required
def book_appointment_view(request, hospital_id):

    hospital = get_object_or_404(
        Hospital,
        pk=hospital_id,
        is_active=True
    )

    doctors = Doctor.objects.filter(
        hospital=hospital,
        is_active=True
    )

    available_slots = Slot.objects.filter(
        doctor__hospital=hospital,
        is_active=True,
        date__gte=date.today(),
        booked_count__lt=F('max_patients')
    ).select_related('doctor')

    if request.method == 'POST':

        form = AppointmentBookingForm(request.POST)

        if form.is_valid():


            patient = Patient.objects.create(
                user=request.user,
                phone_number=form.cleaned_data['contact'],
                gender='O',
                emergency_contact=form.cleaned_data['contact'],
)


            slot = Slot.objects.get(id=form.cleaned_data['slot_id'])

            if slot.booked_count >= slot.max_patients:
                messages.error(request, "Slot is full")
                return redirect('hospital:public_hospital_detail', pk=hospital.id)

            appointment = Appointment.objects.create(
                patient=patient,
                slot=slot,
                date=slot.date,
                status='pending'
            )

            slot.booked_count += 1
            slot.save()

            messages.success(request, f'Appointment booked! ID: {appointment.id}')
            return redirect('hospital:booking_success', appointment_id=appointment.id)

    else:
        form = AppointmentBookingForm()

    context = {
        'hospital': hospital,
        'doctors': doctors,
        'slots': available_slots,
        'form': form,
    }

    return render(request, 'hospital/book_appointment.html', context)

@login_required
def booking_success_view(request, appointment_id):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient__user=request.user
    )

    return render(request, 'hospital/booking_success.html', {
        'appointment': appointment
    })