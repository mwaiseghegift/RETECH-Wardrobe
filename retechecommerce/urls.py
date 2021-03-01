from django.urls import path
from .views import (IndexView)

app_name="retechecommerce"

urlpatterns = [
    path('', IndexView, name='index'),
]
