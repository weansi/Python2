# Generated by Django 2.0.2 on 2018-03-07 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0011_auto_20180307_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.TextField(),
        ),
    ]