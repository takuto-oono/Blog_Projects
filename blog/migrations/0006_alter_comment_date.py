# Generated by Django 3.2.6 on 2022-03-09 01:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20220305_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 3, 9, 10, 36, 22, 5955), verbose_name='公開日'),
        ),
    ]