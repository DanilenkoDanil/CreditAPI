from rest_framework import serializers
from credit_calculate.models import Credit, Payment


class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = ['id', 'amount', 'loan_start_date', 'number_of_payments', 'periodicity', 'interest_rate']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'credit', 'date', 'principal', 'interest']
