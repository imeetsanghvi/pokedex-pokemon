# Generated by Django 3.2.5 on 2021-07-19 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='type',
            name='image',
        ),
    ]
