# 🏥 CarePulse - Complete Hospital Management System

A modern, responsive, and fully functional Hospital Management System website built with **Python 3.12+**, **Django 5.x**, **SQLite**, **HTML5**, **CSS3**, **Bootstrap 5**, **JavaScript**, and **Bootstrap Icons**.

---

## 🎨 Color Combination & Visual Theme

The website adheres to a clean, healthcare-inspired color palette:
- **Primary:** Light Green (`#A5D6A7`)
- **Secondary:** White (`#FFFFFF`)
- **Background:** Very Light Green (`#F1F8F2`)
- **Dark Green:** (`#1B5E20`)
- **Button Green:** (`#2E8B57`)
- **Text:** Dark Gray (`#333333`)

---

## 📁 Exact Project Structure

```
hospital_project/
│
├── manage.py
├── db.sqlite3
├── requirements.txt
├── README.md
├── .gitignore
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── hospital_app/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── forms.py
    ├── tests.py
    │
    ├── management/
    │   └── commands/
    │       └── seed_data.py
    │
    ├── templates/
    │   └── hospital_app/
    │       ├── base.html
    │       ├── home.html
    │       ├── about.html
    │       ├── services.html
    │       ├── doctors.html
    │       ├── doctor_detail.html
    │       ├── departments.html
    │       ├── appointment.html
    │       ├── appointment_success.html
    │       ├── patient_register.html
    │       ├── patient_login.html
    │       ├── patient_dashboard.html
    │       ├── patient_profile.html
    │       ├── contact.html
    │       └── faq.html
    │
    └── static/
        └── hospital_app/
            ├── css/
            │   ├── style.css
            │   ├── home.css
            │   ├── about.css
            │   ├── services.css
            │   ├── doctors.css
            │   ├── doctor_detail.css
            │   ├── departments.css
            │   ├── appointment.css
            │   ├── patient_register.css
            │   ├── patient_login.css
            │   ├── patient_dashboard.css
            │   ├── patient_profile.css
            │   ├── contact.css
            │   └── faq.css
            │
            ├── js/
            │   └── main.js
            │
            └── images/
                ├── hospital-logo.png
                ├── hospital-banner.jpg
                ├── hospital-building.jpg
                ├── hospital-interior.jpg
                ├── doctor1.jpg
                ├── doctor2.jpg
                ├── doctor3.jpg
                ├── doctor4.jpg
                ├── doctor5.jpg
                ├── doctor6.jpg
                ├── cardiology.jpg
                ├── neurology.jpg
                ├── orthopedics.jpg
                ├── pediatrics.jpg
                ├── dermatology.jpg
                ├── gynecology.jpg
                ├── general-medicine.jpg
                ├── dental-care.jpg
                ├── emergency-care.jpg
                ├── laboratory.jpg
                ├── pharmacy.jpg
                └── ambulance.jpg
```

---

## 🖼️ List of 22 Locally Saved Images

All images are stored locally under `hospital_app/static/hospital_app/images/`:
1. `hospital-logo.png`
2. `hospital-banner.jpg`
3. `hospital-building.jpg`
4. `hospital-interior.jpg`
5. `doctor1.jpg`
6. `doctor2.jpg`
7. `doctor3.jpg`
8. `doctor4.jpg`
9. `doctor5.jpg`
10. `doctor6.jpg`
11. `cardiology.jpg`
12. `neurology.jpg`
13. `orthopedics.jpg`
14. `pediatrics.jpg`
15. `dermatology.jpg`
16. `gynecology.jpg`
17. `general-medicine.jpg`
18. `dental-care.jpg`
19. `emergency-care.jpg`
20. `laboratory.jpg`
21. `pharmacy.jpg`
22. `ambulance.jpg`

---

## 📑 15 Distinct HTML Pages

1. **`base.html`** - Master responsive layout with navigation, top helpline bar, flash messages, and footer.
2. **`home.html`** - Hero banner, hospital introduction, key statistics, featured doctors, departments, and testimonials.
3. **`about.html`** - History, mission, vision, hospital building, interior facilities, and accreditations.
4. **`services.html`** - Service cards for Emergency Care, Laboratory, Pharmacy, ICU, Ambulance, General Consultation, and Diagnostic Imaging.
5. **`doctors.html`** - Doctors directory with live name search, department filter pills, qualifications, and booking buttons.
6. **`doctor_detail.html`** - In-depth profile, specialization, experience, biography, availability, and consultation scheduling.
7. **`departments.html`** - Department cards for Cardiology, Neurology, Orthopedics, Pediatrics, Dermatology, Gynecology, General Medicine, and Dental Care.
8. **`appointment.html`** - Interactive booking form with cascading Department ➔ Doctor dynamic dropdown and date picker validation.
9. **`appointment_success.html`** - Confirmation screen with consultation summary and printable slip.
10. **`patient_register.html`** - New patient account creation with password hashing and validation.
11. **`patient_login.html`** - Secure patient sign-in with quick-fill demo buttons and password recovery guidance.
12. **`patient_dashboard.html`** - Private portal showing only the logged-in patient's upcoming and previous appointments with cancellation capability.
13. **`patient_profile.html`** - View and edit personal contact information, residential address, and date of birth.
14. **`contact.html`** - Campus address, helpline, visiting hours, interactive map card, and inquiry form saving directly to SQLite.
15. **`faq.html`** - Interactive Bootstrap accordion with categorized appointment, doctor availability, and patient registration questions.

---

## 🗄️ Database Models (SQLite)

- **`Department`**: `name`, `description`, `image`
- **`Doctor`**: `name`, `specialization`, `department` (ForeignKey), `qualification`, `experience`, `description`, `image`, `availability`
- **`PatientProfile`**: `user` (OneToOneField with User), `phone`, `address`, `date_of_birth`
- **`Appointment`**: `patient` (ForeignKey to User), `doctor` (ForeignKey to Doctor), `department` (ForeignKey to Department), `appointment_date`, `appointment_time`, `reason`, `status` (`Pending`, `Approved`, `Completed`, `Cancelled`), `created_at`
- **`ContactMessage`**: `name`, `email`, `subject`, `message`, `created_at`

---

## ⚡ Quick Start Guide

### 1. Install Dependencies
```bash
py -m pip install -r requirements.txt
```

### 2. Run Database Migrations
```bash
py manage.py makemigrations
py manage.py migrate
```

### 3. Populate Sample Data
```bash
py manage.py seed_data
```

### 4. Run the Development Server
```bash
py manage.py runserver
```

Open your browser and navigate to: **`http://127.0.0.1:8000/`**

---

## 🔑 Pre-Configured Demo Credentials

| Role | Username | Password | Access |
| :--- | :--- | :--- | :--- |
| **Demo Patient** | `patient` | `patient123` | Patient Portal (`/dashboard/`, `/appointment/`) |
| **Hospital Admin** | `admin` | `admin123` | Full Admin Panel (`/admin/`) |

---

## 🧪 Automated Testing

Execute the comprehensive test suite (16 tests covering models, forms, image files, security, and views):
```bash
py manage.py test hospital_app
```

---

## 🚀 GitHub Upload Instructions

Run the following commands to commit your repository:
```bash
git init
git add .
git status
git commit -m "Initial commit - Hospital Management System"
```

To push to your remote GitHub repository:
```bash
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git branch -M main
git push -u origin main
```
