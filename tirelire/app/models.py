from decimal import Decimal
from functools import cache
from typing import List

from django.db import models


class Cash(models.Model):

    class Meta:
        ordering = ['value']

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

    @classmethod
    @cache
    def get_all(cls) -> List['Cash']:
        return list(cls.objects.all())

    @classmethod
    def find_from_type_and_value(cls, cash_type: str, value: str) -> 'Cash':
        return next(
            (cash for cash in cls.get_all() if cash.cash_type == cash_type and cash.value == Decimal(value)),
            None
        )


class MoneyBox(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    cashes = models.ManyToManyField(
        Cash,
        through="MoneyBoxContent",
        through_fields=("money_box", "cash"),
    )
    broken = models.BooleanField(default=False)

    @property
    def moneyboxcontent_set_ordered(self):
        return self.moneyboxcontent_set.order_by('cash__value')

    @property
    def wealth(self) -> Decimal:
        wealth_total = Decimal('0')
        for moneybox_content in self.moneyboxcontent_set.select_related('cash'):
            wealth_total += moneybox_content.cash.value * moneybox_content.amount
        return wealth_total

    def save_money(self, cashes_to_add):
        existing_moneybox_contents = self.moneyboxcontent_set.select_related('cash').all()
        for cash_to_add in cashes_to_add:
            cash_object = Cash.find_from_type_and_value(cash_to_add['cash_type'], cash_to_add['value'])
            existing_moneybox_content = next(
                (
                    moneybox_content for moneybox_content in existing_moneybox_contents
                    if moneybox_content.cash == cash_object
                ),
                None
            )
            if existing_moneybox_content:
                existing_moneybox_content.amount += cash_to_add['amount']
                existing_moneybox_content.save()
            else:
                self.moneyboxcontent_set.add(
                    MoneyBoxContent(cash=cash_object, amount=cash_to_add['amount']), bulk=False
                )
        self.save()

    def break_moneybox(self):
        self.moneyboxcontent_set.all().delete()
        self.broken = True
        self.save()


class MoneyBoxContent(models.Model):
    money_box = models.ForeignKey(MoneyBox, on_delete=models.CASCADE)
    cash = models.ForeignKey(Cash, on_delete=models.CASCADE)
    amount = models.IntegerField()
