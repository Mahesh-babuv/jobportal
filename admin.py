from django.contrib import admin
from .models import JobApplication
from .models import ContactMessage
@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'state', 'city', 'job_role', 'experience','submitted_at')
    search_fields = ('full_name', 'email', 'phone')
    list_filter = ('state', 'city', 'qualification', 'job_role')


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'submitted_at')  # Fields to display in the admin panel
    search_fields = ('full_name', 'email')  # Enable search functionality
    list_filter = ('submitted_at',)  # Filter by submission date
    readonly_fields = ('submitted_at',)  # Prevent modification of submission date

admin.site.register(ContactMessage, ContactMessageAdmin)
