from django import forms
from .models import JobApplication
from .models import ContactMessage

class EmailForm(forms.Form):
    email = forms.EmailField()
    
class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['full_name', 'phone', 'email', 'address', 'state', 'city', 
                  'pincode', 'college', 'qualification', 'job_role', 'resume']
        


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['full_name', 'email', 'message']