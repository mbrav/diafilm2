import random

from django.shortcuts import render
from django.db.models import Max

from diafilms.models import Film, Frame


def home(request):
    return render(request, 'index.html', {'title': 'Δиа Фильм²'})


def post(request):
    max_id = Film.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        rand_film = Film.objects.get(pk=pk)

        if rand_film:
            frames = Frame.objects.filter(film_id=pk)
            return render(
                request, 'post.html',
                {'post': rand_film, 'frames': frames}
            )


def about(request):
    return render(request, 'about.html', {'title': 'Δиа Фильм²'})


def contact(request):
    return render(request, 'contact.html', {'title': 'Δиа Фильм²'})
