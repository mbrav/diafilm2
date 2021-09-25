import random
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from django.db.models import Q

from .forms import CommentForm, PostForm
from .models import Comment, Follow, GroupCategory, Post, User, Tag, TagCategory
from diafilms.models import Film, Frame


# @cache_page(60)
def index(request):
    post_view = request.GET.get('post_view')
    page_number = request.GET.get('page')

    post_list = None
    if post_view:
        films = Film.objects.all().values_list('id')
        post_list = Post.objects.select_related('author').prefetch_related('groups').exclude(
            id__in=films).all().order_by('-pub_date')
    else:
        post_list = Film.objects.select_related('author', 'cover').prefetch_related(
            'groups', 'cover__image').all().order_by('-id')

    paginator = Paginator(post_list, 12)
    page = paginator.get_page(page_number)

    frame_count = Frame.objects.all().count

    context = {
        'page_obj': page,
        'post_view': post_view,
        'index': True,
        'frame_count': frame_count,
    }

    return render(request, 'posts/index.html', context)


def profile(request, username):
    post_view = request.GET.get('post_view')
    page_number = request.GET.get('page')

    author = get_object_or_404(User, username=username)
    post_list = None
    if post_view:
        films = Film.objects.all().values_list('id')
        post_list = Post.objects.select_related('author').prefetch_related('groups').exclude(
            id__in=films).filter(author=author).order_by('-pub_date')
    else:
        post_list = Film.objects.select_related('author', 'cover').prefetch_related(
            'groups', 'cover__image').filter(author=author).order_by('-id')

    following = False
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user, author=author).first() is not None

    paginator = Paginator(post_list, 12)
    page = paginator.get_page(page_number)

    context = {
        'page_obj': page,
        'post_view': post_view,
        'author': author,
        'following': following,
    }

    return render(request, 'posts/profile.html', context)


def group_list(request, group_slug):
    post_view = request.GET.get('post_view')
    page_number = request.GET.get('page')

    group = get_object_or_404(GroupCategory, slug=group_slug)

    post_list = None
    if post_view:
        films = Film.objects.all().values_list('id')
        post_list = Post.objects.select_related('author').prefetch_related('groups').exclude(
            id__in=films).filter(groups=group).order_by('-pub_date')
    else:
        post_list = Film.objects.select_related('author', 'cover').prefetch_related(
            'groups', 'cover__image').filter(groups=group).order_by('-id')

    paginator = Paginator(post_list, 12)
    page = paginator.get_page(page_number)

    context = {
        'page_obj': page,
        'post_view': post_view,
        'group': group,
    }

    return render(request, 'posts/group_list.html', context)


def tag_category_list(request):
    page_number = request.GET.get('page')
    tag_category = request.GET.get('category')
    tag_categories = TagCategory.objects.all()

    tags = None
    if tag_category:
        tag_category = get_object_or_404(TagCategory, slug=tag_category)
        tags = Tag.objects.select_related('category').filter(category__slug=tag_category.slug).order_by('name')
    else:
        tags = Tag.objects.select_related('category').all().order_by('name')

    paginator = Paginator(tags, 100)
    page = paginator.get_page(page_number)

    context = {
        'page_obj': page,
        'category': tag_category,
        'tag_categories': tag_categories,
    }

    return render(request, 'posts/tag_category_list.html', context)


def tag_list(request, tag_category_slug, tag_slug):
    post_view = request.GET.get('post_view')
    page_number = request.GET.get('page')

    tag = get_object_or_404(
        Tag, slug=tag_slug, category__slug=tag_category_slug)

    post_list = None
    if post_view:
        films = Film.objects.all().values_list('id')
        post_list = Post.objects.select_related('author').prefetch_related('groups').exclude(
            id__in=films).filter(tags=tag).order_by('-pub_date')
    else:
        post_list = Film.objects.select_related('author', 'cover').prefetch_related(
            'groups', 'cover__image').filter(tags=tag).order_by('-id')

    paginator = Paginator(post_list, 12)
    page = paginator.get_page(page_number)

    context = {
        'page_obj': page,
        'post_view': post_view,
        'tag': tag,
    }

    return render(request, 'posts/tag_list.html', context)


