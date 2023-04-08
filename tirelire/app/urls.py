from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers

from app import views as api_views

schema_view = get_schema_view(
   openapi.Info(
      title="Moneybox API",
      default_version='v1',
      description=(
        """
        Moneybox API documentation pour la gestion de tirelires et de leurs richesse.
        Grâce à cette API vous avez la possibilité de:
        - Créer une tireline avec l'endpoint: POST /moneyboxes/
        - Lister les tirelires avec l'endpoint: GET /moneyboxes/
        - Retrouver les informations basiques d'une tirelire avec l'endpoint: GET /moneyboxes/{id}/
        - Secouer une tirelire pour y savoir son contenu et votre richesse avec l'endpoint: GET /moneyboxes/{id}/shake/
        - Épargner de la monnaie dans une tirelire avec l'endpoint: GET /moneyboxes/{id}/shake/
        - Casser une tirelire avec l'endpoint: GET /moneyboxes/{id}/break/

        La monnaie est limitée à de la monnaie avec pièces et billets de la devise Euro.
        Casser une tirelire retourna son contenu et votre richesse finale, après ça elle ne sera plus utilisable.
        """
      ),
      contact=openapi.Contact(email="jesuispaulbonnet@gmail.com"),
   )
)

router = routers.DefaultRouter()
router.register(r'moneyboxes', api_views.MoneyBoxViewSet, basename='moneyboxes')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^api/swagger-doc/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
