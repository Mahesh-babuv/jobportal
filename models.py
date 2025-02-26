from django.db import models

class JobApplication(models.Model):
    full_name = models.CharField(max_length=255, null=False, blank=False)
    phone = models.CharField(max_length=10, unique=True)  # Ensure phone is unique
    email = models.EmailField(max_length=255, unique=True) # More appropriate
    address = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    college = models.CharField(max_length=255, blank=True, null=True)
    qualification = models.CharField(max_length=255, blank=True, null=True)
    job_role = models.CharField(max_length=100, blank=True, null=True)
    experience = models.CharField(max_length=255, blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)  # ✅ Add this field

    def __str__(self):
        return self.full_name

class ContactMessage(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)  # More appropriate
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)  # Automatically saves submission time

    def __str__(self):
        return f"{self.full_name} - {self.email}"