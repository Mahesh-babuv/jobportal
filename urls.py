from django.urls import path,include
from .views import custom_login_view
from portal import views
from .views import contact_us

urlpatterns = [
    path('login/', custom_login_view, name='custom_login'),
    path('applynow/', views.job_application, name='job_application'),
    path("contact/", contact_us, name="contact_us"),  # URL for the contact page
    path('send_otp/', views.send_otp_view, name='send_otp'),
    path('verify_otp/', views.verify_otp_view, name='verify_otp'),


]
