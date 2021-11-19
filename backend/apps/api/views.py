from django.shortcuts import render
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination

from apps.diafilms.models import Film

from .serializers import FilmSerializer


class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
