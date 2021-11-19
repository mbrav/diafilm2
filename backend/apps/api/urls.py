from django.contrib.auth import views
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from .views import FilmViewSet

router = DefaultRouter()
router.register(r'films', FilmViewSet, basename='diafilms')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/schema/', get_schema_view(
        title="Δиа Фильм²",
        description="Схема API проекта Δиа Фильм²"
    ), name='diafilm-schema'),
    path('v1/docs/', TemplateView.as_view(
        template_name='api/docs.html',
        extra_context={'schema_url':'api:diafilm-schema'}
    ), name='swagger-ui'),
]
