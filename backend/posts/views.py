from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Group, Post


def index(request):
    latest_posts = Post.objects.order_by('-pub_date')[:10]
    return render(
        request,
        'index.html',
        {'title': 'yatube', 'posts': latest_posts}
    )


def group_posts(request, group_slug):
    group = get_object_or_404(Group, slug=group_slug)
    posts = Post.objects.filter(group__slug=group_slug)
    return render(
        request,
        'group_list.html',
        {'title': group.title, 'group': group, 'posts': posts}
    )
