from django.contrib.auth import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FilmViewSet

router = DefaultRouter()
router.register(r'films', FilmViewSet, basename='diafilms')

urlpatterns = [
    path('v1/', include(router.urls)),
]
