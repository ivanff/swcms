# Generated by Django 2.0.2 on 2018-02-14 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('text_pages', '0003_auto_20180214_1401'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pages',
            old_name='description',
            new_name='desc',
        ),
        migrations.RenameField(
            model_name='pages',
            old_name='keywords',
            new_name='keys',
        ),
    ]
