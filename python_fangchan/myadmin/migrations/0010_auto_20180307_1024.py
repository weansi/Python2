# Generated by Django 2.0.2 on 2018-03-07 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0009_auto_20180307_1006'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='name',
            new_name='me_name',
        ),
    ]
