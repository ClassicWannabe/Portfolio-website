# Generated by Django 3.1.5 on 2021-07-16 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20210716_1234'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carousel',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='document',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='link',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='carousel',
            name='order',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='order'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='order',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='order'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='link',
            name='order',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='order'),
            preserve_default=False,
        ),
    ]
