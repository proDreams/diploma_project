# Generated by Django 4.1.6 on 2023-03-24 18:59

import ckeditor.fields
from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_newsforposts_news_alter_newsforposts_post'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='newsforposts',
            managers=[
                ('nfp_man', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='news',
            name='body',
            field=ckeditor.fields.RichTextField(),
        ),
    ]