"""
Title: N-Queens Problem
Nicolas Child
Analysis of Algorithms - CS3310

            .     .     .
              X   X   X
                X X X
Queen Path: . X X Q X X .     ('.' implies it's continuous)
                X X X
              X   X   X
            .     .     .

Input: A l*w sized chessboard such that l = w, represented as d (for dimmensions)
Output: A list of matricies representing a chessboard
"""

from copy import deepcopy

"""N QUEENS SOLUTIONS"""

def aSolutionToNQueens(d: int) -> list[list]:
    """Takes in dimmensions of board (d*d)"""
    if d < 3:
        return "Board dimmensions too small, d < 3"

    chessBoard = [['-'] * d for _ in range(d)] #2D array of d*d
    columns = set()
    rows = set() #Marks columns which are not possible to place
    negativeDiagnal = set() #Holds (r-c) going in y=x direction
    positiveDiagnal = set() #Holds (r+c) going in y=-x direction
    # Example of negative and positive diagnals
    """
    Negative Diagnal (r-c)
       0   1   2   3
    0 [0, -1, -2, -3] Each diagnal path has a set value of r-c
    1 [1,  0, -1, -2] in the negative direction
    2 [2,  1,  0, -1]
    3 [3,  2,  1,  0]
    
    Positive Diagnal (r+c)
       0  1  2  3
    0 [0, 1, 2, 3] Each diagnal path has a set value of r+c
    1 [1, 2, 3, 4] in the positive direction
    2 [2, 3, 4, 5]
    3 [3, 4, 5, 6]
    """
    # Start placing Queens
    for r in range(d): # Rows
        for c in range(d): # Columns
            currNegDiagnal = r-c
            currPosDiagmnal = r+c
            currRow = r
            currColumn = c
            if currNegDiagnal not in negativeDiagnal and currPosDiagmnal not in positiveDiagnal\
                and currRow not in rows and currColumn not in columns:
                negativeDiagnal.add(currNegDiagnal)
                positiveDiagnal.add(currPosDiagmnal)
                columns.add(currColumn)
                rows.add(currRow)
                chessBoard[r][c] = 'Q'
    return chessBoard


def nQueens(d: int) -> list[list[list]]:
    """Calculates all possible n-Queens combinations for a board of d*d"""
    # Same idea as the single solution, except when we find a placement
    # for a queen we will backtrack that step, and continue with the next row or column
    chessBoard = [['-'] * d for _ in range(d)] #2D array of d*d
    allChessBoards = [] #Where we are going to store our chessBoards
    columns = set()
    negD = set()
    posD = set()
    nQueensHelper(columns, negD, posD, d, 0, chessBoard, allChessBoards)
    return allChessBoards
    

def nQueensHelper(columns, negD, posD, d, r, chessBoard, allChessBoards):
    # We will go through the rows recursively
    # Base case is that we have gone through each row
    if r == d:
        allChessBoards.append(deepcopy(chessBoard))
        return
    for c in range(d):
        curPosD = r + c
        curNegD = r - c
        if c not in columns and curPosD not in posD and curNegD not in negD:
            negD.add(curNegD)
            posD.add(curPosD)
            columns.add(c)
            chessBoard[r][c] = 'Q'
            nQueensHelper(columns, negD, posD, d, r+1, chessBoard, allChessBoards)
            #BACKTRACK
            negD.remove(curNegD)
            posD.remove(curPosD)
            columns.remove(c)
            #Reset board position
            chessBoard[r][c] = '-'

def printChessBoard(board):
    """Handy function to print the chessboard in a readable manner"""
    for x in board: print(x)
    print()

"""TEST SUITE"""
singleSolution = aSolutionToNQueens(5)
allSolutions = nQueens(5)

def test_CompareFunctions():
    """Testing to see if our single solution is in all solutions"""
    assert allSolutions[0] == singleSolution

def test_numberOfSolutions():
    """http://oeis.org/A000170 Testing the official OEIS count for n*n queens backtracking count"""
    assert len(nQueens(3)) == 0
    assert len(nQueens(4)) == 2
    assert len(nQueens(5)) == 10
    assert len(nQueens(6)) == 4
    assert len(nQueens(7)) == 40 
    assert len(nQueens(8)) == 92 
    assert len(nQueens(9)) == 352

def test_queenCollisions():
    """Checks off rows and columns and other collision paths to ensure that there are no duplicates in array"""
    collisionPaths = [] #going to mark each r-c, r+c in a dictionary and keep track of its count
    for row in range(len(singleSolution)):
        for column in range(len(singleSolution)):
            if singleSolution[row][column] == 'Q':
                collisionPaths.append(f"Row: {row}") # Row
                collisionPaths.append(f"Column {column}") # Column
                collisionPaths.append(f"Negative Diagonal: {row-column}")
                collisionPaths.append(f"Positive Diagonal: {row+column}")
    # Now check for duplicates
    collisionPaths.sort()
    # UNIQUE List, just convert it to a set, it will eliminate all duplicates, then turn back to a list for comparison
    uniquePaths = list(set(collisionPaths))
    collisionPaths.sort(), uniquePaths.sort()
    assert collisionPaths == uniquePaths

def test_dimmensionsOfGrids():
    """Checks the grid dimmensions to ensure that they are n*n, like a chessboard"""
    # Single Solution
    assert len(singleSolution) == 5 # Rows
    assert len(singleSolution[0]) == 5 # Columns
    # All Solutions
    assert len(allSolutions[0]) == 5 # Rows
    assert len(allSolutions[0][0]) == 5 # Columns
    