from rest_framework import mixins, viewsets
from rest_framework.decorators import action

from app.models import MoneyBox
from app.serializers import MoneyBoxSerializer, WealthSerializer
from rest_framework.response import Response


class MoneyBoxViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = MoneyBox.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        if self.action in ['shake', 'save']:
            return WealthSerializer
        return MoneyBoxSerializer

    @action(methods=['get'], detail=True)
    def shake(self, request, pk=None):
        # Return moneybox content
        return Response({'test': 'test'})

    @action(methods=['post'], detail=True)
    def save(self, request, pk=None):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Save moneybox content
        return Response({'test': 'test'})

    @action(methods=['delete'], detail=True)
    def break_it(self, request, pk=None):
        # Destroy moneybox content
        return Response({'test': 'test'})
