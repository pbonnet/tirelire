from rest_framework import serializers
from app.models import Cash, MoneyBoxContent, MoneyBox


class MoneyBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyBox
        fields = ['id', 'created_at', 'updated_at', 'name']


class MoneyBoxContentSerializer(serializers.ModelSerializer):
    cash_type = serializers.ChoiceField(source='cash.cash_type', choices=Cash.CashTypeChoice.choices)
    currency = serializers.ChoiceField(source='cash.currency', choices=Cash.CurrencyChoice.choices, read_only=True)
    value = serializers.CharField(source='cash.value')

    class Meta:
        model = MoneyBoxContent
        fields = ['cash_type', 'currency', 'value', 'amount']
        read_only_fields = ['amount']


class WealthSerializer(serializers.Serializer):
    wealth_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    cashes = MoneyBoxContentSerializer(many=True)
