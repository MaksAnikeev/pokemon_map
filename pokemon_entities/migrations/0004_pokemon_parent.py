# Generated by Django 2.2.24 on 2022-09-03 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0003_auto_20220902_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pokemon_entities.Pokemon'),
        ),
    ]
