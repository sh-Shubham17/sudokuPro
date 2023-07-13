# Generated by Django 4.0.4 on 2023-07-13 06:52

import django.contrib.postgres.fields
from django.db import migrations, models
import puzzles.models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0023_rename_successrate_playingdata_success_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='playingdata',
            name='solved_timings',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=puzzles.models.get_default, size=None),
        ),
    ]