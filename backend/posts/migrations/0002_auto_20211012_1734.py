# Generated by Django 3.2.8 on 2021-10-12 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='groups',
            field=models.ManyToManyField(help_text='Укажите группу (группы) поста', related_name='posts', to='posts.GroupCategory', verbose_name='Группы, которые присвоены посту'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(help_text='Укажите тэг (тэги) поста', related_name='posts', to='posts.Tag', verbose_name='Тэги, которые присвоены посту'),
        ),
    ]