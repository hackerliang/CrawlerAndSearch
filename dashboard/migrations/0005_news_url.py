# Generated by Django 2.2.6 on 2019-11-30 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20191130_0332'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='url',
            field=models.URLField(blank=True, max_length=500),
        ),
    ]
