# Generated by Django 4.1.6 on 2023-03-15 06:00

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_post_options_post_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecentlyPosts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_visit', models.DateTimeField(auto_now=True)),
            ],
            managers=[
                ('rec_man', django.db.models.manager.Manager()),
            ],
        ),
    ]
