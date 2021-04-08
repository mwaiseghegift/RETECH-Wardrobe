from rest_framework import serializers
from rest_framework.decorators import api_view

from mainstore.models import MpesaPayment


class MpesaPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaPayment
        fields = ['amount','description','type',
                  'reference','first_name','middle_name',
                  'last_name','phone_number','organization_balance']