from decimal import Decimal
from functools import cache
from typing import List

from django.db import models


class Cash(models.Model):
    """
    DB model to store all the different accepted cash values.
    """
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
        """
        Retrieve all Cash objects from the database, after the first call it will return the list from the cache.
        Returns:
            List['Cash']: A list of Cash objects.
        """
        return list(cls.objects.all())

    @classmethod
    def find_from_type_and_value(cls, cash_type: str, value: str) -> 'Cash':
        """
        Find a Cash object from the cached list based on its cash_type and value.
        Args:
            cash_type (str): The type of cash.
            value (str): The value of cash.
        Returns:
            'Cash': The found Cash object, or None if not found.
        """
        return next(
            (cash for cash in cls.get_all() if cash.cash_type == cash_type and cash.value == Decimal(value)),
            None
        )


class MoneyBox(models.Model):
    """
    DB model to store all the money boxes where you can save cash until it is broken.
    """
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
    def moneyboxcontent_set_ordered(self) -> models.QuerySet:
        """
        Retrieve the MoneyBoxContent objects associated with the MoneyBox object,
        ordered by the value of the corresponding Cash objects.
        Returns:
            QuerySet: A QuerySet of MoneyBoxContent objects, ordered by cash value.
        """
        return self.moneyboxcontent_set.order_by('cash__value')

    @property
    def wealth(self) -> Decimal:
        """
        Calculate the total wealth associated with the MoneyBox object,
        by summing up the value of the Cash objects in the MoneyBoxContent objects.
        Returns:
            Decimal: The total wealth.
        """
        wealth_total = Decimal('0')
        for moneybox_content in self.moneyboxcontent_set.select_related('cash'):
            wealth_total += moneybox_content.cash.value * moneybox_content.amount
        return wealth_total

    def save_money(self, cashes_to_add: List[dict]) -> None:
        """
        Add cash to the MoneyBox object.
        Args:
            cashes_to_add (List[dict]):
            A list of dictionaries containing the details of cash to be added.
            Each dictionary should have keys 'cash_type', 'value', and 'amount'.
        Returns:
            None
        """
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

    def break_moneybox(self) -> None:
        """
        Empty the MoneyBox by deleting all MoneyBoxContent objects associated with it,
        and mark the MoneyBox as broken.
        Returns:
            None
        """
        self.moneyboxcontent_set.all().delete()
        self.broken = True
        self.save()


class MoneyBoxContent(models.Model):
    """
    DB model that keeps a record of the amount of each cash value against a money box.
    """
    money_box = models.ForeignKey(MoneyBox, on_delete=models.CASCADE)
    cash = models.ForeignKey(Cash, on_delete=models.CASCADE)
    amount = models.IntegerField()
