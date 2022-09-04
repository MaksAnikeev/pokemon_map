# Generated by Django 2.2.24 on 2022-09-02 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0002_auto_20220901_0733'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='title_en',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='title_jp',
            field=models.CharField(max_length=200, null=True),
        ),
    ]