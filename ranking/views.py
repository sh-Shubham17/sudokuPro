from re import I
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse
from django.shortcuts import render
from puzzles.models import PlayingData , DificultyLevel
import matplotlib.pyplot as plt
import os
import numpy as np

# Create your views here.


def dashboard(request):
    """ This method id used to get data from database and send it in form of dictionary to display is dashboard.html page
    Parameter:
        request object
    returns:
        render method, 
            dictionary have data rows as list as key value pair
            data can be send in format of dictionary only """
    user_data_rows = PlayingData.objects.all().filter(username = request.user.username)
    user_data_rows = user_data_rows.order_by('best_Time')
    for user_data_row in user_data_rows:
        render_pie_chart(user_data_row.username, user_data_row.level, user_data_row.incorrect_attempts, user_data_row.correct_attempts)
        plot_improvement_graph( user_data_row.username, user_data_row.level, user_data_row.solved_timings)

    return render(request, 'dashboard.html', {'user_data': user_data_rows})

def rankings(request):
    """To get data for ranking and send it to ranking.html to display
    description : gets users playing data for particular level then sort data according to sorting criteria ,
    Paramenter : request object
    returns  : render method
        in dictionary
        string: level_choosed, 
        list : all_levels,
        string : current_criteria( for sorting 0,
        list : all fields( which can be used to do ranking  for eg best_Time, worst_Time ),
        list : all player data rows who have played that level
    """
    levels = DificultyLevel.objects.all().order_by('number_of_empty_cells')
    if( levels ):
        if request.method == "POST":
            if request.POST.get("get_ranks") == "True":
                print('getting value',request.POST.get("level_selected"))
                level_name = request.POST.get("level_selected")
                print(level_name)
                order_criteria = request.POST.get("sort_by")
                current_level = get_object_or_404(DificultyLevel ,name = level_name)
                # we need to sort success rate, correct_attempts, worst time in decreasing order thus in value fields
                #-ve is prefixed in value attribute in rnaking.html page
        else:
            current_level = levels[0]
            order_criteria = "best_Time"
            
        datarows = current_level.playingdata_set.all().order_by(order_criteria)
        #print(datarows[0].best_Time)
        order_fields = ['best_Time' , 'avg_Time' , '-worst_Time', '-correct_attempts' , '-success_rate', 'incorrect_attempts']
        message = ""
        if( datarows):
            return render(request, 'ranking.html', { 'all_levels':levels,'current_level':current_level,'current_criteria':order_criteria,'fields':order_fields, 'ranking_data': datarows})
        else:
            message = "No record found."
            return render(request, 'ranking.html', {'message': message} )

    else:
        message = "No record found."
        return render(request, 'ranking.html', {'message': message} )
   

def render_pie_chart(username, level, incorrect, correct):
    # Create a dark background style
    plt.style.use('dark_background')
    # Create a new figure and axes for each plot
    fig, ax = plt.subplots()
    
    # Data for the pie chart
    data = [incorrect, correct]
    
    # Labels for the chart
    labels = ['Incorrect', 'Correct']
    
    # Colors for the chart
    colors = ['#FF4F4F', '#68FF96']
    
    # Create the pie chart on the axes
    ax.pie(data, labels=labels, colors=colors, autopct='%1.1f%%')
    
    # Add a title to the axes
    ax.set_title('Sudoku Puzzle Attempts')

    # Generate the filename with the username and level as prefix
    filename = f"{username}_{level}_pie_chart.png"
    
    # Specify the image saving path relative to the static folder
    save_path = os.path.join('static/ranking', filename)
    
    # Save the figure to the specified path
    fig.savefig(save_path)
    
    # Close the figure to release memory
    plt.close(fig)

# Example usage
# username = 'john_doe'
# incorrect_attempts = 3
# correct_attempts = 7


def plot_improvement_graph(username, level, times):
    # Calculate the reciprocal of time values
    reciprocals = [1 / t for t in times]
    
    # Create a dark background style
    plt.style.use('dark_background')
    
    # Create a figure and axes
    fig, ax = plt.subplots()
    # Generate X-axis ticks starting from 1
    x_ticks = np.arange(1, len(times) + 1)
    
    # Plot the line graph
    ax.plot(x_ticks, reciprocals, marker='o', markersize=5, linestyle='-', color='aqua')
    
    # Plot the line graph
    # Save the figure to the specified path
    # Set the labels and title
    ax.set_xlabel('Attempts')
    ax.set_ylabel('1 / Time (s)')
    ax.set_title('Improvement Graph')

    # Generate the filename with the username and level as prefix
    filename = f"{username}_{level}_line_plot.png"

    # Specify the image saving path relative to the static folder
    save_path = os.path.join('static/ranking', filename)
    
    # Save the figure to the specified path
    fig.savefig(save_path)
    plt.close(fig)