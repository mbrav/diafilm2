# Generated by Django 3.2.7 on 2021-09-13 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='posts.post')),
                ('name', models.CharField(max_length=120, verbose_name='Имя Диафильма')),
                ('url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ссылка на оригинальный пост на Diafilmy.su')),
                ('studio', models.CharField(blank=True, max_length=120, null=True, verbose_name='Студия диафильма')),
                ('year', models.PositiveIntegerField(blank=True, null=True, verbose_name='Год создания диафильма')),
                ('color', models.CharField(blank=True, max_length=120, null=True, verbose_name='Цвет диафильма')),
                ('index', models.CharField(blank=True, max_length=120, null=True, verbose_name='Индекс диафильма')),
                ('number', models.CharField(blank=True, max_length=120, null=True, verbose_name='Номер диафильма')),
                ('film_name', models.CharField(blank=True, max_length=120, null=True, verbose_name='Плёнка диафильма')),
                ('film_type', models.CharField(blank=True, max_length=120, null=True, verbose_name='Тип плёнки диафильма')),
                ('quality', models.CharField(blank=True, max_length=120, null=True, verbose_name='Качество диафильма')),
            ],
            options={
                'verbose_name': 'Диафильм',
                'verbose_name_plural': 'Диафильмы',
                'ordering': ('-id',),
            },
            bases=('posts.post',),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True, help_text='Укажите дату публикации картинки', verbose_name='Дата публикации картинки')),
                ('external', models.BooleanField(default=True, help_text='Укажите, если картинка внешняя, либо она локальная')),
                ('image', models.ImageField(blank=True, help_text='Локальная картинка', upload_to='images/', verbose_name='Картинка')),
                ('url', models.CharField(help_text='Внешняя картинка', max_length=255)),
            ],
            options={
                'verbose_name': 'Картинка',
                'verbose_name_plural': 'Картинки',
            },
        ),
        migrations.CreateModel(
            name='FilmCover',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('film', models.OneToOneField(help_text='Диафильм, к которому привязана обложка', on_delete=django.db.models.deletion.CASCADE, related_name='cover', to='diafilms.film')),
                ('image', models.ForeignKey(help_text='Картинка обложки', on_delete=django.db.models.deletion.CASCADE, related_name='cover', to='diafilms.image')),
            ],
            options={
                'verbose_name': 'Обложка диафильма',
                'verbose_name_plural': 'Обложки диафильмов',
            },
        ),
        migrations.CreateModel(
            name='Frame',
            fields=[
                ('image_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='diafilms.image')),
                ('sequence', models.PositiveIntegerField(blank=True, help_text='Последовательность кадра', null=True)),
                ('film', models.ForeignKey(help_text='Кадры из которых состоит Диафильм', on_delete=django.db.models.deletion.CASCADE, related_name='frames', to='diafilms.film')),
            ],
            options={
                'verbose_name': 'Кадр',
                'verbose_name_plural': 'Кадры',
            },
            bases=('diafilms.image',),
        ),
    ]
