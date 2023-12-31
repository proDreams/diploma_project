# Generated by Django 4.1.6 on 2023-03-28 18:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_alter_extendeduser_color_scheme'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='publish',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Опубликовано'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='body',
            field=models.TextField(verbose_name='Отзыв'),
        ),
    ]
