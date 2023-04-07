from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException

from app.models import MoneyBox
from app.serializers import MoneyBoxSerializer, MoneyBoxWealthSerializer, MoneyBoxContentSerializer
from rest_framework.response import Response


class MoneyBoxBrokenError(APIException):
    status_code = 400
    default_detail = 'This money box is broken you cannot use it anymore.'


class MoneyBoxViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = MoneyBox.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        if self.action in ['shake', 'save', 'break_moneybox']:
            return MoneyBoxWealthSerializer
        return MoneyBoxSerializer

    def get_money_box(self, pk: int, raise_error: bool = True) -> MoneyBox:
        money_box = get_object_or_404(MoneyBox, id=pk)
        if money_box.broken and raise_error:
            raise MoneyBoxBrokenError
        return money_box

    @action(methods=['get'], detail=True)
    def shake(self, request, pk=None):
        # Return moneybox content
        serializer = MoneyBoxWealthSerializer(self.get_money_box(pk))
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True)
    def save(self, request, pk=None):
        money_box = self.get_money_box(pk)
        cashes_to_add_serializer = MoneyBoxContentSerializer(data=request.data['cashes'], many=True)
        if not cashes_to_add_serializer.is_valid():
            # Map the errors to get the correct format
            errors = [error for error in cashes_to_add_serializer.errors if 'cashes' in error][0]
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        # Save moneybox content
        money_box.save_money(cashes_to_add_serializer.data)
        serializer = MoneyBoxWealthSerializer(money_box)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True, url_name='break', url_path='break')
    def break_moneybox(self, request, pk=None):
        # Break moneybox and return all the cash
        money_box = self.get_money_box(pk)
        serializer = MoneyBoxWealthSerializer(money_box)
        data = serializer.data
        money_box.break_moneybox()
        return Response(data)
