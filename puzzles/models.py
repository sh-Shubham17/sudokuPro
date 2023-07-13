from email.policy import default
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

# Create your models here.
class DificultyLevel(models.Model):
    """ model class for levels table"""
    name = models.CharField(max_length=50)
    best_Time = models.IntegerField(default = 0)
    avg_Time = models.IntegerField(default = 0)
    attempts = models.IntegerField(default = 0)
    number_of_empty_cells = models.IntegerField(default = 0)
    def __str__(self):
        return self.name


def get_default():
    """ This method is used to initialise default value to puzzle rows
    returns : 1 dim list having elements with 0 as each element """
#     #return [0 for i in range(1,10)]
    return [0 for i in range(1,10)]



class Puzzle(models.Model):
    """ model for puzzle table 
    have attributes that each puzzle row will going to have"""
    title = models.CharField(max_length=100)
    qrow1 = ArrayField(models.IntegerField(),size=9,default = get_default)
    qrow2 = ArrayField(models.IntegerField(),size=9,default = get_default)
    qrow3 = ArrayField(models.IntegerField(),size=9,default = get_default)
    qrow4 = ArrayField(models.IntegerField(),size=9,default = get_default)
    qrow5 = ArrayField(models.IntegerField(),size=9,default = get_default)
    qrow6 = ArrayField(models.IntegerField(),size=9,default = get_default)
    qrow7 = ArrayField(models.IntegerField(),size=9,default = get_default)
    qrow8 = ArrayField(models.IntegerField(),size=9,default = get_default)
    qrow9 = ArrayField(models.IntegerField(),size=9,default = get_default)

    dificultyLevel = models.ForeignKey(DificultyLevel, on_delete=models.CASCADE)

    date_created = models.DateTimeField(default = timezone.now)
    source = models.CharField(default="https://websudoku.com/" ,max_length=100)

    def __str__(self):
        return self.title

class PlayingData(models.Model):
    """To store playing data of each user seprate rows for seprate levels"""
    username = models.CharField( max_length=250)
    level = models.ForeignKey(DificultyLevel, on_delete=models.CASCADE )
    success_rate = models.FloatField(default=0.0)
    correct_attempts = models.IntegerField(default = 0)
    incorrect_attempts = models.IntegerField(default = 0)
    best_Time = models.IntegerField(default = 0)
    avg_Time  = models.IntegerField(default = 0)
    solved_timings = ArrayField(models.IntegerField())

    worst_Time = models.IntegerField(default = 0)
    def __str__(self):
        return self.username
