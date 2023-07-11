from django.contrib import admin
from credit_calculate.models import Credit, Payment, Period


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'credit', 'date', 'principal', 'interest')


@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'loan_start_date', 'number_of_payments', 'periodicity', 'interest_rate')

