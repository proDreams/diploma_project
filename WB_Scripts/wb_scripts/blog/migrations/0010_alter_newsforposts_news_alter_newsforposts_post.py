# Generated by Django 4.1.6 on 2023-03-23 04:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_news_newsforposts_news_blog_news_updated_cb1b36_idx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsforposts',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.news'),
        ),
        migrations.AlterField(
            model_name='newsforposts',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post'),
        ),
    ]
