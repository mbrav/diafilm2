import random

from django.shortcuts import render
from django.db.models import Max

from diafilms.models import Film, Frame, FilmCover


def home(request):
    latest_films = Film.objects.order_by('-id')[:10]
    return render(request, 'index.html', {'title': 'Δиа Фильм²', 'posts': latest_films})


def post(request):
    max_id = Film.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        film = Film.objects.get(pk=pk)

        if film:
            frames = Frame.objects.filter(film_id=pk).order_by('sequence')
            return render(
                request, 'post.html',
                {'post': film, 'frames': frames}
            )


def post_detail(request, post_id):
    film = Film.objects.get(pk=post_id)

    frames = Frame.objects.filter(film_id=post_id).order_by('sequence')
    return render(
        request, 'post.html',
        {'post': film, 'frames': frames}
    )


def about(request):
    return render(request, 'about.html', {'title': 'Δиа Фильм²'})


def contact(request):
    return render(request, 'contact.html', {'title': 'Δиа Фильм²'})
