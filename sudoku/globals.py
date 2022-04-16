import time

import sudoku
arr = [[0 for x in range(0,9)] for y in range(0,9)]
sudokuPuzzle = [[0 for x in range(0,9)] for y in range(0,9)]
playdictionary = {}
startTime = 0
totalTime = 0
puzzleSubmit = False
timeElapsed = 0

invalidInput = False


def validMatrix(arr):
  """TO validate matrix"puzzle whether it is valid sudoku puzzle or not
  Parameter : 2d list : arr
  retunrs : boolean : True if valid else false 
  """
  numbers = range(1,10)
  for i in range(0,9):
    for j in range(0,9):
      num = arr[i][j]
      if( num in numbers ):
        if( NumberIsValidInRowCol(arr, i, j , num) and NumberIsValidInGrid(arr, i - i%3, j-j%3, i, j , num) ):
          continue
        else:
          return False
  return True
def NumberIsValidInGrid(arr,startRow, startColumn,rowindex,colindex, num):
  """checks whether given number already exists in grid or not
  if it already exists then it returns false
  Parameters : 
    2d list : arr , int: startRow , int : startColumn , int : rowindex(grid row index in which cell is) ,int : colindex(grid col index in which cell is),
    int : num which we have to check for 
  Returns : True or False
  """
  for i in range(startRow, startRow + 3 ):
      for j in range(startColumn, startColumn + 3):
          if(not (i== rowindex and j == colindex) ):
              if(num == arr[i][j]):
                  return False
  return True


def NumberIsValidInRowCol(arr,row, col, num):
    """checks whether given number already exists in same row or same column
    if it already exists then it returns false that number is not valid to place there or puzzle is invalid
    Parameters : 
      2d list : arr , int: row , int : col , int : num which we have to check for 
    Returns : True or False
    """
    for i in range(0,9):
        if(not i== col ):
            if(num == arr[row][i]):
                return False
    for i in range(0,9):
        if(not i== row ):
            if(num == arr[i][col]):
                return False
    return True

def calculateBestTime(previous_bestTime , current_time):
  """ reusable method to calculate best time between 2 times
    parameter : 
        int | previous_bestTime( in seconds),
        int |  current_time (in seconds)
    Returns : int | small time between the two"""
  if( previous_bestTime > current_time or previous_bestTime == 0) :
    return current_time
  else:
    return previous_bestTime

def calculateAverageTime(avg_Time,time_elapsed, attempts):
  """ reusable method to calculate average time
  parameter : 
      int | avg_Time( in seconds),
      int |  current_time (in seconds)
  Returns : int | average time of all times
  convert whole time in seconds then finds average of all then convert back into minutes and seconds format """
  total_previous_time = (attempts-1)*avg_Time
  total_time = total_previous_time + time_elapsed
  avg_time = total_time // attempts
  return avg_time
  
def calculateWorstTime(previous_worstTime , current_time):
  """ reusable method to calculate worst time between 2 times
  parameter : 
      int | previous_worstTime( in seconds),
      int |  current_time (in seconds)
  Returns : int | more time between the two"""
  print("in worst time")
  if( previous_worstTime < current_time ) :
    print("in worst time , returning time")
    return current_time
  else:
    print("returning same time")
    return previous_worstTime