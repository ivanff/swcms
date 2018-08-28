# Generated by Django 2.0.3 on 2018-03-22 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0003_auto_20180322_1328'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subject',
            options={'ordering': ('-order',), 'verbose_name': 'тема помощи', 'verbose_name_plural': 'темы помощи'},
        ),
        migrations.AddField(
            model_name='subject',
            name='order',
            field=models.IntegerField(db_index=True, default=0, help_text='Меньше первее'),
        ),
        migrations.AlterIndexTogether(
            name='faq',
            index_together={('subject', 'order')},
        ),
    ]