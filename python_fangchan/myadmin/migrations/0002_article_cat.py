# Generated by Django 2.0.2 on 2018-03-01 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='cat',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myadmin.article_cat'),
            preserve_default=False,
        ),
    ]