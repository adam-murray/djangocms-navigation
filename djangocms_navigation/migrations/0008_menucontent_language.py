# Generated by Django 2.2.13 on 2020-06-26 05:17

import cms.utils.i18n
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_navigation', '0007_auto_20200302_0853'),
    ]

    operations = [
        migrations.AddField(
            model_name='menucontent',
            name='language',
            field=models.CharField(db_index=True, default="", max_length=15, verbose_name='language', blank=True),
        ),
    ]
