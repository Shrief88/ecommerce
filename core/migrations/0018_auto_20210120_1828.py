# Generated by Django 2.2 on 2021-01-20 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_refund'),
    ]

    operations = [
        migrations.RenameField(
            model_name='refund',
            old_name='Order',
            new_name='order',
        ),
    ]
