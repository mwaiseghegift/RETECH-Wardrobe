from django.urls import path
from mainstore.api.views import *

app_name = 'api'

urlpatterns = [
    path('checkout/lipa-na-mpesa/', api_LipaNaMpesaView, name='api_lipa_na_mpesa'),
    path('c2b/register/', api_register_urls, name="api_register_mpesa_validation"),
    path('c2b/confirmation/', api_confirmation, name="api_confirmation"),
    path('c2b/validation/', api_validation, name="api_validation"),
    path('c2b/callback/', api_call_back, name="api_call_back"),
]
