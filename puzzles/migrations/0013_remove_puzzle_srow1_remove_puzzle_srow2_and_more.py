# Generated by Django 4.0.1 on 2022-02-21 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0012_puzzle_besttime_minutes_puzzle_besttime_seconds'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='puzzle',
            name='srow1',
        ),
        migrations.RemoveField(
            model_name='puzzle',
            name='srow2',
        ),
        migrations.RemoveField(
            model_name='puzzle',
            name='srow3',
        ),
        migrations.RemoveField(
            model_name='puzzle',
            name='srow4',
        ),
        migrations.RemoveField(
            model_name='puzzle',
            name='srow5',
        ),
        migrations.RemoveField(
            model_name='puzzle',
            name='srow6',
        ),
        migrations.RemoveField(
            model_name='puzzle',
            name='srow7',
        ),
        migrations.RemoveField(
            model_name='puzzle',
            name='srow8',
        ),
        migrations.RemoveField(
            model_name='puzzle',
            name='srow9',
        ),
    ]
