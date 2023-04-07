from rest_framework import serializers
from app.models import Cash, MoneyBoxContent, MoneyBox


class MoneyBoxSerializer(serializers.ModelSerializer):

    class Meta:
        model = MoneyBox
        fields = ['id', 'created_at', 'updated_at', 'name', 'broken']
        read_only_fields = ['broken']


class MoneyBoxContentSerializer(serializers.ModelSerializer):
    cash_type = serializers.ChoiceField(source='cash.cash_type', choices=Cash.CashTypeChoice.choices)
    currency = serializers.ChoiceField(source='cash.currency', choices=Cash.CurrencyChoice.choices, read_only=True)
    value = serializers.DecimalField(source='cash.value', max_digits=5, decimal_places=2)

    class Meta:
        model = MoneyBoxContent
        fields = ['cash_type', 'currency', 'value', 'amount']

    def validate(self, data):
        """
        Check that start is before finish.
        """
        cash_data = data['cash']
        if Cash.find_from_type_and_value(cash_data['cash_type'], cash_data['value']) is None:
            raise serializers.ValidationError(
                {"cashes": f"The {cash_data['cash_type']} with the value {cash_data['value']} does not exist."}
            )
        return data


class MoneyBoxWealthSerializer(serializers.ModelSerializer):
    wealth = serializers.DecimalField(max_digits=10, decimal_places=2)
    cashes = MoneyBoxContentSerializer(many=True, source='moneyboxcontent_set_ordered')

    class Meta:
        model = MoneyBox
        fields = ['wealth', 'cashes']
