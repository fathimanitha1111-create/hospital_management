from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('departments/', views.departments, name='departments'),
    path('appointment/', views.appointment, name='appointment'),
    path('appointment/success/<int:pk>/', views.appointment_success, name='appointment_success'),
    path('appointment/cancel/<int:pk>/', views.cancel_appointment, name='cancel_appointment'),
    path('api/doctors-by-department/<int:dept_id>/', views.api_doctors_by_department, name='api_doctors_by_department'),
    path('register/', views.patient_register, name='patient_register'),
    path('login/', views.patient_login, name='patient_login'),
    path('logout/', views.patient_logout, name='patient_logout'),
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('profile/', views.patient_profile, name='patient_profile'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
]

