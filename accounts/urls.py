from django.urls import path
from .views import (LogInView, LogOutView, RegisterView,
                    VerificationView)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView, name='register'),
    path('login', LogInView, name='login'),
    path('logout', LogOutView, name='logout'),
    path('activate/<uidb64>/<token>/', VerificationView, name='activate'),
]

