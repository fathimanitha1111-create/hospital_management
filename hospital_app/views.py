from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from datetime import date

from .models import Department, Doctor, PatientProfile, Appointment, ContactMessage
from .forms import (
    PatientRegistrationForm,
    AppointmentForm,
    PatientProfileEditForm,
    ContactMessageForm
)


# ---------------------------------------------------------------------
# Public Views
# ---------------------------------------------------------------------

def home(request):
    featured_departments = Department.objects.all()[:4]
    featured_doctors = Doctor.objects.all()[:4]
    
    stats = {
        'doctors': Doctor.objects.count(),
        'departments': Department.objects.count(),
        'patients_healed': 15000 + Appointment.objects.count(),
        'satisfaction_rate': '99.5%'
    }

    return render(request, 'hospital_app/home.html', {
        'featured_departments': featured_departments,
        'featured_doctors': featured_doctors,
        'stats': stats,
    })


def about(request):
    return render(request, 'hospital_app/about.html')


def services(request):
    return render(request, 'hospital_app/services.html')


def departments(request):
    all_departments = Department.objects.all()
    return render(request, 'hospital_app/departments.html', {
        'departments': all_departments,
    })


def doctors(request):
    dept_id = request.GET.get('department')
    search_q = request.GET.get('q', '').strip()

    doctor_qs = Doctor.objects.select_related('department').all()

    if dept_id and dept_id.isdigit():
        doctor_qs = doctor_qs.filter(department_id=int(dept_id))

    if search_q:
        doctor_qs = doctor_qs.filter(
            Q(name__icontains=search_q) |
            Q(specialization__icontains=search_q) |
            Q(qualification__icontains=search_q) |
            Q(department__name__icontains=search_q)
        )

    all_departments = Department.objects.all()

    return render(request, 'hospital_app/doctors.html', {
        'doctors': doctor_qs,
        'departments': all_departments,
        'selected_dept': int(dept_id) if dept_id and dept_id.isdigit() else None,
        'search_q': search_q,
    })


def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor.objects.select_related('department'), pk=pk)
    related_doctors = Doctor.objects.filter(department=doctor.department).exclude(pk=doctor.pk)[:3]

    return render(request, 'hospital_app/doctor_detail.html', {
        'doctor': doctor,
        'related_doctors': related_doctors,
    })


def contact(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your message has been sent to our hospital coordinator.")
            return redirect('contact')
        else:
            messages.error(request, "Please fix the errors in your contact submission.")
    else:
        form = ContactMessageForm()

    return render(request, 'hospital_app/contact.html', {'form': form})


def faq(request):
    return render(request, 'hospital_app/faq.html')


# ---------------------------------------------------------------------
# Appointment Booking & Management
# ---------------------------------------------------------------------

@login_required
def appointment(request):
    initial_data = {}
    doctor_id = request.GET.get('doctor')
    dept_id = request.GET.get('department')

    if doctor_id and doctor_id.isdigit():
        try:
            doc = Doctor.objects.get(pk=int(doctor_id))
            initial_data['doctor'] = doc
            initial_data['department'] = doc.department
        except Doctor.DoesNotExist:
            pass
    elif dept_id and dept_id.isdigit():
        try:
            initial_data['department'] = Department.objects.get(pk=int(dept_id))
        except Department.DoesNotExist:
            pass

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save(commit=False)
            appt.patient = request.user
            appt.status = 'Pending'
            appt.save()

            messages.success(request, f"Your appointment has been successfully scheduled with {appt.doctor.name}!")
            return redirect('appointment_success', pk=appt.pk)
        else:
            messages.error(request, "Please correct the errors in the appointment form.")
    else:
        form = AppointmentForm(initial=initial_data)

    departments_list = Department.objects.all()
    doctors_list = Doctor.objects.all()
    profile, _ = PatientProfile.objects.get_or_create(user=request.user)

    return render(request, 'hospital_app/appointment.html', {
        'form': form,
        'departments': departments_list,
        'doctors': doctors_list,
        'profile': profile,
        'today_date': date.today().strftime('%Y-%m-%d')
    })


@login_required
def appointment_success(request, pk):
    appt = get_object_or_404(Appointment.objects.select_related('doctor', 'department'), pk=pk, patient=request.user)
    return render(request, 'hospital_app/appointment_success.html', {'appointment': appt})


@login_required
def cancel_appointment(request, pk):
    appt = get_object_or_404(Appointment, pk=pk, patient=request.user)
    if appt.status in ['Pending', 'Approved']:
        appt.status = 'Cancelled'
        appt.save()
        messages.success(request, f"Appointment with {appt.doctor.name} has been cancelled.")
    else:
        messages.warning(request, "Completed or already cancelled appointments cannot be cancelled.")
    return redirect('patient_dashboard')


def api_doctors_by_department(request, dept_id):
    doctors_qs = Doctor.objects.filter(department_id=dept_id).values(
        'id', 'name', 'specialization', 'availability'
    )
    return JsonResponse({'doctors': list(doctors_qs)})


# ---------------------------------------------------------------------
# Patient Authentication & Dashboard
# ---------------------------------------------------------------------

def patient_register(request):
    if request.user.is_authenticated:
        return redirect('patient_dashboard')

    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            PatientProfile.objects.create(
                user=user,
                phone=form.cleaned_data.get('phone', ''),
                address='',
                date_of_birth=None
            )

            login(request, user)
            messages.success(request, f"Welcome to CarePulse Hospital, {user.first_name}!")
            return redirect('patient_dashboard')
        else:
            messages.error(request, "Please fix the highlighted errors below to complete your registration.")
    else:
        form = PatientRegistrationForm()

    return render(request, 'hospital_app/patient_register.html', {'form': form})


def patient_login(request):
    if request.user.is_authenticated:
        return redirect('patient_dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Signed in successfully as {user.first_name or user.username}.")

            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('patient_dashboard')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()

    return render(request, 'hospital_app/patient_login.html', {'form': form})


def patient_logout(request):
    logout(request)
    messages.info(request, "You have been logged out safely.")
    return redirect('home')


@login_required
def patient_dashboard(request):
    today = date.today()
    user_appointments = Appointment.objects.filter(patient=request.user).select_related('doctor', 'department')

    upcoming_appointments = user_appointments.filter(
        status__in=['Pending', 'Approved'],
        appointment_date__gte=today
    )
    previous_appointments = user_appointments.exclude(
        id__in=upcoming_appointments.values_list('id', flat=True)
    )

    profile, _ = PatientProfile.objects.get_or_create(user=request.user)

    return render(request, 'hospital_app/patient_dashboard.html', {
        'upcoming_appointments': upcoming_appointments,
        'previous_appointments': previous_appointments,
        'total_count': user_appointments.count(),
        'profile': profile,
    })


@login_required
def patient_profile(request):
    profile, _ = PatientProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = PatientProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            form.save()
            messages.success(request, "Your patient profile has been updated successfully!")
            return redirect('patient_dashboard')
        else:
            messages.error(request, "Please fix the errors in your profile form.")
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = PatientProfileEditForm(instance=profile, initial=initial)

    return render(request, 'hospital_app/patient_profile.html', {
        'form': form,
        'profile': profile,
    })
