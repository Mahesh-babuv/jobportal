from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import JobApplication
from django.contrib import messages
from .models import ContactMessage
from django.db import IntegrityError

def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('hom')  # Redirect to homepage after login
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import JobApplication
from django.db import IntegrityError

def job_application(request):
    if request.method == 'POST':
        # Collect data from the form
        form_data = {
            'name': request.POST.get('name'),
            'phone': request.POST.get('phone'),
            'email': request.POST.get('email'),
            'address': request.POST.get('address'),
            'state': request.POST.get('state'),
            'city': request.POST.get('city'),
            'pincode': request.POST.get('pincode'),
            'college': request.POST.get('college'),
            'qualification': request.POST.get('qualification'),
            'jobrole': request.POST.get('jobrole'),
            'experience': request.POST.get('experience'),
        }

        # Check if email already exists
        if JobApplication.objects.filter(email=form_data['email']).exists():
            messages.error(request, "This email is already in use. Please use a unique email.")
            return render(request, 'applynow.html', {'form_data': form_data})

        # Check if phone already exists
        if JobApplication.objects.filter(phone=form_data['phone']).exists():
            messages.error(request, "This phone number is already in use.")
            return render(request, 'applynow.html', {'form_data': form_data})

        # Get the uploaded resume
        resume = request.FILES.get('resume')

        # Validate file size (limit to 1MB)
        if resume:
            if resume.size > 1 * 1024 * 1024:  # 1MB = 1024 * 1024 bytes
                messages.error(request, "The resume file should be less than 1MB.")
                return render(request, 'applynow.html', {'form_data': form_data})

        try:
            # Save the data to the database
            JobApplication.objects.create(
                full_name=form_data['name'],
                phone=form_data['phone'],
                email=form_data['email'],
                address=form_data['address'],
                state=form_data['state'],
                city=form_data['city'],
                pincode=form_data['pincode'],
                college=form_data['college'],
                qualification=form_data['qualification'],
                job_role=form_data['jobrole'],
                experience=form_data['experience'],
                resume=resume,
            )
            messages.success(request, "Your application has been submitted successfully!")
            return redirect('/thankyou/')

        except IntegrityError:
            messages.error(request, "An error occurred while submitting your application. Please try again.")
            return render(request, 'applynow.html', {'form_data': form_data})

    return render(request, 'applynow.html')


def thankyou(request):
    return render(request, 'thankyou.html')



def contact_us(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        print("Received data:", full_name, email, message)  # Debugging

        if full_name and email and message:
            ContactMessage.objects.create(full_name=full_name, email=email, message=message)
            print("Message saved successfully!")  # Debugging
            return redirect('/contact')

    return render(request, 'contact.html')
 

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_backends
from datetime import datetime
from .forms import EmailForm, OTPForm
from .utils import generate_otp, send_otp_email

def send_otp_view(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp = generate_otp()

            # Get the current timestamp and convert it to an ISO string
            otp_timestamp = timezone.now().isoformat()

            # Save OTP, email, and timestamp (as string) in session
            request.session['otp'] = otp
            request.session['email'] = email
            request.session['otp_timestamp'] = otp_timestamp
            
            # Send OTP email
            send_otp_email(email, otp)
            return redirect('verify_otp')
    else:
        form = EmailForm()

    return render(request, 'send_otp.html', {'form': form})

def verify_otp_view(request):
    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            stored_otp = request.session.get('otp')
            email = request.session.get('email')
            otp_timestamp = request.session.get('otp_timestamp')

            if not email or not stored_otp or not otp_timestamp:
                messages.error(request, "Session expired. Please try again.")
                return redirect('send_otp')

            # Convert timestamp back to datetime object
            try:
                otp_timestamp = datetime.fromisoformat(otp_timestamp)
            except ValueError:
                messages.error(request, "Invalid OTP timestamp.")
                return redirect('send_otp')

            # Check OTP and timestamp validity (e.g., within 5 minutes)
            if otp == stored_otp and (timezone.now() - otp_timestamp).seconds <= 300:
                # Check if user exists, if not, create the user
                user = User.objects.filter(email=email).first()
                if not user:
                    # Create a new user if the user does not exist
                    user = User.objects.create_user(username=email, email=email, password='defaultpassword')
                    user.save()
                    messages.success(request, "User created and logged in successfully!")

                # Specify the authentication backend explicitly
                backend = get_backends()[0]  # Select the first authentication backend
                user.backend = backend.__module__ + "." + backend.__class__.__name__

                # Authenticate and log in the user
                login(request, user)
                return redirect('job_application')  # Redirect to the home page after login
            else:
                messages.error(request, "Invalid or expired OTP.")
        else:
            messages.error(request, "Invalid OTP format.")

    else:
        form = OTPForm()

    return render(request, 'verify_otp.html', {'form': form})

def home(request):
    return render(request, 'home.html')


def applynow(request):
    if request.method == 'POST':
        # Process form data (this can be extended for a real form)
        messages.success(request, "Application submitted successfully.")
        return redirect('thankyou')  # Redirect to a thank-you page
    return render(request, 'applynow.html')

