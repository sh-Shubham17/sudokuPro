# Generated by Django 4.0.1 on 2022-03-11 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0018_rename_avg_besttime_minutes_playingdata_avg_time_minutes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playingdata',
            name='avg_Time_minutes',
        ),
        migrations.RemoveField(
            model_name='playingdata',
            name='avg_Time_seconds',
        ),
        migrations.RemoveField(
            model_name='playingdata',
            name='bestTime_minutes',
        ),
        migrations.RemoveField(
            model_name='playingdata',
            name='bestTime_seconds',
        ),
        migrations.AddField(
            model_name='dificultylevel',
            name='best_Time',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playingdata',
            name='avg_Time',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playingdata',
            name='best_Time',
            field=models.IntegerField(default=0),
        ),
    ]
