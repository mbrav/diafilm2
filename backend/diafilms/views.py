from django.shortcuts import render


def home(request):
    return render(request, 'index.html', {'title': 'Δиа Фильм²'})


def post(request):
    return render(request, 'post.html', {'title': 'Δиа Фильм²'})


def about(request):
    return render(request, 'about.html', {'title': 'Δиа Фильм²'})


def contact(request):
    return render(request, 'contact.html', {'title': 'Δиа Фильм²'})
