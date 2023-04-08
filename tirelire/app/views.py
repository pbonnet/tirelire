from typing import Union

from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.request import Request

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
    """
    Viewset for managing moneyboxes and its cash content.
    """

    queryset = MoneyBox.objects.all().order_by('-created_at')

    def get_serializer_class(self) -> Union[MoneyBoxSerializer, MoneyBoxWealthSerializer]:
        """
        Get the appropriate serializer class based on the action.
        Returns:
            Union[MoneyBoxSerializer, MoneyBoxWealthSerializer]: Serializer class.
        """
        if self.action in ['shake', 'save', 'break_moneybox']:
            return MoneyBoxWealthSerializer
        return MoneyBoxSerializer

    def get_money_box(self, pk: int) -> MoneyBox:
        """
        Get a MoneyBox instance by its primary key.
        Args:
            pk (int): Primary key of the MoneyBox instance.
        Returns:
            MoneyBox: MoneyBox instance.
        """
        money_box = get_object_or_404(MoneyBox, id=pk)
        if money_box.broken:
            raise MoneyBoxBrokenError
        return money_box

    @action(methods=['get'], detail=True)
    def shake(self, request: Request, pk: int):
        """
        Perform the 'shake' action on a MoneyBox instance, which retrieves its wealth.
        Args:
            request (Request): DRF request object.
            pk (int): Primary key of the MoneyBox instance.
        Returns:
            Response: DRF response object of MoneyBoxWealthSerializer serialized which contains wealth data.
        """
        serializer = MoneyBoxWealthSerializer(self.get_money_box(pk))
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def save(self, request: Request, pk):
        """
        Perform the 'save' action on a MoneyBox instance, which adds cashes to it.
        Args:
            request (Request): DRF request object.
            pk (int): Primary key of the MoneyBox instance.
        Returns:
            Response: DRF response object of MoneyBoxWealthSerializer serialized which contains wealth data.
        """
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
    def break_moneybox(self, request: Request, pk):
        """
        Perform the 'break' action on a MoneyBox instance, which deletes all its contents and marks it as broken.
        Args:
            request (Request): DRF request object.
            pk (int): Primary key of the MoneyBox instance.
        Returns:
            Response: DRF response object of MoneyBoxWealthSerializer serialized which contains wealth data.
        """
        money_box = self.get_money_box(pk)
        serializer = MoneyBoxWealthSerializer(money_box)
        wealth_data = serializer.data
        money_box.break_moneybox()
        return Response(wealth_data)
