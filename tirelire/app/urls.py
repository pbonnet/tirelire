from django.urls import path
from app.views import web as web_views

urlpatterns = [
    path('', web_views.tirelire, name='tirelire')
]
