from django.shortcuts import render
from django.views.decorators.cache import cache_page


@cache_page(60 * 15)
def author(request):
    return render(request, 'about/author.html')


@cache_page(60 * 15)
def contact(request):
    return render(request, 'about/contact.html')
