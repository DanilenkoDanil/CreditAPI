from datetime import date
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from credit_calculate.utils import decimal_round
from .views import CreatePaymentScheduleView, ReducePrincipalView
from .models import Credit, Payment, Period


class CreatePaymentScheduleViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        Period.objects.create(name='1m', days_count=31)

    def test_create_payment_schedule(self):
        data = {
            'amount': 1000,
            'loan_start_date': date.today(),
            'number_of_payments': 12,
            'periodicity': 1,
            'interest_rate': 0.05
        }
        request = self.factory.post('/api/create_payment_schedule/', data)

        view = CreatePaymentScheduleView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        payment_schedule = response.data
        self.assertEqual(len(payment_schedule), 12)

        self.assertEqual(
            payment_schedule[0]['principal'],
            decimal_round(1000 / 12)
        )
        self.assertEqual(
            payment_schedule[0]['interest'],
            decimal_round(1000 * 0.05 * 31 / 365)
        )
        self.assertEqual(
            payment_schedule[1]['interest'],
            decimal_round((1000 - 1000 / 12) * 0.05 * 31 / 365)
        )

        self.assertEqual(Credit.objects.count(), 1)
        self.assertEqual(Payment.objects.count(), 12)


class ReducePrincipalViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        Period.objects.create(name='1m', days_count=31)

    def test_reduce_principal(self):
        data = {
            'amount': 1000,
            'loan_start_date': date.today(),
            'number_of_payments': 10,
            'periodicity': 1,
            'interest_rate': 0.05
        }
        request = self.factory.post('/api/create_payment_schedule/', data)
        view = CreatePaymentScheduleView.as_view()
        view(request)

        data = {'amount': 50}
        request = self.factory.patch('/api/reduce-principal/1/3/', data)
        view = ReducePrincipalView.as_view()
        response = view(request, credit_id=1, payment_id=3)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_payment = Payment.objects.get(id=3)
        self.assertEqual(updated_payment.principal, 50)
