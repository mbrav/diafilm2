from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class GroupCategory(models.Model):

    name = models.CharField(
        max_length=120,
        unique=True,
        verbose_name='Имя категории постов',
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
        verbose_name='Slug категории постов',
    )

    description = models.TextField(
        blank=True,
        verbose_name='Описание категории постов',
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):

    text = models.TextField(
        verbose_name='Текст',
        help_text='Напишите текст поста',
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации поста',
        help_text='Укажите дату публикации поста',
    )

    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последней редакции поста',
        help_text='Дате последней редакции поста',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор поста',
        help_text='Укажите автора поста',
    )

    groups = models.ManyToManyField(
        GroupCategory,
        related_name="posts",
        verbose_name='Tэги, которые присвоены посту',
        help_text='Укажите группу (группы) поста',
    )

    tags = models.ManyToManyField(
        'Tag',
        related_name="posts",
        verbose_name='Группы, которые присвоены посту',
        help_text='Укажите тэг (тэги) поста',
    )

    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return f'{self.text[:15]}'


class TagCategory(models.Model):

    name = models.CharField(
        max_length=120,
        unique=True,
        verbose_name='Имя категории тэгов',
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
        verbose_name='Slug категории тэгов',
    )

    class Meta:
        verbose_name = 'Категория тэгов'
        verbose_name_plural = 'Категории тэгов'

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):

    name = models.CharField(
        max_length=120,
        verbose_name='Имя тэгa',
    )

    slug = models.SlugField(
        max_length=120,
        verbose_name='Slug тэгa',
    )

    category = models.ForeignKey(
        TagCategory,
        related_name='tags',
        on_delete=models.CASCADE,
        help_text='Группа тэгов, к которому присвоен тэг',
    )

    class Meta:
        unique_together = ('name', 'category')
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return f'{self.name}'


class Comment(models.Model):

    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Напишите текст комментария',
    )

    post = models.ForeignKey(
        Post,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='comments',
        verbose_name='Комменты поста',
        help_text='Укажите пост коммента',
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации комментария',
        help_text='Укажите дату и время публикации комментария',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комменты пользователя',
        help_text='Укажите автора коммента',
    )

    class Meta:
        verbose_name = 'Коммент'
        verbose_name_plural = 'Комменты'

    def __str__(self):
        return f'{self.text[:15]}'


class Follow(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подпискa пользователя',
        help_text='Укажите пользователя подписки',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписка на пользователя',
        help_text='Укажите пользователя на которого подписываются',
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата подписки',
        help_text='Укажите дату и время начала подписки на пользователя',
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user}'
