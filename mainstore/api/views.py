from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from mainstore.api.serializers import MpesaPaymentSerializer
from mainstore.models import MpesaPayment

from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from mainstore.forms import CompletePayMent
from django.contrib.auth.decorators import login_required
from mainstore.models import Order
import json
import requests
from requests.auth import HTTPBasicAuth
from mainstore.mpesa_credentials import MpesaAccessToken,LipaNaMpesaPassword

@api_view(['POST'])
@login_required
def api_LipaNaMpesaView(request, *args, **kwargs):
    order = Order.objects.get(user=request.user, is_ordered=False)
    amount = order.totalPrice()
    telephone = ""
    
    if request.method == 'POST':
        telephone = request.POST['phone-no']
        
       
            
        print(telephone)
        
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization":"Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipaNaMpesaPassword.business_short_code,
            "Password": LipaNaMpesaPassword.decode_password,
            "Timestamp": LipaNaMpesaPassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "5",
            "PartyA": f"254{telephone}",
            "PartyB": "174379",
            "PhoneNumber": f"254{telephone}",
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Retech Store",
            "TransactionDesc": "Retech Store Test"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponseRedirect(reverse('retechecommerce:lipa-na-mpesa'))
                
    else:
        form = CompletePayMent()
            

    
    context = {
        'amount':amount,
        'telephone':telephone,
    }
    
    return render(request, 'payments/mpesa_checkout.html', context)

@api_view(['GET'])
@csrf_exempt
def api_register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipaNaMpesaPassword.test_c2b_shortcode,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://45291b1fab33.ngrok.io/api/c2b/confirmation/",
               "ValidationURL": "https://45291b1fab33.ngrok.io/api/c2b/validation/"}
    response = requests.post(api_url, json=options, headers=headers)
    return Response(response.text)

@api_view(['GET'])
@csrf_exempt
def api_call_back(request):
    pass

@api_view(['GET'])
@csrf_exempt
def api_validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return Response(dict(context))

@api_view(['GET'])
@csrf_exempt
def api_confirmation(request):
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    payment = MpesaPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],
    )
    payment.save()
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return Response(dict(context))