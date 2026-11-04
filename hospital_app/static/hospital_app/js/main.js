/**
 * CarePulse Hospital Management System - Main JavaScript (main.js)
 * Implements interactive features, cascading dropdowns, form validation,
 * date picker constraints, appointment cancellation confirmation, and UI helpers.
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Auto-dismiss Bootstrap alert messages after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            try {
                const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
                bsAlert.close();
            } catch (e) {
                alert.style.display = 'none';
            }
        }, 5000);
    });

    // 2. Prevent past dates in appointment date inputs
    const apptDateInputs = document.querySelectorAll('input[type="date"]#id_appointment_date, input[type="date"].min-today');
    const today = new Date().toISOString().split('T')[0];
    apptDateInputs.forEach(input => {
        if (!input.getAttribute('min')) {
            input.setAttribute('min', today);
        }
    });

    // 3. Dynamic Cascading Dropdown: Department -> Doctor
    const deptSelect = document.getElementById('id_department');
    const doctorSelect = document.getElementById('id_doctor');

    if (deptSelect && doctorSelect) {
        deptSelect.addEventListener('change', function () {
            const deptId = this.value;
            if (!deptId) {
                doctorSelect.innerHTML = '<option value="">-- First Select a Department --</option>';
                return;
            }

            doctorSelect.innerHTML = '<option value="">Loading available doctors...</option>';
            doctorSelect.disabled = true;

            fetch(`/api/doctors-by-department/${deptId}/`)
                .then(response => {
                    if (!response.ok) throw new Error('Network error loading doctors');
                    return response.json();
                })
                .then(data => {
                    doctorSelect.innerHTML = '<option value="">-- Select a Doctor --</option>';
                    if (data.doctors && data.doctors.length > 0) {
                        data.doctors.forEach(doc => {
                            const option = document.createElement('option');
                            option.value = doc.id;
                            option.textContent = `${doc.name} (${doc.specialization})`;
                            doctorSelect.appendChild(option);
                        });
                    } else {
                        const option = document.createElement('option');
                        option.value = '';
                        option.textContent = 'No doctors currently assigned to this department';
                        doctorSelect.appendChild(option);
                    }
                    doctorSelect.disabled = false;
                })
                .catch(err => {
                    console.error('Error fetching doctors:', err);
                    doctorSelect.innerHTML = '<option value="">-- Select a Doctor --</option>';
                    doctorSelect.disabled = false;
                });
        });
    }

    // 4. Live Doctor Search Filter (client-side instantaneous filter)
    const doctorSearchInput = document.getElementById('doctorLiveSearch');
    const doctorCards = document.querySelectorAll('.doctor-card-item');

    if (doctorSearchInput && doctorCards.length > 0) {
        doctorSearchInput.addEventListener('input', function () {
            const term = this.value.toLowerCase().trim();
            doctorCards.forEach(card => {
                const cardText = card.textContent.toLowerCase();
                if (cardText.includes(term)) {
                    card.closest('.doctor-grid-col').style.display = '';
                } else {
                    card.closest('.doctor-grid-col').style.display = 'none';
                }
            });
        });
    }

    // 5. Appointment Cancellation Confirmation
    const cancelButtons = document.querySelectorAll('.btn-confirm-cancel');
    cancelButtons.forEach(btn => {
        btn.addEventListener('click', function (e) {
            const confirmed = confirm("Are you sure you want to cancel this scheduled appointment? This action cannot be undone.");
            if (!confirmed) {
                e.preventDefault();
            }
        });
    });

    // 6. Smooth Scrolling for Anchor Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href.length > 1) {
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });

    // 7. Print Slip Helper
    const printBtns = document.querySelectorAll('.btn-print-slip');
    printBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            window.print();
        });
    });
});

