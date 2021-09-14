from django.contrib import admin

from .models import Comment, Follow, GroupCategory, Post, Tag, TagCategory


@admin.register(GroupCategory)
class GroupCategoryAdmin(admin.ModelAdmin):
    list_per_page = 50

    list_display = (
        'id',
        'name',
        'slug',
        'description',
    )

    list_editable = (
        'slug',
    )

    ordering = (
        'name',
    )

    search_fields = (
        'name',
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_per_page = 50

    list_display = (
        'id',
        'pub_date',
        'modified_at',
        'author',
    )

    search_fields = (
        'text',
    )

    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_per_page = 50

    list_display = (
        'id',
        'text',
        'post',
        'author',
        'created',
    )

    list_filter = (
        'author',
    )

    search_fields = (
        'text',
        'post',
    )

    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_per_page = 50

    list_display = (
        'user',
        'author',
    )

    search_fields = (
        'user',
        'author',
    )

    list_filter = (
        'user',
        'author',
        'created',
    )

@admin.register(TagCategory)
class TagCategory(admin.ModelAdmin):
    list_per_page = 100

    list_display = (
        'id',
        'name',
        'slug',
    )

    search_fields = (
        'id',
        'name',
        'slug',
    )

    ordering = (
        'name',
    )

@admin.register(Tag)
class Tag(admin.ModelAdmin):
    list_per_page = 100

    list_display = (
        'id',
        'name',
        'slug',
        'category',
    )

    search_fields = (
        'id',
        'name',
        'slug',
        'category',
    )

    list_filter = (
        'category',
    )

    ordering = (
        'category',
        'name',
        'slug',
    )
