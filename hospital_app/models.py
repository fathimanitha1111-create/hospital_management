from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    image = models.CharField(
        max_length=255, 
        default="hospital_app/images/cardiology.jpg",
        help_text="Path to static image e.g. hospital_app/images/cardiology.jpg"
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def doctor_count(self):
        return self.doctors.count()


class Doctor(models.Model):
    name = models.CharField(max_length=150)
    specialization = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='doctors')
    qualification = models.CharField(max_length=200)
    experience = models.CharField(max_length=50, help_text="e.g. 12 Years")
    description = models.TextField()
    image = models.CharField(
        max_length=255, 
        default="hospital_app/images/doctor1.jpg",
        help_text="Path to static image e.g. hospital_app/images/doctor1.jpg"
    )
    availability = models.CharField(max_length=150, default="Mon - Fri, 09:00 AM - 04:00 PM")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.specialization})"


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=30)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    TIME_SLOT_CHOICES = [
        ('09:00 AM - 10:00 AM', '09:00 AM - 10:00 AM'),
        ('10:00 AM - 11:00 AM', '10:00 AM - 11:00 AM'),
        ('11:00 AM - 12:00 PM', '11:00 AM - 12:00 PM'),
        ('01:00 PM - 02:00 PM', '01:00 PM - 02:00 PM'),
        ('02:00 PM - 03:00 PM', '02:00 PM - 03:00 PM'),
        ('03:00 PM - 04:00 PM', '03:00 PM - 04:00 PM'),
        ('04:00 PM - 05:00 PM', '04:00 PM - 05:00 PM'),
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.CharField(max_length=50, choices=TIME_SLOT_CHOICES, default='09:00 AM - 10:00 AM')
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-appointment_date', '-created_at']

    def __str__(self):
        return f"Appointment with {self.doctor.name} for {self.patient.username} on {self.appointment_date}"

    @property
    def badge_class(self):
        mapping = {
            'Pending': 'bg-warning text-dark',
            'Approved': 'bg-success text-white',
            'Completed': 'bg-primary text-white',
            'Cancelled': 'bg-danger text-white',
        }
        return mapping.get(self.status, 'bg-secondary text-white')


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.name}"
