from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import date, timedelta
from hospital_app.models import Department, Doctor, PatientProfile, Appointment, ContactMessage


class Command(BaseCommand):
    help = "Populates sample departments, doctors, patient profile, and appointments."

    def handle(self, *args, **options):
        self.stdout.write("Seeding sample hospital data...")

        # 1. Admin User
        admin, created = User.objects.get_or_create(username="admin", defaults={
            "email": "admin@carepulse.hospital",
            "first_name": "Hospital",
            "last_name": "Admin",
            "is_staff": True,
            "is_superuser": True
        })
        if created:
            admin.set_password("admin123")
            admin.save()
            self.stdout.write(self.style.SUCCESS("Created admin user: admin / admin123"))

        # 2. Demo Patient User
        patient_user, p_created = User.objects.get_or_create(username="patient", defaults={
            "email": "patient@carepulse.hospital",
            "first_name": "John",
            "last_name": "Doe"
        })
        if p_created:
            patient_user.set_password("patient123")
            patient_user.save()
            PatientProfile.objects.get_or_create(
                user=patient_user,
                defaults={
                    "phone": "+1 (555) 234-5678",
                    "address": "742 Evergreen Healthcare Ave, Medical City",
                    "date_of_birth": date(1992, 6, 15)
                }
            )
            self.stdout.write(self.style.SUCCESS("Created patient user: patient / patient123"))

        # 3. 8 Departments
        departments_data = [
            {
                "name": "Cardiology",
                "description": "Comprehensive cardiac diagnostics, interventional angioplasty, arrhythmia monitoring, and preventative heart care.",
                "image": "hospital_app/images/cardiology.jpg"
            },
            {
                "name": "Neurology",
                "description": "Specialized neurology care, stroke rehabilitation, brain mapping, epilepsy monitoring, and neuro-spine consultation.",
                "image": "hospital_app/images/neurology.jpg"
            },
            {
                "name": "Orthopedics",
                "description": "Robotic joint arthroplasty, sports injury rehabilitation, fracture recovery, and minimally invasive spine surgery.",
                "image": "hospital_app/images/orthopedics.jpg"
            },
            {
                "name": "Pediatrics",
                "description": "Gentle, family-centered infant, child and adolescent medical care, neonatal intensive monitoring, and vaccinations.",
                "image": "hospital_app/images/pediatrics.jpg"
            },
            {
                "name": "Dermatology",
                "description": "Clinical skin pathology, laser therapy, allergy patch testing, cosmetic dermatology, and complex eczema management.",
                "image": "hospital_app/images/dermatology.jpg"
            },
            {
                "name": "Gynecology",
                "description": "Complete maternal care, prenatal ultrasound diagnostics, obstetric delivery suites, and women's wellness checks.",
                "image": "hospital_app/images/gynecology.jpg"
            },
            {
                "name": "General Medicine",
                "description": "Primary adult consultations, chronic hypertension and diabetes monitoring, preventative health screening, and travel medicine.",
                "image": "hospital_app/images/general-medicine.jpg"
            },
            {
                "name": "Dental Care",
                "description": "Full dental restorations, root canal microsurgery, cosmetic teeth whitening, pediatric orthodontics, and implants.",
                "image": "hospital_app/images/dental-care.jpg"
            },
        ]

        depts = {}
        for d in departments_data:
            dept, _ = Department.objects.get_or_create(
                name=d["name"],
                defaults=d
            )
            depts[d["name"]] = dept
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(depts)} departments."))

        # 4. 8 Doctors
        doctors_data = [
            {
                "name": "Dr. Alexander Wright",
                "specialization": "Interventional Cardiology",
                "department": depts["Cardiology"],
                "qualification": "MBBS, MD (Cardiology), FACC",
                "experience": "16 Years",
                "description": "Dr. Wright is a leading interventional cardiologist specializing in coronary artery angioplasty, cardiac catheterization, and preventative heart failure therapy.",
                "image": "hospital_app/images/doctor1.jpg",
                "availability": "Mon - Fri, 09:00 AM - 03:00 PM"
            },
            {
                "name": "Dr. Elena Rostova",
                "specialization": "Cerebrovascular Neurology",
                "department": depts["Neurology"],
                "qualification": "MBBS, MD, PhD (Neuroscience)",
                "experience": "13 Years",
                "description": "Dr. Rostova specializes in stroke recovery, neuro-critical monitoring, migraines, and advanced neuro-imaging diagnostics.",
                "image": "hospital_app/images/doctor2.jpg",
                "availability": "Tue - Sat, 10:00 AM - 04:00 PM"
            },
            {
                "name": "Dr. Marcus Sterling",
                "specialization": "Robotic Joint Replacement",
                "department": depts["Orthopedics"],
                "qualification": "MBBS, MS (Orthopedics), FAAOS",
                "experience": "15 Years",
                "description": "Dr. Sterling has performed over 2,500 minimally invasive robotic knee and hip replacements and serves as orthopedic consultant for collegiate athletes.",
                "image": "hospital_app/images/doctor3.jpg",
                "availability": "Mon, Wed, Fri, 08:30 AM - 02:30 PM"
            },
            {
                "name": "Dr. Sarah Jenkins",
                "specialization": "General Pediatrics & Neonatal Care",
                "department": depts["Pediatrics"],
                "qualification": "MD (Pediatrics), FAAP",
                "experience": "11 Years",
                "description": "Dr. Jenkins brings compassionate and gentle care to children of all ages, from newborn assessments to pediatric growth tracking.",
                "image": "hospital_app/images/doctor4.jpg",
                "availability": "Mon - Fri, 09:00 AM - 04:00 PM"
            },
            {
                "name": "Dr. Emily Thorne",
                "specialization": "Clinical & Aesthetic Dermatology",
                "department": depts["Dermatology"],
                "qualification": "MBBS, MD (Dermatology)",
                "experience": "9 Years",
                "description": "Dr. Thorne offers expertise in chronic skin disorders, autoimmune dermatoses, targeted laser therapies, and allergy care.",
                "image": "hospital_app/images/doctor5.jpg",
                "availability": "Tue, Thu, Sat, 10:00 AM - 05:00 PM"
            },
            {
                "name": "Dr. Michael Chen",
                "specialization": "Obstetrics & Maternal-Fetal Medicine",
                "department": depts["Gynecology"],
                "qualification": "MD (OB/GYN), FACOG",
                "experience": "14 Years",
                "description": "Dr. Chen is dedicated to supporting mothers through high-risk pregnancies, routine prenatal care, and gynecological surgeries.",
                "image": "hospital_app/images/doctor6.jpg",
                "availability": "Mon - Thu, 09:00 AM - 03:00 PM"
            },
            {
                "name": "Dr. David Miller",
                "specialization": "Internal Medicine & Preventative Health",
                "department": depts["General Medicine"],
                "qualification": "MBBS, MD (Internal Medicine)",
                "experience": "17 Years",
                "description": "Dr. Miller leads our adult primary care team, focusing on holistic disease prevention, lifestyle medicine, and multi-system care.",
                "image": "hospital_app/images/doctor7.jpg",
                "availability": "Mon - Fri, 08:00 AM - 02:00 PM"
            },
            {
                "name": "Dr. Sophia Martinez",
                "specialization": "Cosmetic & Restorative Dentistry",
                "department": depts["Dental Care"],
                "qualification": "DDS, MS (Prosthodontics)",
                "experience": "10 Years",
                "description": "Dr. Martinez provides comprehensive dental exams, porcelain crowns, teeth whitening, and comfortable pain-free root canals.",
                "image": "hospital_app/images/doctor8.jpg",
                "availability": "Wed - Sat, 09:30 AM - 04:30 PM"
            },
        ]

        for doc in doctors_data:
            Doctor.objects.get_or_create(
                name=doc["name"],
                department=doc["department"],
                defaults=doc
            )
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(doctors_data)} doctors."))

        # 5. Sample Appointments for Demo Patient
        today = date.today()
        sample_appointments = [
            {
                "patient": patient_user,
                "doctor": Doctor.objects.get(name="Dr. Alexander Wright"),
                "department": depts["Cardiology"],
                "appointment_date": today + timedelta(days=2),
                "appointment_time": "10:00 AM - 11:00 AM",
                "reason": "Routine cardiac checkup and blood pressure assessment.",
                "status": "Approved"
            },
            {
                "patient": patient_user,
                "doctor": Doctor.objects.get(name="Dr. Marcus Sterling"),
                "department": depts["Orthopedics"],
                "appointment_date": today + timedelta(days=5),
                "appointment_time": "01:00 PM - 02:00 PM",
                "reason": "Mild joint inflammation following marathon running.",
                "status": "Pending"
            },
            {
                "patient": patient_user,
                "doctor": Doctor.objects.get(name="Dr. David Miller"),
                "department": depts["General Medicine"],
                "appointment_date": today - timedelta(days=10),
                "appointment_time": "09:00 AM - 10:00 AM",
                "reason": "Annual comprehensive health screening.",
                "status": "Completed"
            }
        ]

        for ap in sample_appointments:
            Appointment.objects.get_or_create(
                patient=ap["patient"],
                doctor=ap["doctor"],
                appointment_date=ap["appointment_date"],
                defaults=ap
            )
        self.stdout.write(self.style.SUCCESS("Loaded sample appointments."))

        # 6. Sample Contact Message
        ContactMessage.objects.get_or_create(
            name="Alice Morgan",
            email="alice@example.com",
            subject="Health Insurance Coverage",
            message="Hello, do you accept Blue Cross Blue Shield for outpatient specialist consultations?",
            defaults={"created_at": today}
        )

        self.stdout.write(self.style.SUCCESS("Data seeding completed successfully!"))
