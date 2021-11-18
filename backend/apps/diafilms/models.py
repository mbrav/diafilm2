from django.db import models
from posts.models import Post


class Film(Post):

    name = models.CharField(
        max_length=120,
        verbose_name='Имя Диафильма',
    )

    url = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Ссылка на оригинальный пост на Diafilmy.su',
    )

    studio = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name='Студия диафильма',
    )

    year = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Год создания диафильма',
    )

    color = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name='Цвет диафильма',
    )

    index = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name='Индекс диафильма',
    )

    number = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name='Номер диафильма',
    )

    film_name = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name='Плёнка диафильма',
    )

    film_type = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name='Тип плёнки диафильма',
    )

    quality = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name='Качество диафильма',
    )

    def frames(self):
        return self.frames.all().count()

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Диафильм'
        verbose_name_plural = 'Диафильмы'

    def __str__(self):
        return f'{self.name[:15]}'


class Image(models.Model):

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации картинки',
        help_text='Укажите дату публикации картинки',
    )

    external = models.BooleanField(
        default=True,
        help_text="Укажите, если картинка внешняя, либо она локальная",
    )

    image = models.ImageField(
        'Картинка',
        upload_to='images/',
        help_text="Локальная картинка",
        blank=True
    )

    url = models.CharField(
        max_length=255,
        unique=False,
        blank=False,
        help_text="Внешняя картинка",
    )

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

    def __str__(self):
        return "Картинка #%s" % (self.id, )


class Frame(Image):

    film = models.ForeignKey(
        Film,
        related_name='frames',
        on_delete=models.CASCADE,
        help_text='Кадры из которых состоит Диафильм',
    )

    sequence = models.PositiveIntegerField(
        blank=True,
        null=True,
        unique=False,
        help_text='Последовательность кадра',
    )

    class Meta:
        verbose_name = 'Кадр'
        verbose_name_plural = 'Кадры'

    def __str__(self):
        return "Кадр #%s" % (self.id, )


class FilmCover(models.Model):

    film = models.OneToOneField(
        Film,
        related_name='cover',
        on_delete=models.CASCADE,
        help_text='Диафильм, к которому привязана обложка',
    )

    image = models.ForeignKey(
        Image,
        related_name='cover',
        unique=False,
        on_delete=models.CASCADE,
        help_text='Картинка обложки',
    )

    class Meta:
        verbose_name = 'Обложка диафильма'
        verbose_name_plural = 'Обложки диафильмов'

    def __str__(self):
        return "FilmCover #%s" % (self.id, )
