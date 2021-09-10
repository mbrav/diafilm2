from django.urls import path

from . import views

urlpatterns = [
    path('', views.author, name='author'),
    path('contact/', views.contact, name='contact'),
]
