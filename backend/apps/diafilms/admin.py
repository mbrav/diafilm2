from apps.diafilms.models import Film, FilmCover, Frame, Image
from django.contrib import admin


@admin.register(Film)
class Film(admin.ModelAdmin):
    list_per_page = 100
    list_display = (
        'id',
        'name',
        'pub_date',
        'modified_at',
        'year',
    )

    search_fields = (
        'id',
        'name',
    )

    ordering = (
        '-id',
    )

    autocomplete_fields = ['groups', 'tags']
    empty_value_display = '-пусто-'


@admin.register(Image)
class Image(admin.ModelAdmin):
    list_per_page = 100

    empty_value_display = '-пусто-'


@admin.register(Frame)
class Frame(admin.ModelAdmin):
    list_per_page = 100

    list_display = (
        'id',
        'film',
        'sequence',
    )

    search_fields = (
        'sequence',
    )

    ordering = (
        'film',
        'sequence',
    )

    autocomplete_fields = ['film']
    empty_value_display = '-пусто-'


@admin.register(FilmCover)
class FilmCover(admin.ModelAdmin):
    list_per_page = 100

    list_display = (
        'id',
        'film',
    )

    ordering = (
        'film',
    )

    autocomplete_fields = ['film']
    raw_id_fields = ['image']
    empty_value_display = '-пусто-'
