from rest_framework import serializers

from apps.diafilms.models import Film, FilmCover


class FilmSerializer(serializers.ModelSerializer):

    groups = serializers.StringRelatedField(many=True)
    tags = serializers.StringRelatedField(many=True)

    film_cover = serializers.SerializerMethodField(
        method_name='get_cover_url')

    def get_cover_url(self, obj):
        cover = FilmCover.objects.get(film=obj)
        return cover.image.url

    class Meta:
        model = Film
        fields = ('id', 'name', 'url', 'film_cover', 'image', 'text', 'studio',
                  'year', 'color', 'index', 'number', 'quality', 'tags', 'groups')
