# Generated by Django 2.2 on 2021-01-20 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20210120_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ref_code',
            field=models.CharField(default='123', max_length=20),
            preserve_default=False,
        ),
    ]