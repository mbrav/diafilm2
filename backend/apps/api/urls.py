from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from .views import FilmViewSet

schema_view = get_swagger_view(title='Схема API проекта Δиа Фильм²')


router = DefaultRouter()
router.register(r'films', FilmViewSet, basename='diafilms')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/docs/', schema_view, name='swagger-ui'),
]
