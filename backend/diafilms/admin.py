from django.contrib import admin
from diafilms.models import Film, Image, Frame, FilmCover


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

    empty_value_display = '-пусто-'
