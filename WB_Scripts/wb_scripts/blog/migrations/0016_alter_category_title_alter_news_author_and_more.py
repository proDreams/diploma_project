# Generated by Django 4.1.6 on 2023-03-26 03:15

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0015_alter_newsforposts_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=250, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='news',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор новости'),
        ),
        migrations.AlterField(
            model_name='news',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Содержание новости'),
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=250, verbose_name='Название новости'),
        ),
        migrations.AlterField(
            model_name='news',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлено'),
        ),
        migrations.AlterField(
            model_name='news',
            name='view_count',
            field=models.IntegerField(default=1, verbose_name='Количество просмотров'),
        ),
        migrations.AlterField(
            model_name='newsforposts',
            name='news',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.news', verbose_name='Новость'),
        ),
        migrations.AlterField(
            model_name='newsforposts',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.post', verbose_name='Материал'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blog.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Опубликовано'),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('ЧЕ', 'Черновик'), ('ОП', 'Опубликовано')], default='ЧЕ', max_length=2, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=250, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлено'),
        ),
        migrations.AlterField(
            model_name='post',
            name='view_count',
            field=models.IntegerField(default=1, verbose_name='Количество просмотров'),
        ),
        migrations.AlterField(
            model_name='recentlyposts',
            name='date_visit',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата просмотра'),
        ),
        migrations.AlterField(
            model_name='recentlyposts',
            name='post',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blog.post', verbose_name='Материал'),
        ),
        migrations.AlterField(
            model_name='recentlyposts',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='scriptsforposts',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='scriptsforposts',
            name='operation',
            field=models.CharField(default='Нет информации', max_length=250, verbose_name='Операция'),
        ),
        migrations.AlterField(
            model_name='scriptsforposts',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post', verbose_name='Материал'),
        ),
        migrations.AlterField(
            model_name='scriptsforposts',
            name='script',
            field=models.TextField(verbose_name='Скрипт'),
        ),
        migrations.AlterField(
            model_name='scriptsforposts',
            name='title',
            field=models.CharField(max_length=250, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='scriptsforposts',
            name='type',
            field=models.CharField(choices=[('SC', 'Скрипт'), ('SV', 'Супервайзер'), ('PR', 'Проблема')], default='SC', max_length=2, verbose_name='Тип скрипта'),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Отзыв')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
    ]
