# Generated by Django 4.0.4 on 2022-10-16 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0004_rename_modified_at_pokemon_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
