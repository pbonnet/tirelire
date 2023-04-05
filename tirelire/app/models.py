from django.db import models


class MoneyBox(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    cashes = models.ManyToManyField(
        "Cash",
        through="MoneyBoxContent",
        through_fields=("money_box", "cash"),
    )


class Cash(models.Model):
    class CashTypeChoice(models.TextChoices):
        BILL = "bill"
        COIN = "coin"

    class CurrencyChoice(models.TextChoices):
        EUR = "EUR", "€"

    cash_type = models.CharField(
        max_length=4,
        choices=CashTypeChoice.choices,
    )
    currency = models.CharField(
        max_length=3,
        choices=CurrencyChoice.choices,
        default=CurrencyChoice.EUR
    )
    value = models.DecimalField(max_digits=5, decimal_places=2)


class MoneyBoxContent(models.Model):
    money_box = models.ForeignKey(MoneyBox, on_delete=models.CASCADE)
    cash = models.ForeignKey(Cash, on_delete=models.CASCADE)
    amount = models.IntegerField()
