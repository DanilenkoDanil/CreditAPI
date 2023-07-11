from django.urls import path
from credit_calculate.views import CreatePaymentScheduleView, ReducePrincipalView


urlpatterns = [
    path('create-payment-schedule/', CreatePaymentScheduleView.as_view()),
    path('reduce-principal/<int:credit_id>/<int:payment_id>/', ReducePrincipalView.as_view()),
]
