from rest_framework import serializers
from rest_framework.decorators import api_view

from mainstore.models import MpesaPayment, Order


class MpesaPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaPayment
        fields = ['amount','description','type',
                  'reference','first_name','middle_name',
                  'last_name','phone_number','organization_balance']
        
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields= ['user','items','start_date','ordered_date',
                 'is_ordered','billing_address','payment','coupon']