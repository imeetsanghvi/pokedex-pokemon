# Generated by Django 3.2.5 on 2021-07-19 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0002_remove_type_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='type',
            name='image',
            field=models.URLField(default=''),
        ),
    ]
