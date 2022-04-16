
import inspect
# Create your views here.
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404 , redirect
from .models import Puzzle, PlayingData
from .models import DificultyLevel
import time
import random
from sudoku import globals  #gobals is an object that contains all globals varibale we have defined
# Create your views here.
def reInitializeGlobals():
    """To reinitialise globals attributes for re use"""
    globals.invalidInput = False
    globals.puzzleSubmit = False


def index(request):
    """ to fetch all level ojects from database and send them in dictionary to index.html template
    Parameter : request object
    retunrs : render method 
        levels | levelm objects( rows in data table) """
    levels = DificultyLevel.objects.all().order_by('number_of_empty_cells')
    return render(request, 'puzzles/index.html', {'levels':levels})

def updatePlayingData(solved,Level, userName):
    """To update playing data table after user clicks submit button while playing game
    if user is new, then it'll create a object of playnigdata and add new row for new user
    parameter : 
        bool | solved ( True or False)
        level object | Level
        string | userName 
    returns : None
    """
    playerLevelData = Level.playingdata_set.all().filter(username = userName) # , it rerurns list of objects thus we will access its 0th index element(data object)
    # print("were in update playing data row")
    # print('level data row',playerLevelData)
    if playerLevelData:
        playerLevelData = playerLevelData[0]
        #print('we can update existing row')
        if solved :
            # for best time either it can be best time or worst time or it can be neither best nor worst thus calling only 1 method
            playerLevelData.best_Time = globals.calculateBestTime(playerLevelData.best_Time, globals.timeElapsed)
            playerLevelData.worst_Time = globals.calculateWorstTime(playerLevelData.worst_Time, globals.timeElapsed)

            # for success percentage
            playerLevelData.correct_attempts +=1 
            playerLevelData.success_rate = 100 * playerLevelData.correct_attempts / (playerLevelData.correct_attempts + playerLevelData.incorrect_attempts)

            # for average best time
            playerLevelData.avg_Time = globals.calculateAverageTime(playerLevelData.avg_Time, globals.timeElapsed, playerLevelData.correct_attempts)   

        else:
            # if puzzle is not solved
            playerLevelData.incorrect_attempts +=1 
            playerLevelData.success_rate = 100 * playerLevelData.correct_attempts / (playerLevelData.correct_attempts + playerLevelData.incorrect_attempts)
        playerLevelData.save()


    else :
        #print("we have to add row in our database")
        if solved:
            new_level_for_user = PlayingData(username = userName , level = Level, success_rate = 100 , correct_attempts = 1 , best_Time = globals.timeElapsed , avg_Time = globals.timeElapsed, worst_Time = globals.timeElapsed)
        else :
            new_level_for_user = PlayingData(username = userName , level = Level, incorrect_attempts = 1 )
        new_level_for_user.save()

def get_userSolution(request):
    userSolution = [[0 for i in range(9)] for j in range(9)]    #initialising a 9 X 9 list
    # now we will read user's data
    numbersCheck = [str(x) for x in range(0,10)]
    globals.invalidInput = False
    for i in range(9):
        s = str(i+1)    #converting i+1 index to string so that
        for j in range(9):
            key_name = "row"+s+"col"+str(j+1)
            value = request.POST.get(key_name)
            if(value == '' or (value not in numbersCheck)):
                globals.invalidInput = True
                userSolution[i][j] = value
            else:
                userSolution[i][j] = int(value)

    return userSolution

def removeDigits(puzzleObj, puzzle):
    """
    This method is used to remove random digits from sudoku puzzle
    this will generate new puzzle every time user visits or reloads
    Parameters :
        puzzle object | puzzleObj
        2d List | puzzle
    returns : 2d list | puzzle ( with certain number of cells emtied)
    """
    # print(puzzleObj)
    # print("our level is ",puzzleObj.dificultyLevel.name, type(puzzleObj.dificultyLevel.name))
    removedigits = puzzleObj.dificultyLevel.number_of_empty_cells
    while(removedigits >0):
        cellid = random.randint(0,80)
        row = cellid//9
        col = cellid%9
        #print(row, col)
        if not puzzle[row][col] == 0 :
            removedigits -=1
            puzzle[row][col] = 0
    return puzzle
    #print(userSolution)


def getRandomPuzzle(level):
    """
    to select random puzzle of given level from the set of puzzle we have in our database
    Parameter : object of level class | 'level' 
    returns : puzzle Object | 'random_puzzle'
    """
   # tryobjs = Puzzle.objects.filter(dificultyLevel__name__contains = "Easy") #another way to get all objects with given foriegn key name
   # print("try objects " ,tryobjs)
   
    puzzlesObj = level.puzzle_set.all()     #this helps us gives all puzzles with given level , it rerurns list of objects
    #puzzlesObj = Puzzle.objects.select_related().filter(id = level_id)

    #print(puzzlesObj, type(puzzlesObj ), puzzlesObj.count())
    # puzzle = puzzlesObj[0]      
    # we can see we can access puzzle pbjects using indexing
    # print(puzzle.title, puzzle.source)
    print(puzzlesObj)
    print(puzzlesObj is None)
    print(len(puzzlesObj))
    if(len(puzzlesObj) > 0 ):
        puzzles_count = puzzlesObj.count() -1
        random_puzzle = puzzlesObj[ random.randint(0,puzzles_count)]
    else:
         return None
    #print("random puzzle", random_puzzle)
    return random_puzzle



