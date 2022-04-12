from django.urls import path
from . import views

app_name = 'puzzles'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:level_id>', views.play, name='play'),
    path('get_time', views.get_time, name='get_time')
]