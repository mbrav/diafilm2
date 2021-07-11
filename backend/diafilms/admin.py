from django.contrib import admin
from diafilms.models import Film, Image, Frame, FilmCover, Category, Tag


@admin.register(Film)
class Film(admin.ModelAdmin):
    list_per_page = 100
    list_display = (
        'name',
        'studio',
        'year',
        # 'frames',
        'id',
    )

    search_fields = (
        'name',
        'studio',
    )

    ordering = (
        '-id',
    )


@admin.register(Image)
class Image(admin.ModelAdmin):
    list_per_page = 100


@admin.register(Frame)
class Frame(admin.ModelAdmin):
    list_per_page = 100

    list_display = (
        'film',
        'sequence',
        'id',
    )

    search_fields = (
        'sequence',
    )

    ordering = (
        'film',
        'sequence',
    )


@admin.register(FilmCover)
class FilmCover(admin.ModelAdmin):
    list_per_page = 100

    list_display = (
        'film',
        'id',
    )

    ordering = (
        'film',
    )


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_per_page = 100

    list_display = (
        'name',
        'id',
    )

    ordering = (
        'name',
        'id',
    )


@admin.register(Tag)
class Tag(admin.ModelAdmin):
    list_per_page = 100

    list_display = (
        'name',
        'category',
        'id',
    )

    search_fields = (
        'name',
        'category',
    )

    ordering = (
        'category',
        'name',
    )
