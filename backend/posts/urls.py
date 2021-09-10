from django.urls import path

from . import views

urlpatterns = [
    # Основное
    path('', views.index, name='index'),
    path('create/', views.post_create, name='post_create'),
    path('follow/', views.follow_index, name='follow_list'),
    path('diafilms/', views.diafilms, name='diafilms_list'),
    path('diafilms/random/', views.diafilms_random, name='diafilms_random'),
    path('group/<slug:group_slug>/', views.group_list, name='group_list'),

    # Профиль
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/follow/',
         views.profile_follow, name='follow_user'),
    path('profile/<str:username>/unfollow/',
         views.profile_unfollow, name='unfollow_user'),

    # Посты
    path('posts/<int:post_id>/', views.post, name='post'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('posts/<int:post_id>/comment/',
         views.add_comment, name='add_comment'),
    path('posts/<int:post_id>/comment/delete/<int:comment_id>/',
         views.delete_comment, name='delete_comment'),
]
