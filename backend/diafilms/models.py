from django.db import models


class Film(models.Model):
    name = models.CharField(max_length=120)
    url = models.CharField(max_length=255, blank=True, null=True)
    studio = models.CharField(max_length=120, blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    color = models.CharField(max_length=120, blank=True, null=True)
    type = models.CharField(max_length=120, blank=True, null=True)
    index = models.CharField(max_length=120, blank=True, null=True)
    number = models.CharField(max_length=120, blank=True, null=True)
    film = models.CharField(max_length=120, blank=True, null=True)
    quality = models.CharField(max_length=120, blank=True, null=True)
    description = models.CharField(max_length=120, blank=True, null=True)

    def frames(self):
        return self.frames.all().count()

    class Meta:
        verbose_name = 'Diafilm'
        verbose_name_plural = 'Diafilms'

    def __str__(self):
        return "%s" % (self.name, )


class Image(models.Model):

    url = models.CharField(
        max_length=255,
        blank=False,
    )

    external = models.BooleanField(
        default=True,
        help_text="Set whether the image is external",
    )

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return "image #%s" % (self.id, )


class Frame(Image):

    film = models.ForeignKey(
        Film,
        related_name='frames',
        on_delete=models.CASCADE,
        help_text='Frames that the Film consists of',
    )

    sequence = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Frame'
        verbose_name_plural = 'Frames'

    def __str__(self):
        return "Frame #%s" % (self.id, )


class Category(models.Model):

    name = models.CharField(max_length=32)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return "%s" % (self.name, )


class Tag(models.Model):

    name = models.CharField(max_length=64)

    category = models.ForeignKey(
        Category,
        related_name='tags',
        on_delete=models.CASCADE,
        help_text='Tags that the Category has',
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return "%s" % (self.name, )
