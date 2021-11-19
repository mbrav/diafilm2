from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.diafilms.models import Film


class FilmSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(
    #     read_only=True,
    #     many=False
    # )
    # genre = GenreSerializer(
    #     read_only=True,
    #     many=True
    # )

    # rating = serializers.SerializerMethodField(
    #     read_only=True,
    #     method_name='get_rating')

    # def get_rating(self, obj):
    #     reviews = obj.reviews.all()
    #     score_avg = reviews.aggregate(models.Avg('score')).get('score__avg')
    #     return None if isinstance(score_avg, type(None)) else int(score_avg)

    class Meta:
        model = Film
        fields = ('__all__')
