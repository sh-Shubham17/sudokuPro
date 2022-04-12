from django.contrib import admin
from .models import Puzzle,DificultyLevel, PlayingData
#Register your models here.

class DificultyLevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'best_Time')

class PuzzleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'source']

class PlayingDataAdmin(admin.ModelAdmin):
    list_display = ['id','username','level','win_percentage','successful_attempts','unsuccessful_attempts','best_Time', 'avg_Time' ]
    

admin.site.register(Puzzle)
admin.site.register(DificultyLevel)
admin.site.register(PlayingData)