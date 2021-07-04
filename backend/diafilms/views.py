from django.shortcuts import render


def home(request):
    return render(request, 'index.html', {'title': 'Δиа Фильм²'})
