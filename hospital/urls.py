from django.urls import path
from . import views

urlpatterns = [
    # Public Pages
    path('', views.home, name='home'),
    path('patient-reviews.html', views.patient_reviews, name='patient_reviews'),
    path('about.html', views.about, name='about'),
    path('contact.html', views.contact, name='contact'),
    path('department.html', views.department, name='department'),

    # Authentication
    path('login.html', views.login, name='login'),  # Renamed view function
    path('signup.html', views.signup, name='signup'),

    # Admin Section
    path('admin_dashboard.html', views.admin_dashboard, name='admin_dashboard'),
    path('admin_feedback.html', views.admin_feedback, name='admin_feedback'),
    path('admin_logout.html', views.admin_logout, name='admin_logout'),
    path('admin_reports.html', views.admin_reports, name='admin_reports'),
    path('approve-user/<int:profile_id>/', views.approve_user, name='approve_user'),


    # Management
    path('manage_patients.html', views.manage_patients, name='manage_patients'),
    path('manage_doctors.html', views.manage_doctors, name='manage_doctors'),
    path('manage_appointments.html', views.manage_appointments, name='manage_appointments'),

    # Patient Section
    path('patient_dashboard.html', views.patient_dashboard, name='patient_dashboard'),
    path('patient-registration.html', views.patient_registration, name='patient_registration'),
    path('book_appointment.html', views.book_appointment, name='book_appointment'),
    path('appointments.html', views.appointment, name='appointments'),
    path('cancel-appointment.html', views.cancel_appointment, name='cancel_appointment'),
    path('medical-history.html', views.medical_history, name='medical_history'),
    path('settings-and-logout.html', views.settings_and_logout, name='settings_and_logout'),
    path('patient_home.html', views.patient_home, name='patient_home'),

    # Doctor Section
    path('doctor-home.html', views.doctor_home, name='doctor_home'),
    path('doctor-dashboard.html', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor-logout.html', views.doctor_logout, name='doctor_logout'),
]
