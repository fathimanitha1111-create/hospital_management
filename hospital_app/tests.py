import os
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from datetime import date, timedelta
from hospital_app.models import Department, Doctor, PatientProfile, Appointment, ContactMessage


class HospitalSystemComprehensiveTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create department
        self.department = Department.objects.create(
            name="Cardiology",
            description="Heart care and angioplasty diagnostics.",
            image="hospital_app/images/cardiology.jpg"
        )

        self.dept2 = Department.objects.create(
            name="Neurology",
            description="Brain and spine care.",
            image="hospital_app/images/neurology.jpg"
        )

        # Create doctors
        self.doctor1 = Doctor.objects.create(
            name="Dr. Alexander Wright",
            specialization="Interventional Cardiology",
            department=self.department,
            qualification="MBBS, MD (Cardiology)",
            experience="16 Years",
            description="Specialist in coronary interventions.",
            image="hospital_app/images/doctor1.jpg",
            availability="Mon - Fri, 09:00 AM - 03:00 PM"
        )

        self.doctor2 = Doctor.objects.create(
            name="Dr. Elena Rostova",
            specialization="Cerebrovascular Neurology",
            department=self.dept2,
            qualification="MBBS, MD, PhD",
            experience="13 Years",
            description="Specialist in stroke and neurology.",
            image="hospital_app/images/doctor2.jpg",
            availability="Tue - Sat, 10:00 AM - 04:00 PM"
        )

        # Create demo patient user
        self.patient_user = User.objects.create_user(
            username="patient_test",
            password="testpassword123",
            first_name="Jane",
            last_name="Doe",
            email="janedoe@example.com"
        )
        self.patient_profile = PatientProfile.objects.create(
            user=self.patient_user,
            phone="+1 (555) 000-1111",
            address="123 Hospital Lane",
            date_of_birth=date(1995, 4, 10)
        )

        # Create another user for permission testing
        self.other_user = User.objects.create_user(
            username="other_patient",
            password="testpassword123"
        )

    # 1. Verify Image Files Exist Locally
    def test_all_22_images_exist(self):
        required_images = [
            "hospital-logo.png",
            "hospital-banner.jpg",
            "hospital-building.jpg",
            "hospital-interior.jpg",
            "doctor1.jpg",
            "doctor2.jpg",
            "doctor3.jpg",
            "doctor4.jpg",
            "doctor5.jpg",
            "doctor6.jpg",
            "cardiology.jpg",
            "neurology.jpg",
            "orthopedics.jpg",
            "pediatrics.jpg",
            "dermatology.jpg",
            "gynecology.jpg",
            "general-medicine.jpg",
            "dental-care.jpg",
            "emergency-care.jpg",
            "laboratory.jpg",
            "pharmacy.jpg",
            "ambulance.jpg"
        ]
        images_dir = os.path.join(settings.BASE_DIR, "hospital_app", "static", "hospital_app", "images")
        for img_name in required_images:
            path = os.path.join(images_dir, img_name)
            self.assertTrue(os.path.exists(path), f"Missing required image: {img_name}")
            self.assertGreater(os.path.getsize(path), 0, f"Empty image file: {img_name}")

    # 2. Public Pages
    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CarePulse")
        self.assertContains(response, "Cardiology")

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pioneering Clinical Excellence")

    def test_services_page(self):
        response = self.client.get(reverse('services'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Emergency & Trauma Care")

    def test_departments_page(self):
        response = self.client.get(reverse('departments'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cardiology")
        self.assertContains(response, "Neurology")

    def test_doctors_directory_and_search(self):
        # All doctors
        response = self.client.get(reverse('doctors'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dr. Alexander Wright")
        self.assertContains(response, "Dr. Elena Rostova")

        # Search by query
        search_res = self.client.get(reverse('doctors'), {'q': 'Alexander'})
        self.assertEqual(search_res.status_code, 200)
        self.assertContains(search_res, "Dr. Alexander Wright")
        self.assertNotContains(search_res, "Dr. Elena Rostova")

        # Filter by department
        dept_res = self.client.get(reverse('doctors'), {'department': self.department.id})
        self.assertEqual(dept_res.status_code, 200)
        self.assertContains(dept_res, "Dr. Alexander Wright")
        self.assertNotContains(dept_res, "Dr. Elena Rostova")

    def test_doctor_detail_page(self):
        response = self.client.get(reverse('doctor_detail', kwargs={'pk': self.doctor1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dr. Alexander Wright")
        self.assertContains(response, "16 Years")

    def test_faq_page(self):
        response = self.client.get(reverse('faq'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Frequently Asked Questions")

    def test_contact_form(self):
        data = {
            'name': 'Visitor Alice',
            'email': 'alice@example.com',
            'subject': 'Insurance question',
            'message': 'Do you take Anthem insurance?'
        }
        response = self.client.post(reverse('contact'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ContactMessage.objects.filter(email='alice@example.com').exists())

    # 3. Patient Authentication
    def test_patient_registration(self):
        reg_data = {
            'first_name': 'Mark',
            'last_name': 'Taylor',
            'email': 'markt@example.com',
            'phone': '555-4433',
            'username': 'marktaylor',
            'password': 'StrongPassword123!',
            'confirm_password': 'StrongPassword123!'
        }
        response = self.client.post(reverse('patient_register'), data=reg_data)
        self.assertEqual(response.status_code, 302)
        user = User.objects.filter(username='marktaylor').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('StrongPassword123!'))
        self.assertTrue(PatientProfile.objects.filter(user=user).exists())

    def test_patient_login_and_logout(self):
        login_res = self.client.post(reverse('patient_login'), data={
            'username': 'patient_test',
            'password': 'testpassword123'
        })
        self.assertEqual(login_res.status_code, 302)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.patient_user.pk)

        logout_res = self.client.get(reverse('patient_logout'))
        self.assertEqual(logout_res.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)

    # 4. Appointment Booking & Cancellation
    def test_appointment_booking(self):
        self.client.login(username='patient_test', password='testpassword123')
        tomorrow = date.today() + timedelta(days=3)
        booking_data = {
            'department': self.department.id,
            'doctor': self.doctor1.id,
            'appointment_date': tomorrow.strftime('%Y-%m-%d'),
            'appointment_time': '10:00 AM - 11:00 AM',
            'reason': 'Blood pressure checkup'
        }
        response = self.client.post(reverse('appointment'), data=booking_data)
        self.assertEqual(response.status_code, 302)

        appt = Appointment.objects.filter(patient=self.patient_user, doctor=self.doctor1).first()
        self.assertIsNotNone(appt)
        self.assertEqual(appt.status, 'Pending')

    def test_appointment_cancellation(self):
        self.client.login(username='patient_test', password='testpassword123')
        tomorrow = date.today() + timedelta(days=2)
        appt = Appointment.objects.create(
            patient=self.patient_user,
            doctor=self.doctor1,
            department=self.department,
            appointment_date=tomorrow,
            appointment_time='09:00 AM - 10:00 AM',
            reason='Routine visit',
            status='Approved'
        )

        cancel_res = self.client.get(reverse('cancel_appointment', kwargs={'pk': appt.pk}))
        self.assertEqual(cancel_res.status_code, 302)
        appt.refresh_from_db()
        self.assertEqual(appt.status, 'Cancelled')

    def test_patient_cannot_cancel_others_appointment(self):
        # Patient A owns an appointment
        tomorrow = date.today() + timedelta(days=2)
        appt = Appointment.objects.create(
            patient=self.patient_user,
            doctor=self.doctor1,
            department=self.department,
            appointment_date=tomorrow,
            appointment_time='09:00 AM - 10:00 AM',
            reason='Routine visit',
            status='Approved'
        )

        # Other user logs in and tries to cancel Patient A's appointment
        self.client.login(username='other_patient', password='testpassword123')
        cancel_res = self.client.get(reverse('cancel_appointment', kwargs={'pk': appt.pk}))
        # Must return 404 (not authorized to touch other patient's record)
        self.assertEqual(cancel_res.status_code, 404)
        appt.refresh_from_db()
        self.assertEqual(appt.status, 'Approved')

    # 5. Patient Profile Edit
    def test_patient_profile_edit(self):
        self.client.login(username='patient_test', password='testpassword123')
        profile_data = {
            'first_name': 'Janet',
            'last_name': 'Doe-Smith',
            'email': 'janet@example.com',
            'phone': '+1 (555) 999-8888',
            'address': '456 New Healthcare Blvd',
            'date_of_birth': '1995-04-10'
        }
        res = self.client.post(reverse('patient_profile'), data=profile_data)
        self.assertEqual(res.status_code, 302)

        self.patient_user.refresh_from_db()
        self.patient_profile.refresh_from_db()
        self.assertEqual(self.patient_user.first_name, 'Janet')
        self.assertEqual(self.patient_profile.phone, '+1 (555) 999-8888')

    # 6. Cascading API
    def test_api_doctors_by_department(self):
        res = self.client.get(reverse('api_doctors_by_department', kwargs={'dept_id': self.department.id}))
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue('doctors' in data)
        self.assertEqual(len(data['doctors']), 1)
        self.assertEqual(data['doctors'][0]['name'], 'Dr. Alexander Wright')
