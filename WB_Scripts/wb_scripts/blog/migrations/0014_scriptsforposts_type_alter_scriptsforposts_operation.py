# Generated by Django 4.1.6 on 2023-03-25 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_alter_newsforposts_options_alter_post_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scriptsforposts',
            name='type',
            field=models.CharField(choices=[('SC', 'Скрипт'), ('SV', 'Супервайзер'), ('PR', 'Проблема')], default='SC', max_length=2),
        ),
        migrations.AlterField(
            model_name='scriptsforposts',
            name='operation',
            field=models.CharField(default='Нет информации', max_length=250),
        ),
    ]
