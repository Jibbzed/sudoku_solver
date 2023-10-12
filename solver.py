#Start by defining the board : two different difficulties just to test the solver
#0 means empty cell
easy = [[8,6,0,0,0,4,0,0,0],
        [0,0,0,9,0,0,8,0,0],
        [3,0,4,0,0,0,0,6,7],
        [6,2,0,0,4,5,7,9,1],
        [5,3,9,0,8,1,4,0,6],
        [0,0,7,0,2,9,0,0,0],
        [0,0,3,0,0,6,0,0,0],
        [0,5,0,4,0,0,0,8,9],
        [0,0,0,5,0,7,6,0,2]]

two_sols = [[9,0,6,0,7,0,4,0,3],
            [0,0,0,4,0,0,2,0,0],
            [0,7,0,0,2,3,0,1,0],
            [5,0,0,0,0,0,1,0,0],
            [0,4,0,2,0,8,0,6,0],
            [0,0,3,0,0,0,0,0,5],
            [0,3,0,7,0,0,0,5,0],
            [0,0,7,0,0,5,0,0,0],
            [4,0,5,0,1,0,7,0,8]]

medium = [[0,8,0,0,5,0,0,9,0],
          [0,0,0,6,0,0,2,0,3],
          [4,2,7,0,0,3,0,6,0],
          [0,0,8,1,6,2,0,0,0],
          [0,3,0,0,0,9,0,8,0],
          [0,0,0,5,0,0,0,0,0],
          [2,5,6,8,0,1,3,7,0],
          [0,4,0,0,0,0,1,0,0],
          [0,0,0,0,4,0,0,2,0]]

difficult = [[1,0,0,6,8,5,0,7,0],
             [0,6,0,0,1,0,0,0,0],
             [5,9,0,0,0,4,0,6,0],
             [0,0,7,0,6,0,0,0,0],
             [0,1,0,0,0,0,0,0,7],
             [6,0,0,0,9,0,2,5,4],
             [0,0,0,0,7,3,0,9,1],
             [0,0,0,0,5,0,0,0,6],
             [8,0,0,0,0,0,3,0,0]]

expert = [[5,8,6,4,0,0,0,0,3],
          [0,0,0,0,8,0,0,0,4],
          [0,0,0,9,0,0,0,0,7],
          [0,0,0,0,0,0,0,4,0],
          [0,0,0,0,0,9,7,2,0],
          [0,3,0,0,5,0,0,0,1],
          [7,0,0,0,0,0,0,6,0],
          [0,5,0,0,3,2,0,0,0],
          [2,0,0,0,6,0,0,0,0]]

diabolical = [[0,8,0,2,0,0,0,1,0],
              [0,6,0,0,0,3,0,0,0],
              [3,0,1,0,7,0,9,0,0],
              [4,0,2,0,0,8,0,9,0],
              [0,0,0,5,0,0,7,0,0],
              [0,1,0,0,0,0,0,0,0],
              [9,0,3,0,0,4,0,2,0],
              [0,0,0,0,8,0,0,0,4],
              [6,0,0,0,0,0,0,0,0]]

extreme = [[0,0,1,0,0,3,0,0,2],
           [0,2,0,0,4,0,0,1,0],
           [7,0,0,9,0,0,5,0,0],
           [4,0,0,8,0,0,6,0,0],
           [0,1,0,0,7,0,0,4,0],
           [0,0,3,0,0,4,0,0,8],
           [0,0,2,0,0,7,0,0,5],
           [0,9,0,0,5,0,0,6,0],
           [6,0,0,3,0,0,8,0,0]]

#Define helper functions
#Print the board in a nice way
def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("---------------------")
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print("| ", end = "")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end = "")

#Test if a number is valid in a given position
def isValid(i,j,n,board):
    #Check row
    for k in range(len(board[0])):
        if board[i][k] == n:
            return False
    #Check column
    for k in range(len(board)):
        if board[k][j] == n:
            return False
    #Check box
    box_i = i//3
    box_j = j//3
    for k in range(box_i*3,box_i*3+3):
        for l in range(box_j*3,box_j*3+3):
            if board[k][l] == n:
                return False
    return True

#Then define the actual solver
#For this we will use a simple backtracking algorithm
# => we try to fill each empty cell with a number and everytime we reach a dead end we backtrack
def solve(board):
    #First we have to find the next empty cell
    for i in range(len(board)):
        for j in range(len(board[0])):
            #If the cell is empty
            if board[i][j] == 0:
                #Then we try to fill it with a number
                for n in range(1,10):
                    #If the number is valid in this position
                    if(isValid(i,j,n,board)):
                        #Then we put it in the cell and recursively call the solve function
                        board[i][j] = n
                        solve(board)
                        #If the recursive call returns false then we have to backtrack
                        board[i][j] = 0
                return False
    #If all the cells are filled then a solution has been found and we can print it and return true
    print_board(board) 
    print("=====================")
    return True

#Finally we can call the solver on the board
to_solve = extreme
print_board(to_solve)
print("Solving board...")
solve(to_solve)