from django.contrib import admin
from .models import Department, Doctor, PatientProfile, Appointment, ContactMessage


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'department', 'qualification', 'experience', 'availability')
    list_filter = ('department',)
    search_fields = ('name', 'specialization', 'qualification', 'department__name')


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'date_of_birth')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'department', 'appointment_date', 'appointment_time', 'status', 'created_at')
    list_filter = ('status', 'department', 'appointment_date')
    search_fields = ('patient__username', 'patient__first_name', 'doctor__name', 'reason')
    list_editable = ('status',)
    date_hierarchy = 'appointment_date'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
