from django.db import models
from posts.models import Post


class Film(Post):
    name = models.CharField(max_length=120)
    url = models.CharField(max_length=255, blank=True, null=True)
    studio = models.CharField(max_length=120, blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    color = models.CharField(max_length=120, blank=True, null=True)
    type = models.CharField(max_length=120, blank=True, null=True)
    index = models.CharField(max_length=120, blank=True, null=True)
    number = models.CharField(max_length=120, blank=True, null=True)
    film_name = models.CharField(max_length=120, blank=True, null=True)
    quality = models.CharField(max_length=120, blank=True, null=True)

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
        help_text="Укажите, если картинка внешняя",
    )

    image = models.ImageField(
        'Картинка',
        upload_to='images/',
        blank=True
    )

    url = models.CharField(
        max_length=255,
        unique=False,
        blank=False,
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
