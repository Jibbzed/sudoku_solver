#The idea is to implement several solving methods for a sudoku puzzle that can be performed by a human
#The methods are:
#0. Simple elimination
#1. Naked candidates
#2. Hidden candidates
#3. Pointing pairs
#4. Box/line reduction
#5. X-wing
#The methods will be applied in order until either no new digits can be found (in which case these techniques are not enough) or
#the puzzle is completed

easy = "8,6,0,0,0,4,0,0,0,0,0,0,9,0,0,8,0,0,3,0,4,0,0,0,0,6,7,6,2,0,0,4,5,7,9,1,5,3,9,0,8,1,4,0,6,0,0,7,0,2,9,0,0,0,0,0,3,0,0,6,0,0,0,0,5,0,4,0,0,0,8,9,0,0,0,5,0,7,6,0,2"
puzzle = "1,0,0,6,8,5,0,7,0,0,6,0,0,1,0,0,0,0,5,9,0,0,0,4,0,6,0,0,0,7,0,6,0,0,0,0,0,1,0,0,0,0,0,0,7,6,0,0,0,9,0,2,5,4,0,0,0,0,7,3,0,9,1,0,0,0,0,5,0,0,0,6,8,0,0,0,0,0,3,0,0"

#Here is how the puzzle will be represented and solved :
#Each cell will be represented by a list of possible digits => in the begining given digits are alone, and empty cells contain all the digits
#Each iteration will aim to reduce the number of digits in the cells, until only one digit is left in each cell
#The grid is a list of lists of lists, with the first list representing the rows, the second the columns and the third the possible digits

#===============================================================================================================================================

#We will first need to define some helper functions to make our life easier
#Transform the puzzle from a list of numbers, with 0s to represent empty cells, to a "grid" 
def grid_from_string(numbers):
    grid = []
    for i in range(9):
        row = []
        for j in range(9):
            row.append([numbers[i*9+j]])
        grid.append(row)
    return grid

#Add possible candidates to a cell instead of zeros
def fill_candidates(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j][0] == 0:
                grid[i][j] = [i for i in range(1,10)]
    return grid

#Print the grid in a nice way
def print_grid(grid):
    for i in range(len(grid)):
        if i % 3 == 0 and i != 0:
            print("---------------------")
        for j in range(len(grid[0])):
            if j % 3 == 0 and j != 0:
                print("| ", end = "")
            if len(grid[i][j]) == 1:
                print(str(grid[i][j][0]) + " ", end = "")
            else:
                print(". ", end = "")
        print()

#Number of cells already solved
def cells_solved(grid):
    solved = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if len(grid[i][j]) == 1:
                solved += 1
    return solved

#Number of cells left to solve
def cells_left(grid):
    return 81 - cells_solved(grid)

#Number of candidates to remove to solve the puzzle
def candidates_left(grid):
    candidates = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            #In each cell there are x digits and 1 is correct so we have to eliminate x-1 candidates
            candidates += len(grid[i][j]) - 1 
    return candidates

#===============================================================================================================================================

#Then we can define the different solving methods
#To be able to track the number of candidates removed by each method, we will return a tuple with the grid and the number of candidates removed
#This will also be helpful to know when to stop trying to solve the puzzle

#===============================================================================================================================================

#0. Simple elimination
#The idea of this method is to look at each row, column and box and eliminate the digits that are already present
def simple_elimination(grid):
    removed = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            #If the cell is solved, then we remove the number it contains from the corresponding row, column and box
            if len(grid[i][j]) == 1:
                #Remove from row
                for k in range(len(grid[0])):
                    if grid[i][j][0] in grid[k][j]:
                        grid[i][k].remove(grid[i][j][0])
                        removed += 1
                #Remove from column
                for k in range(len(grid)):
                    if grid[i][j][0] in grid[k][j]:
                        grid[k][j].remove(grid[i][j][0])
                        removed += 1
                #Remove from box
                box_i = i//3
                box_j = j//3
                for k in range(box_i*3,box_i*3+3):
                    for l in range(box_j*3,box_j*3+3):
                        if k!=i and l!=j:
                            if grid[i][j][0] in grid[k][l]:
                                grid[k][l].remove(grid[i][j][0])
                                removed += 1
    return (grid,removed)

#===============================================================================================================================================

#1. Naked candidates
#The idea of this method is to look at each row, column and box and see if there are n cells that contain the same n candidates
#There can be naked singles, pairs, triples and quads, but we will only implement the first two

#1.1. Naked singles
#If a cell is the only one in its row, column or box to contain a certain candidate, then we can remove all the other candidates from this cell
def naked_singles(grid):
    removed = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            #If the cell is not solved yet then we check the row, col and box
            if len(grid[i][j]) > 1:
                #For each candidate in the cell
                for k in range(len(grid[i][j])):
                    #Check column
                    found = False
                    for l in range(len(grid)):
                        if i!=l and grid[i][j][k] in grid[l][j]:
                            found = True
                            break
                    #If the number is alone in the column then we can solve the cell and look at other cells
                    if found == False:
                        removed += len(grid[i][j]) - 1
                        grid[i][j] = [grid[i][j][k]]
                        continue
                    #Reset the boolean value
                    found = False
                    #Check row
                    for l in range(len(grid[0])):
                        if j!=l and grid[i][j][k] in grid[i][l]:
                            found = True
                            break
                    #If the number is alone in the row then we can solve the cell and look at other cells
                    if found == False:
                        removed += len(grid[i][j]) - 1
                        grid[i][j] = [grid[i][j][k]]
                        continue
                    #Reset the boolean value
                    found = False
                    #Check box
                    box_i = i//3
                    box_j = j//3
                    for l in range(box_i*3,box_i*3+3):
                        for m in range(box_j*3,box_j*3+3):
                            if l!=i and m!=j and grid[i][j][k] in grid[l][m]:
                                found = True
                                break
                    #If the number is alone in the box then we can solve the cell and look at other cells
                    if found == False:
                        removed += len(grid[i][j]) - 1
                        grid[i][j] = [grid[i][j][k]]
                        continue
    return (grid, removed)

#===============================================================================================================================================