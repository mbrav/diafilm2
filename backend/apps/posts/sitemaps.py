from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import GroupCategory, Post, Tag


class PostsSitemap(Sitemap):
    priority = 0.8
    limit = 200
    changefreq = 'weekly'
    protocol = 'http'

    def items(self):
        return Post.objects.all()

    def lastmod(self, item):
        return item.pub_date

    def location(self, item):
        url = reverse('posts:post', kwargs={
            'post_id': item.id})
        return url


class GroupsSitemap(Sitemap):
    priority = 0.5
    limit = 100
    changefreq = 'monthly'
    protocol = 'http'

    def items(self):
        return GroupCategory.objects.all()

    def location(self, item):
        url = reverse('posts:group_detail', kwargs={
            'group_slug': item.slug})
        return url


class TagsSitemap(Sitemap):
    priority = 0.7
    limit = 100
    changefreq = 'monthly'
    protocol = 'http'

    def items(self):
        return Tag.objects.all()

    def location(self, item):
        url = reverse('posts:tag_detail', kwargs={
            'tag_category_slug': item.category.slug,
            'tag_slug': item.slug,
        })
        return url


# class TagCategoriesSitemap(Sitemap):
#     priority = 0.5
#     changefreq = 'weekly'
#     protocol = 'http'

#     def items(self):
#         return TagCategory.objects.all()

#     def location(self, item):
#         url = reverse('posts:tag_category', kwargs={
#             'tag_category_slug': item.slug})
#         return url
