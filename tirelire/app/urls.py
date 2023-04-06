from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers

from app.views import api as api_views
from app.views import web as web_views

schema_view = get_schema_view(
   openapi.Info(
      title="Moneybox API",
      default_version='v1',
      description=(
        """
        Moneybox API documentation to present different endpoints to manage moneyboxes.
        You will be able to:
        - Create a moneybox
        - List the moneyboxes
        - Shake a moneybox to get the list of money in it
        - Save money in a moneybox by inserting coins or bills
        - Break a moneybox to get the money back and destroy the moneybox
        """
      ),
      contact=openapi.Contact(email="jesuispaulbonnet@gmail.com"),
   )
)

router = routers.DefaultRouter()
router.register(r'moneyboxes', api_views.MoneyBoxViewSet)

urlpatterns = [
    path('web/', web_views.tirelire, name='tirelire'),
    path('api/v1/', include(router.urls)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^api/swagger-doc/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
