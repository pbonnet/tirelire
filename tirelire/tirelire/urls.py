from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('moneybox-app/', include(('app.urls', 'app'), namespace='api')),
    path('admin/', admin.site.urls),
]