# to avoid putting whole render function again and again in play function I defined renderPlay function
def renderPlay(request, playdictionary): 
    return render(request,'puzzles/play.html', playdictionary ) # renderPlay will return render function to our play function which will return it again to render template when called

def changePuzzle(levelObj):
    puzzleObj = getRandomPuzzle(levelObj)
    message = 'solve the puzzle below'
    sudokuPuzzle = []
    if( puzzleObj):
        sudokuPuzzle = [
            puzzleObj.qrow1,puzzleObj.qrow2,puzzleObj.qrow3,puzzleObj.qrow4,puzzleObj.qrow5,puzzleObj.qrow6,puzzleObj.qrow7,puzzleObj.qrow8,puzzleObj.qrow9
        ]           #2d list puzzleObj
        sudokuPuzzle = removeDigits(puzzleObj, sudokuPuzzle)
    else :
        message = "No puzzles found! :("
    globals.playdictionary = {'mysudoku':sudokuPuzzle , 'message': message , 'puzzleObj': puzzleObj, 'gamefinished': False}



def play(request, level_id):
    """
    To handly whole play function , 
    it handles user input data, user button clicks like restart , clear and submit puzzle 
    operations :
    clear | this button is used to clear all inputs done to a puzzle wihtout changing current puzzle and time 
    submit | this button is used for submission of solution solved by user
    restart | to random puzzle 

    Parameters :
        object : request
        int : level_id
    
    returns :
        render method | with dictionary containing message and puzzle to display
    """
    #print(request.user)
    reInitializeGlobals()
    #print(level_id)
    #print("we are in puzzles")
    puzzle_level = get_object_or_404(DificultyLevel, pk = level_id)    #to get level object of given level id , we can get object usinglevel id only
    # we can also do like (id = level_id)    
    if request.method == "POST":

        if request.POST.get("restart") =="True":
            return redirect("puzzles:play", level_id = level_id)

        elif request.POST.get("clearAll") =="True":
            return renderPlay(request,globals.playdictionary)

        elif request.POST.get("finish") == "True":
            globals.playdictionary['gamefinished']= True # we need this so I can diable submit and cleaall buttons after user finisged the game so it will
            # prevent user from starting timer and game again with all data showed in sudoku table. only way to replay should be restart button only 
            globals.puzzleSubmit = True
            userSolution =  get_userSolution(request)
            globals.playdictionary['mysudoku'] = userSolution
            #print(operation,(type(operation) in ['str']))
            if (globals.invalidInput == True):
                if request.user.is_authenticated:
                    updatePlayingData(False , puzzle_level, request.user.username)
                globals.playdictionary['message'] = "please give correct inputs. Try again"
            else:
                # solved = checkSolution(userSolution)
                solved = globals.validMatrix(userSolution)
                if(solved):
                    minutes = globals.timeElapsed // 60
                    seconds = globals.timeElapsed % 60
                    globals.playdictionary['message'] = "congrats you Have solved this puzzle in time : {}m {}s".format(minutes, seconds)
                    puzzle_level.best_Time = globals.calculateBestTime(puzzle_level.best_Time, globals.timeElapsed)
                    puzzle_level.attempts +=1
                    puzzle_level.avg_Time = globals.calculateAverageTime(puzzle_level.avg_Time, globals.timeElapsed, puzzle_level.attempts)
                    puzzle_level.save()
                else:
                    globals.playdictionary['message'] = "Your Solution is Incorrect!!! Try Again."

                if request.user.is_authenticated:
                    updatePlayingData(solved , puzzle_level, request.user.username)
            return renderPlay(request, globals.playdictionary)
    else:
        globals.playdictionary["level_id"] = level_id
        changePuzzle(puzzle_level)
        globals.startTime = time.time()
        globals.minutes = 0         #only when user restarts the game then only globals minuters and seconds will be initialized by 0(zero)
        globals.seconds = 0         #when timer stops or game ends then we can't put minutes and seconds zero because we want to display 
        globals.playdictionary['starttime'] = globals.startTime
        return renderPlay(request, globals.playdictionary)      #them constantly as hx trigger is sending request every seconds

def get_time(request):
    """TO display time every seconds 
    this method calculates time elapsed since game starts , and sends minutes and seconds in format to display
    Parameter : object | request 
    returns : render funcion | dictionary - contianing minutes & seconds 
    """
    if(globals.puzzleSubmit == False):
        globals.timeElapsed = int(time.time() - globals.startTime) 
        

    seconds = globals.timeElapsed%60
    minutes = globals.timeElapsed//60
    #minutes = minutes if(minutes >= 10) else '0'+str(minutes)
    #seconds = seconds if(seconds >= 10) else '0'+str(seconds)
    # print(globals.minutes, globals.seconds)
    # print(minutes, seconds)
    return render(request,'puzzles/get_time.html', {'minutes' : minutes, 'seconds': seconds , 'starttime': globals.startTime , 'elapsed_time' : time.time() } )

