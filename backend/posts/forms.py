from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'groups', 'image',)
        labels = {
            'text': 'Текст нового поста',
            'groups': 'Группы, к которой будет относиться пост',
            'image': 'Картинка поста',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': 'Текст нового коммента',
        }
