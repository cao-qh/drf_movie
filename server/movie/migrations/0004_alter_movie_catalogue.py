# Generated by Django 4.2.4 on 2025-05-05 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_remove_movie_actors_remove_movie_alternate_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='catalogue',
            field=models.TextField(max_length=1000, verbose_name='目录'),
        ),
    ]
