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
#The idea is to look at remaining possible candidates in the cells : if there are n cells that contain the same n candidates, then we can remove them from other cells
#There can be naked singles, pairs, triples and quads, but we will only implement the first two

#1.1. Naked singles
#Naked singles are cells that contain only one candidate => same as simple elimination

#1.2. Naked pairs
def naked_pairs(grid):
    removed = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            #If we find a cell with two candidates, we look for another cell with the same two candidates
            if len(grid[i][j]) == 2:
                #Check row
                for k in range(len(grid[0])):
                    if k!=j and grid[i][j] == grid[i][k]: #We can just use equality because the lists are sorted
                        #If we find such a cell, then we can remove these two candidates from all other cells in the row
                        for l in range(len(grid[0])):
                            if l!=j and l!=k:
                                for m in range(len(grid[i][l])):
                                    if grid[i][l][m] in grid[i][j]:
                                        grid[i][l].remove(grid[i][l][m])
                                        removed += 1
                        break
                #Check column
                for k in range(len(grid)):
                    if k!=j and grid[i][j] == grid[k][j]: #We can just use equality because the lists are sorted
                        #If we find such a cell, then we can remove these two candidates from all other cells in the column
                        for l in range(len(grid)):
                            if l!=i and l!=k:
                                for m in range(len(grid[l][j])):
                                    if grid[l][j][m] in grid[i][j]:
                                        grid[l][j].remove(grid[l][j][m])
                                        removed += 1
                        break
                #Check box
                box_i = i//3
                box_j = j//3
                for k in range(box_i*3,box_i*3+3):
                    for l in range(box_j*3,box_j*3+3):
                        if k!=i and l!=j and grid[i][j] == grid[k][l]: #We can just use equality because the lists are sorted
                            #If we find such a cell, then we can remove these two candidates from all other cells in the box
                            for m in range(box_i*3,box_i*3+3):
                                for n in range(box_j*3,box_j*3+3):
                                    if m!=i and n!=j and m!=k and n!=l:
                                        for o in range(len(grid[m][n])):
                                            if grid[m][n][o] in grid[i][j]:
                                                grid[m][n].remove(grid[m][n][o])
                                                removed += 1
                            break
    return (grid, removed)

#===============================================================================================================================================

#2. Hidden candidates
#This methods ressembles the naked candidates, but can find broader relationships between cells
#The idea is to look at each row, column and box and look for n candidates that only appear in n cells (instead of looking for n cells that contain the same n candidates)
#If we find such a relationship, then we can remove all other candidates from these cells
#There exists hidden singles, pairs, triples and quads, but we will only implement the first two

#1.1. Hidden singles
#If a cell is the only one in its row, column or box to contain a certain candidate, then we can remove all the other candidates from this cell
def hidden_singles(grid):
    removed = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            #If the cell is not solved yet then we check the row, col and box
            if len(grid[i][j]) > 1:
                #For each candidate in the cell
                for k in range(len(grid[i][j])):
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

#1.2. Hidden pairs
#If two cells in a row, column or box contain the same two candidates, then we can remove all other candidates from these two cells
#Computationaly heavy because for each unsolved cell we have to check the "intersection" with all other unsolved cells in the row, column and box
#Harder than it looks : checking the length of the intersection is not enough because we can have a case where two cells have 3 candidates in common
#but only 2 of them are "unique" on the row, column or box, so we have to "choose" the two right candidates and remove the others
#There can be conflicts with hidden triples if the implemntation is not careful : typically if we have 3 cells that contain a hidden triple, we can
#wrongly identify a hidden pair in two of them => {2,5,6} {2,6} {2,5} is a hidden triple, but we can wrongly identify {2,5} {2,6} as a hidden pair
#and remove 5 or 6 from the {2,5,6} cell even though it is an error to do so !
#In order to avoid this we could look for hidden pairs, triples and quads and then choose from this, but we will only implement hidden pairs for now
#So what we have to do is : for each unsolved cell, check the intersection with all other unsolved cells, and then check the intersection of this pair
#with all other unsolved cells
#Example : we pick (1,1), we compute the intersection with (1,2) which is also unsolved, 1) if the intersection is of length 2, then we check the the
#intersection of (1,1) and (1,2) with all other unsolved cells, if it is empty then we have a hidden pair and we can remove the other candidates from
#(1,1) and (1,2) ; 2) if the intersection is of length > 2 then we have to check all the possible pairs in the intesection against the other unsolved
#cells and if we find a pair that yield an empty intersection then we have found a hidden pair
#The implementation will be very computationaly intensive, and I don't see a way to make it much more efficient, other than maybe using a different
#data structure to represent the grid, but I don't think it would make much of a difference
def hidden_pairs(grid):
    removed = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            #If the cell is not solved yet then we check the row, col and box for hidden pairs
            if len(grid[i][j]) > 1:
                


#===============================================================================================================================================