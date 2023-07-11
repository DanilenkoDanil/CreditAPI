from django.db import models


class Period(models.Model):
    name = models.CharField(max_length=10)
    days_count = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Credit(models.Model):
    amount = models.FloatField()
    loan_start_date = models.DateField()
    number_of_payments = models.IntegerField()
    periodicity = models.ForeignKey(Period, on_delete=models.CASCADE)
    interest_rate = models.FloatField()

    def __str__(self):
        return f"Credit - {self.pk}"


class Payment(models.Model):
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE)
    date = models.DateField()
    principal = models.FloatField()
    interest = models.FloatField()

    def __str__(self):
        return f"Payment - {self.pk}"