def diafilms(request):
    page_number = request.GET.get('page')
    query = request.GET.get('q')

    post_list = None
    if query:
        # SQLite workaround
        # Ref: https://docs.djangoproject.com/en/dev/ref/databases/#substring-matching-and-case-sensitivity
        q_low = query.lower()
        q_cap = query.capitalize()
        post_list = Film.objects.filter(
            Q(name__icontains=q_low) | Q(name__icontains=q_cap)).order_by('id')
    else:
        post_list = Film.objects.all().order_by('id')

    paginator = Paginator(post_list, 100)
    page = paginator.get_page(page_number)

    context = {
        'page_obj': page,
        'query': query,
    }

    return render(request, 'posts/diafilm_list.html', context)


def diafilms_random(request):
    diafilms_ids = Film.objects.all().values_list('id')

    return redirect('posts:post', post_id=random.choice(diafilms_ids)[0])


def post(request, post_id):

    frames, post = None, None
    if Film.objects.filter(id=post_id).exists():
        post = get_object_or_404(Film.objects.select_related('author', 'cover').prefetch_related(
            'comments__post', 'comments__author', 'frames__film', 'tags', 'tags__category'), id=post_id)
        frames = post.frames
    else:
        post = get_object_or_404(Post.objects.select_related(
            'author').prefetch_related('comments__post', 'comments__author', 'tags', 'tags__category'), id=post_id)

    posts_by_user = Post.objects.filter(
        author=post.author).count()

    following = False
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user, author=post.author).first() is not None

    form = CommentForm(None)

    is_edit = request.user == post.author

    context = {
        'post': post,
        'frames': frames,
        'form': form,
        'posts_by_user': posts_by_user,
        'is_edit': is_edit,
        'following': following,
    }

    return render(request, 'posts/post_detail.html', context)


@login_required(login_url='/auth/login/')
def post_create(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=post.author.username)

    context = {
        'form': form,
    }

    return render(request, 'posts/create_post.html', context)


@login_required(login_url='/auth/login/')
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(
        request.POST or None,
        instance=post,
        files=request.FILES or None,)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.save()
        return redirect(
            'posts:post',
            post_id=post_id)

    is_edit = request.user == post.author

    context = {
        'form': form,
        'username': request.user,
        'is_edit': is_edit,
        'post': post
    }

    return render(request, 'posts/update_post.html', context)


@login_required(login_url='/auth/login/')
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author == request.user:
        post.delete()

    return redirect('posts:index')


@login_required(login_url='/auth/login/')
def add_comment(request, post_id):
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post, id=post_id)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

    return redirect('posts:post', post_id=post.id)


@login_required(login_url='/auth/login/')
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author == request.user:
        comment.delete()

    return redirect('posts:post', post_id=post_id)


@login_required(login_url='/auth/login/')
def follow_index(request):
    post_view = request.GET.get('post_view')
    page_number = request.GET.get('page')

    usernames = Follow.objects.filter(
        user=request.user).values_list('author')
    post_list = None
    if post_view:
        post_list = Film.objects.select_related('group', 'author', 'cover').filter(
            author__in=usernames).order_by('-id')
    else:
        films = Film.objects.all().values_list('id')
        post_list = Post.objects.select_related('group', 'author').filter(
            author__in=usernames).exclude(id__in=films).order_by('-pub_date')

    paginator = Paginator(post_list, 12)
    page = paginator.get_page(page_number)

    context = {
        'page_obj': page,
        'post_view': post_view,
        'following': usernames,
    }

    return render(request, 'posts/follow_list.html', context)


@login_required(login_url='/auth/login/')
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)

    if author != request.user:
        Follow.objects.get_or_create(
            user=request.user,
            author=author)

    return redirect('posts:follow_list')


@login_required(login_url='/auth/login/')
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)

    follow = Follow.objects.filter(
        user=request.user,
        author=author)

    if follow.exists():
        follow.delete()

    return redirect('posts:follow_list')
