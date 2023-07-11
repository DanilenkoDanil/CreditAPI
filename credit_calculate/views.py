from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import timedelta
from credit_calculate.models import Credit, Payment
from credit_calculate.serializers import CreditSerializer, PaymentSerializer


class CreatePaymentScheduleView(APIView):
    def post(self, request):
        serializer = CreditSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            loan_start_date = serializer.validated_data['loan_start_date']
            number_of_payments = serializer.validated_data['number_of_payments']
            periodicity = serializer.validated_data['periodicity']
            interest_rate = serializer.validated_data['interest_rate']

            credit = Credit.objects.create(
                amount=amount,
                loan_start_date=loan_start_date,
                number_of_payments=number_of_payments,
                periodicity=periodicity,
                interest_rate=interest_rate
            )

            payment_schedule = self.create_payment_schedule(credit)

            schedule_serializer = PaymentSerializer(payment_schedule, many=True)
            return Response(schedule_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def create_payment_schedule(credit: Credit):
        remaining_balance = credit.amount
        payment_schedule = []
        date_delta = credit.periodicity.days_count
        payment_date = credit.loan_start_date + timedelta(days=date_delta)

        for _ in range(credit.number_of_payments):
            interest_payment = remaining_balance * credit.interest_rate
            principal_payment = credit.amount / credit.number_of_payments
            remaining_balance -= principal_payment

            payment = Payment.objects.create(
                credit=credit,
                date=payment_date,
                principal=principal_payment,
                interest=interest_payment
            )

            payment_schedule.append(payment)

            payment_date = payment_date + timedelta(days=date_delta)

        return payment_schedule


class ReducePrincipalView(APIView):

    def patch(self, request, credit_id, payment_id):
        amount = request.data.get('amount', None)

        if amount is None:
            return Response({"error": "Request must include 'amount'."}, status=status.HTTP_400_BAD_REQUEST)

        amount = float(amount)

        try:
            payment = Payment.objects.get(credit_id=credit_id, id=payment_id)
        except Payment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if payment.principal < amount:
            return Response({"error": "The amount to reduce exceeds the principal of the payment."},
                            status=status.HTTP_400_BAD_REQUEST)

        credit = Credit.objects.get(id=credit_id)
        next_payments = Payment.objects.filter(credit=credit, id__gt=payment_id)

        if len(next_payments) == 0:
            return Response({"error": "It is not possible to carry out such an operation with the last payment."},
                            status=status.HTTP_400_BAD_REQUEST)

        remaining_balance = payment.interest / credit.interest_rate

        payment.principal -= amount
        payment.save()

        remaining_balance -= payment.principal

        increase = amount / len(next_payments)

        self.calculate_interest(next_payments, credit, remaining_balance, increase)

        serializer = PaymentSerializer(payment)
        return Response(serializer.data)

    @staticmethod
    def calculate_interest(payments, credit, current_remaining_balance, increase_principal):
        new_payments = []
        remaining_balance = current_remaining_balance

        for payment in payments:
            payment.principal += increase_principal
            payment.interest = remaining_balance * credit.interest_rate
            remaining_balance -= payment.principal
            payment.save()

        return new_payments
