from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
User.objects.all()


# ================= Home & Public Pages =================

def home(request):
    return render(request, 'home.html')

def patient_reviews(request):
    return render(request, 'patient-reviews.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def department(request):
    return render(request, 'department.html')


# ================= User Signup =================

# def signup(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         phone = request.POST.get('phone')
#         role = request.POST.get('role')
#         specialization = request.POST.get('specialization')

#         # Validate that role is selected
#         if not role:
#             messages.error(request, "Please select a role.")
#             return render(request, 'signup.html')

#         # If doctor, specialization required (optional)
#         if role == 'doctor' and not specialization:
#             messages.error(request, "Please enter specialization for doctor role.")
#             return render(request, 'signup.html')

#         try:
#             # Prevent duplicate users
#             if User.objects.filter(username=email).exists():
#                 messages.error(request, "A user with this email already exists.")
#                 return render(request, 'signup.html')

#             # Create the user with hashed password
#             user = User.objects.create_user(
#                 username=email,
#                 email=email,
#                 password=password,
#                 first_name=name
#             )

#             # Create the linked Profile with approval set False by default
#             Profile.objects.create(
#                 user=user,
#                 role=role,
#                 phone=phone,
#                 specialization=specialization if role == 'doctor' else '',
#                 is_approved=False
#             )

#             messages.success(request, "Signup successful. Please wait for admin approval.")
#             return redirect('login')  # Change 'login' to your actual login URL name

#         except IntegrityError:
#             messages.error(request, "An error occurred during signup. Please try again.")
#             return render(request, 'signup.html')

#     return render(request, 'signup.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        specialization = request.POST.get("specialization", "").strip()

        # Role check
        if not role:
            messages.error(request, "Please select a role.")
            return render(request, 'signup.html')

        # Specialization check for doctor
        if role == 'doctor' and not specialization:
            messages.error(request, "Please enter specialization for doctor.")
            return render(request, 'signup.html')

        # Duplicate email check
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'signup.html')

        try:
            # Create user
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )

            # If admin, make user staff and superuser
            if role == "admin":
                user.is_staff = True
                user.is_superuser = True
                user.save()

            # Create user profile
            Profile.objects.create(
                user=user,
                role=role,
                phone=phone,
                specialization=specialization if role == 'doctor' else "",
                is_approved=True  # Change to False if admin approval is required
            )

            messages.success(request, "Signup successful. Please wait for admin approval.")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"Signup error: {str(e)}")
            return render(request, 'signup.html')

    return render(request, 'signup.html')


# ================= User Login =================

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        # Validate role selection
        if not role:
            messages.error(request, "Please select your role to login.")
            return render(request, 'login.html')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Check if user has a profile and matching role
            if hasattr(user, 'profile') and user.profile.role == role:
                # Check if user is approved by admin
                if user.profile.is_approved:
                    auth_login(request, user)
                    # Redirect based on role
                    if role == 'doctor':
                        return redirect('doctor_home')
                    elif role == 'patient':
                        return redirect('patient_home')
                    elif role == 'admin':
                        return redirect('admin_dashboard')
                    else:
                        messages.error(request, "Invalid role.")
                else:
                    messages.error(request, "Your account is pending approval by admin.")
            else:
                messages.error(request, "Role mismatch or profile not found.")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'login.html')



# ================= Admin Views =================

def approve_user(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    profile.is_approved = True
    profile.save()
    messages.success(request, f"{profile.user.first_name}'s account approved.")
    return redirect('admin_dashboard')

def admin_dashboard(request):
    pending_users = Profile.objects.filter(is_approved=False)
    return render(request, 'admin_dashboard.html', {'pending_users': pending_users})

def admin_contact_messages(request):
    return render(request, 'admin_contact_messages.html')

def admin_feedback(request):
    return render(request, 'admin_feedback.html')

def admin_logout(request):
    return render(request, 'admin_logout.html')

def admin_report(request):
    return render(request, 'admin_report.html')

def admin_contact_message(request):
    return render(request, 'admin_contact_message.html')

def admin_reports(request):
    return render(request, 'admin_reports.html')


# ================= Doctor Views =================

def doctor_home(request):
    return render(request, 'doctor-home.html')

def doctor_dashboard(request):
    return render(request, 'doctor-dashboard.html')

def doctor_logout(request):
    return render(request, 'doctor-logout.html')


# ================= Patient Views =================

def patient_home(request):
    return render(request, 'patient_home.html')

def patient_dashboard(request):
    return render(request, 'patient_dashboard.html')
@login_required
def dashboard(request):
    user = request.user

    # Get or create the user's profile
    profile, created = Profile.objects.get_or_create(user=user, defaults={'role': 'patient'})

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.role = 'patient'
            profile.save()
            return redirect('dashboard')  # refresh after save
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'dashboard.html', {'form': form, 'profile': profile})

# def patient_registration(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         age = request.POST.get('age')
#         gender = request.POST.get('gender')
#         department = request.POST.get('department')
#         doctor = request.POST.get('doctor')
#         address = request.POST.get('address')

#         if User.objects.filter(username=email).exists():
#             messages.error(request, 'A user with this email already exists.')
#             return redirect('patient_registration')

#         user = User.objects.create_user(username=email, email=email, password="docnow123")
#         user.first_name = name
#         user.save()

#         Profile.objects.create(
#             user=user,
#             role='patient',
#             phone=phone,
#             age=age,
#             gender=gender,
#             department=department,
#             doctor=doctor,
#             address=address,
#             is_approved=True
#         )

#         messages.success(request, 'Registration successful!')
#         return redirect('patient_dashboard')

#     return render(request, 'patient-registration.html')

def patient_registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        department = request.POST.get('department')
        doctor = request.POST.get('doctor')
        address = request.POST.get('address')

        # ✅ Convert age to integer safely
        try:
            age = int(age)
        except (ValueError, TypeError):
            age = None

        # ✅ Check if any required fields are missing
        if not all([name, email, phone, gender, department, doctor, address]):
            messages.error(request, 'Please fill all required fields.')
            return redirect('patient_registration')

        # ✅ Check for existing user
        if User.objects.filter(username=email).exists():
            messages.error(request, 'A user with this email already exists.')
            return redirect('patient_registration')

        # ✅ Create the user
        user = User.objects.create_user(username=email, email=email, password="docnow123")
        user.first_name = name
        user.save()

        # ✅ Create the profile with all fields
        Profile.objects.create(
            user=user,
            role='patient',
            phone=phone,
            age=age,
            gender=gender,
            department=department,
            doctor=doctor,
            address=address,
            is_approved=True
        )

        messages.success(request, 'Registration successful!')
        return redirect('patient_dashboard')

    return render(request, 'patient-registration.html')


def book_appointment(request):
    return render(request, 'book_appointment.html')

def appointment(request):
    return render(request, 'appointments.html')

def cancel_appointment(request):
    return render(request, 'cancel-appointment.html')

def medical_history(request):
    return render(request, 'medical-history.html')

def settings_and_logout(request):
    return render(request, 'settings-and-logout.html')


# ================= Management Views =================

def manage_patients(request):
    return render(request, 'manage_patients.html')

def manage_doctors(request):
    return render(request, 'manage_doctors.html')

def manage_appointments(request):
    return render(request, 'manage_appointments.html')


# ================= Custom Error Page =================

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)
