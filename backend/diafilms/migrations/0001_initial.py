# Generated by Django 3.2.4 on 2021-07-05 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('external', models.BooleanField(default=True, help_text='Set whether the image is external')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('category', models.ForeignKey(help_text='Tags that the Category has', on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='diafilms.category')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
                ('studio', models.CharField(blank=True, max_length=120, null=True)),
                ('year', models.PositiveIntegerField(blank=True, null=True)),
                ('color', models.CharField(blank=True, max_length=120, null=True)),
                ('type', models.CharField(blank=True, max_length=120, null=True)),
                ('index', models.CharField(blank=True, max_length=120, null=True)),
                ('number', models.CharField(blank=True, max_length=120, null=True)),
                ('film', models.CharField(blank=True, max_length=120, null=True)),
                ('quality', models.CharField(blank=True, max_length=120, null=True)),
                ('description', models.CharField(blank=True, max_length=120, null=True)),
                ('cover', models.ForeignKey(blank=True, help_text='Films where the image is used as a cover.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='film_covers', to='diafilms.image')),
            ],
            options={
                'verbose_name': 'Diafilm',
                'verbose_name_plural': 'Diafilms',
            },
        ),
        migrations.CreateModel(
            name='Frame',
            fields=[
                ('image_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='diafilms.image')),
                ('sequence', models.PositiveIntegerField(blank=True, null=True)),
                ('film', models.ForeignKey(help_text='Frames that the Film consists of', on_delete=django.db.models.deletion.CASCADE, related_name='frames', to='diafilms.film')),
            ],
            options={
                'verbose_name': 'Frame',
                'verbose_name_plural': 'Frames',
            },
            bases=('diafilms.image',),
        ),
    ]