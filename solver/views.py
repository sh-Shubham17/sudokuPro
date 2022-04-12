
from tkinter import E
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from sudoku import globals
from puzzles.models import DificultyLevel, Puzzle

def get_all_levels():
  """ To fetch all existing level objects(rows) from database
    Parameter : None
    returns : list having level objects as item
  """
  levels = DificultyLevel.objects.all().order_by('number_of_empty_cells')
  return levels


def save_puzzle_in_database(request, solution):
  """TO save puzzle in database if there exists solution to a puzzle
    parameter : 
    request object , 
    2d list - solution

    returns : True or false whether data is saved or not in our database
  """
  try:
    name = request.POST.get("puzzle_name")
    level_name = request.POST.get("selected_level_id")
    print(level_name)
    levelObj = DificultyLevel.objects.get(name = level_name)
    Source = request.POST.get("source")
    if not name:
      name = level_name + "_" + name

    puzzleObj = Puzzle( title = name,
    qrow1 = solution[0],
    qrow2 = solution[1],
    qrow3 = solution[2],
    qrow4 = solution[3],
    qrow5 = solution[4],
    qrow6 = solution[5],
    qrow7 = solution[6],
    qrow8 = solution[7],
    qrow9 = solution[8],
    dificultyLevel = levelObj,
    source = Source
    )
    puzzleObj.save()
    return True
  except Exception as e:
    return False

def findingCell(row):
  """finds and reurns very empty next cell 
    parameter : current filled row 
    returns : list having row and col index for next empty cell in sudoku puzzle
  """
  cell = [-1,-1]
  for i in range(row, 9):
    for j in range(0, 9):
      if(globals.arr[i][j]==0):
        cell = [i,j]
        return cell
  return cell


def display():
  " used to display whole array in puzzle format is needed unless it is not useful in our project app "
  for i in range(0,9):
    for j in range(0,9):
      print(globals.arr[i][j],end=',')
    print()


def solvePuzzle():
  """This method solves the puzzle using backtracking( First search based approach) 
  parameter : None
  reuturns :   0 if puzzle has no solution, else 1
  """
  CellRow = 0
  CellCol = 0

  cell = findingCell(CellRow)
  #print("---------------------------------")
  #print("cell found",cell)
  if(cell[0] == -1):
    return 1
  else:
    # previousCellRow = globals.currentCellRow
    # previousCellCol = globals.currentCellCol
    CellRow = cell[0]
    CellCol = cell[1]
  flag = 0
  k = 1
  gridRow = CellRow - CellRow%3
  gridColumn = CellCol - CellCol%3
  while((not flag == 1) and k<=9 ):
    if ( globals.NumberIsValidInRowCol(globals.arr,CellRow, CellCol,k) and globals.NumberIsValidInGrid(globals.arr,gridRow, gridColumn,CellRow, CellCol, k)):
      globals.arr[CellRow][CellCol] = k
      #print("number set ",k)
      flag = solvePuzzle()
    k+=1
  if(flag == 0):
    #print('No number suit backtracking')
    globals.arr[CellRow][CellCol] = 0
    # globals.currentCellRow = previousCellRow
    # globals.currentCellCol = previousCellCol

  return flag


def readData(request):
  """ This method ise used to read and validate puzzle from user form input
    parameter : request object
    returns : dicionary
    dictionry attributes : message (string) , mysudoku (2d list)
   """
  numbersCheck = [str(x) for x in range(0,10)]
  nonNumeric = False
  for i in range(9):
    s = str(i+1)    #converting i+1 index to string so that
    for j in range(9):
      key_name = "row"+s+"col"+str(j+1)
      value = request.POST.get(key_name)
      if value == '':
        globals.arr[i][j] = 0
      elif value not in numbersCheck :
        nonNumeric = True
        globals.arr[i][j] = value
        #print('non numeric :- ', value)
      else:
        globals.arr[i][j] = int(value)
  if(nonNumeric):
    message = 'non numeric value'
  else:
    message = 'finding solution'
  return {'message':message, 'mysudoku': globals.arr}


def index(request):
  """This function is used to take input(puzzle, puzzle_level, puzzle_name, puzzle_source) from input and handle it
    parameter : request object
    returns : render method 
      render method is passed a dictionry to display data and solution if solution exists"""
  if not request.user.is_authenticated:
    return render(request, 'solver/Anonymous_user.html')
  else :
    globals.arr = [[0 for x in range(0,9)] for y in range(0,9)]
    #print(globals.arr)

    responseData = {'message': 'Type your problem in below grid', 'mysudoku': globals.arr, 'solveClicked': False, }
    if request.method == "POST":

      levels = get_all_levels()
      responseData['all_levels'] = levels
      responseData['current_level'] = levels[0]

      if request.POST.get("solve") == "True":
        responseData = readData(request)
        responseData['solveClicked'] = True
        if( responseData['message'] == 'non numeric value'):
          responseData["message"]= 'please enter only numbers between 0-9'
          return render(request, 'solver/index.html', responseData)
        else:
          if(not  globals.validMatrix(globals.arr)):
            responseData['message'] = 'Invalid Puzzle !!! No solution Found '
            return render(request, 'solver/index.html', responseData) 
          else:
            solved = 0
            #print("before going to solve",solved)
            solved = solvePuzzle()
            #print("after",solved)
            if(solved == 1):
              responseData['message'] = "here is your solution"
              responseData['mysudoku'] = globals.arr
              # request.POST.get("save_data") returns "on" and None 2 values
              if request.POST.get("save_data"):
                print('working')
                added = save_puzzle_in_database(request, globals.arr)
                if added:
                  responseData['message'] += "&, data saved in the database :)"
            else:
              responseData['message'] = "No solution found!!!\nSorry looks like there is some error in your puzzle.:`("
            return render(request, 'solver/index.html', responseData)
    else: 
      levels = get_all_levels()
      responseData['all_levels'] = levels
      responseData['current_level'] = levels[0]
    return render(request, 'solver/index.html', responseData)
