# Generated by Django 2.2 on 2021-01-13 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20210113_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingaddress',
            name='city',
            field=models.CharField(default='cario', max_length=100),
            preserve_default=False,
        ),
    ]