# Generated by Django 2.0.7 on 2018-07-05 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_remove_posts_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='posts',
            options={'ordering': ('-created',), 'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
    ]
