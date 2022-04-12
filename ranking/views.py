from re import I
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse
from django.shortcuts import render
from puzzles.models import PlayingData , DificultyLevel
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
            message = "No Levels found."
            return render(request, 'ranking.html', {'message': message} )

    else:
        message = "No Levels found."
        return render(request, 'ranking.html', {'message': message} )
   
