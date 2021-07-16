# Generated by Django 3.1.5 on 2021-07-16 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_carousel'),
    ]

    operations = [
        migrations.AddField(
            model_name='carousel',
            name='published',
            field=models.BooleanField(default=False, verbose_name='published'),
        ),
        migrations.AddField(
            model_name='project',
            name='published',
            field=models.BooleanField(default=True, verbose_name='published'),
        ),
    ]