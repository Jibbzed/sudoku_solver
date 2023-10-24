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

easy = "860004000000900800304000067620045791539081406007029000003006000050400089000507602"
puzzle = "100685070060010000590004060007060000010000007600090254000073091000050006800000300"

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
            row.append([int(numbers[i*9+j])])
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
                    if k!=j and grid[i][j][0] in grid[i][k]:
                        grid[i][k].remove(grid[i][j][0])
                        removed += 1
                #Remove from column
                for k in range(len(grid)):
                    if k!=i and grid[i][j][0] in grid[k][j]:
                        grid[k][j].remove(grid[i][j][0])
                        removed += 1
                #Remove from box
                box_i = i//3
                box_j = j//3
                for k in range(box_i*3,box_i*3+3):
                    for l in range(box_j*3,box_j*3+3):
                        if k!=i or l!=j:
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
                                for m in range(len(grid[i][j])):
                                    if grid[i][j][m] in grid[i][l]:
                                        grid[i][l].remove(grid[i][j][m])
                                        removed += 1
                        break
                #Check column
                for k in range(len(grid)):
                    if k!=i and grid[i][j] == grid[k][j]: #We can just use equality because the lists are sorted
                        #If we find such a cell, then we can remove these two candidates from all other cells in the column
                        for l in range(len(grid)):
                            if l!=i and l!=k:
                                for m in range(len(grid[i][j])):
                                    if grid[i][j][m] in grid[l][j]:
                                        grid[l][j].remove(grid[i][j][m])
                                        removed += 1
                        break
                #Check box
                box_i = i//3
                box_j = j//3
                for k in range(box_i*3,box_i*3+3):
                    for l in range(box_j*3,box_j*3+3):
                        if (k!=i or l!=j) and grid[i][j] == grid[k][l]: #We can just use equality because the lists are sorted
                            #If we find such a cell, then we can remove these two candidates from all other cells in the box
                            for m in range(box_i*3,box_i*3+3):
                                for n in range(box_j*3,box_j*3+3):
                                    #Condition is : we don't want either (i,j) or (k,l) cells => can be written as : (m!=i or n!=j) and (m!=k or n!=l) but less readable
                                    if not((m==i and n==j) or (m==k and n==l)):
                                        for o in range(len(grid[i][j])):
                                            if grid[i][j][o] in grid[m][n]:
                                                grid[m][n].remove(grid[i][j][o])
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
                        break
                    #Reset the boolean value
                    found = False
                    #Check column
                    for l in range(len(grid)):
                        if i!=l and grid[i][j][k] in grid[l][j]:
                            found = True
                            break
                    #If the number is alone in the column then we can solve the cell and look at other cells
                    if found == False:
                        removed += len(grid[i][j]) - 1
                        grid[i][j] = [grid[i][j][k]]
                        break
                    #Reset the boolean value
                    found = False
                    #Check box
                    box_i = i//3
                    box_j = j//3
                    for l in range(box_i*3,box_i*3+3):
                        for m in range(box_j*3,box_j*3+3):
                            if (l!=i or m!=j) and grid[i][j][k] in grid[l][m]:
                                found = True
                                break
                    #If the number is alone in the box then we can solve the cell and look at other cells
                    if found == False:
                        removed += len(grid[i][j]) - 1
                        grid[i][j] = [grid[i][j][k]]
                        break
    return (grid, removed)

#1.2. Hidden pairs
#If two cells in a row, column or box contain the same two candidates, then we can remove all other candidates from these two cells
#Checking the length of the intersection is not enough because we can have a case where two cells have 3 candidates in common
#but only 2 of them are "unique" on the row, column or box, so we have to "choose" the two right candidates and remove the others
#There can be conflicts with hidden triples if the implementation is not careful : typically if we have 3 cells that contain a hidden triple, we can
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
from itertools import combinations
def hidden_pairs(grid):
    removed = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            #If the cell is not solved yet then we check the row, col and box for hidden pairs
            if len(grid[i][j]) > 1:
                #Check row
                for k in range(len(grid[0])):
                    if j!=k:
                        #Here we make use of the intersection method of sets
                        inter = set(grid[i][j]).intersection(set(grid[i][k]))
                        if len(inter) == 2:
                            #If the intersection is of length 2 then we might have a hidden pair, but we have to check that it is not part of a hidden triple
                            #or quad, so we have to check the intersection of this pair with all other unsolved cells
                            pair = True
                            for l in range(len(grid[0])):
                                #We might be able to just check unsolved cells, but if we apply the different methods one after the other, then we might have
                                #a case where a cell has been solved but the method didn't clear the digit from the other cells, so we have to check all cells just in case
                                if l!=j and l!=k: 
                                    if len(inter.intersection(set(grid[i][l]))) != 0:
                                        #If the intersection is not empty then we don't have a hidden pair
                                        pair = False
                                        break
                            #If we have a hidden pair then we can remove all other candidates from the two cells
                            if pair == True:
                                rm_1 = len(grid[i][j]) - 2
                                rm_2 = len(grid[i][k]) - 2
                                removed += rm_1 + rm_2
                                grid[i][j] = list(inter)
                                grid[i][k] = list(inter)
                        elif len(inter) > 2:
                            #If the intersection is of length > 2 then we have to check all the possible pairs in the intesection against the other unsolved
                            #cells and if we find a pair that yield an empty intersection then we have found a hidden pair
                            #We will use itertools.combinations to get all the possible pairs
                            #combinations() returns an iterator but we have to convert it to a list to be able to remove elements from it
                            combi = [elem for elem in combinations(inter,2)]
                            #We are forced to use a copy of the list because we will remove elements from it while iterating over it
                            final_combi = combi.copy() 
                            for l in combi:
                                for m in range(len(grid[0])):
                                    #We might be able to just check unsolved cells, but if we apply the different methods one after the other, then we might have
                                    #a case where a cell has been solved but the method didn't clear the digit from the other cells, so we have to check all cells just in case
                                    if m!=j and m!=k:
                                        if len(set(l).intersection(set(grid[i][m]))) != 0:
                                            #If the intersection is not empty then we don't have a hidden pair and we can remove it from the list of pairs
                                            final_combi.remove(l)
                                            break
                            #Finally, if there is only one pair left then we have a hidden pair and we can remove all other candidates from the two cells
                            if len(final_combi) == 1:
                                rm_1 = len(grid[i][j]) - 2
                                rm_2 = len(grid[i][k]) - 2
                                removed += rm_1 + rm_2
                                grid[i][j] = list(final_combi[0])
                                grid[i][k] = list(final_combi[0])
                #Check column
                for k in range(len(grid)):
                    if i!=k:
                        #Here we make use of the intersection method of sets
                        inter = set(grid[i][j]).intersection(set(grid[k][j]))
                        if len(inter) == 2:
                            #If the intersection is of length 2 then we have a hidden pair, but we have to check that it is not part of a hidden triple
                            #or quad, so we have to check the intersection of this pair with all other unsolved cells
                            pair = True
                            for l in range(len(grid)):
                                #We might be able to just check unsolved cells, but if we apply the different methods one after the other, then we might have
                                #a case where a cell has been solved but the method didn't clear the digit from the other cells, so we have to check all cells just in case
                                if l!=i and l!=k:
                                    if len(inter.intersection(set(grid[l][j]))) != 0:
                                        #If the intersection is not empty then we don't have a hidden pair
                                        pair = False
                                        break
                            #If we have a hidden pair then we can remove all other candidates from the two cells
                            if pair == True:
                                rm_1 = len(grid[i][j]) - 2
                                rm_2 = len(grid[k][j]) - 2
                                removed += rm_1 + rm_2
                                grid[i][j] = list(inter)
                                grid[k][j] = list(inter)
                        elif len(inter) > 2:
                            #If the intersection is of length > 2 then we have to check all the possible pairs in the intesection against the other unsolved
                            #cells and if we find a pair that yield an empty intersection then we have found a hidden pair
                            #We will use itertools.combinations to get all the possible pairs
                            #combinations() returns an iterator but we have to convert it to a list to be able to remove elements from it
                            combi = [elem for elem in combinations(inter,2)]
                            #We are forced to use a copy of the list because we will remove elements from it while iterating over it
                            final_combi = combi.copy() 
                            for l in combi:
                                for m in range(len(grid)):
                                    #We might be able to just check unsolved cells, but if we apply the different methods one after the other, then we might have
                                    #a case where a cell has been solved but the method didn't clear the digit from the other cells, so we have to check all cells
                                    if m!=i and m!=k:
                                        if len(set(l).intersection(set(grid[m][j]))) != 0:
                                            #If the intersection is not empty then we don't have a hidden pair and we can remove it from the list of pairs
                                            final_combi.remove(l)
                                            break
                            #Finally, if there is only one pair left then we have a hidden pair and we can remove all other candidates from the two cells
                            if len(final_combi) == 1:
                                rm_1 = len(grid[i][j]) - 2
                                rm_2 = len(grid[k][j]) - 2
                                removed += rm_1 + rm_2
                                grid[i][j] = list(final_combi[0])
                                grid[k][j] = list(final_combi[0])
                #Check box
                box_i = i//3
                box_j = j//3
                for k in range(box_i*3,box_i*3+3):
                        for l in range(box_j*3,box_j*3+3):
                            if k!=i or l!=j:
                                #Here we make use of the intersection method of sets
                                inter = set(grid[i][j]).intersection(set(grid[k][l]))
                                if len(inter) == 2:
                                    #If the intersection is of length 2 then we have a hidden pair, but we have to check that it is not part of a hidden triple
                                    #or quad, so we have to check the intersection of this pair with all other unsolved cells
                                    pair = True
                                    for m in range(box_i*3,box_i*3+3):
                                        for n in range(box_j*3,box_j*3+3):
                                            #We might be able to just check unsolved cells, but if we apply the different methods one after the other, then we might have
                                            #a case where a cell has been solved but the method didn't clear the digit from the other cells, so we have to check all cells just in case
                                            if not((m==i and n==j) or (m==k and n==l)):
                                                if len(inter.intersection(set(grid[m][n]))) != 0:
                                                    #If the intersection is not empty then we don't have a hidden pair
                                                    pair = False
                                                    break
                                        if pair == False:
                                            break
                                    #If we have a hidden pair then we can remove all other candidates from the two cells
                                    if pair == True:
                                        rm_1 = len(grid[i][j]) - 2
                                        rm_2 = len(grid[k][l]) - 2
                                        removed += rm_1 + rm_2
                                        grid[i][j] = list(inter)
                                        grid[k][l] = list(inter)
                                elif len(inter) > 2:
                                    #If the intersection is of length > 2 then we have to check all the possible pairs in the intesection against the other unsolved
                                    #cells and if we find a pair that yield an empty intersection then we have found a hidden pair
                                    #We will use itertools.combinations to get all the possible pairs
                                    #combinations() returns an iterator but we have to convert it to a list to be able to remove elements from it
                                    combi = [elem for elem in combinations(inter,2)]
                                    #We are forced to use a copy of the list because we will remove elements from it while iterating over it
                                    final_combi = combi.copy() 
                                    for o in combi:
                                        #We have to use a flag variable to break out of the two loops
                                        flag = False
                                        for m in range(box_i*3,box_i*3+3):
                                            for n in range(box_j*3,box_j*3+3):
                                                #We might be able to just check unsolved cells, but if we apply the different methods one after the other, then we might have
                                                #a case where a cell has been solved but the method didn't clear the digit from the other cells, so we have to check all cells just in case
                                                if not((m==i and n==j) or (m==k and n==l)):
                                                    if len(set(o).intersection(set(grid[m][n]))) != 0:
                                                        #If the intersection is not empty then we don't have a hidden pair and we can remove it from the list of pairs
                                                        final_combi.remove(o)
                                                        flag = True
                                                        break
                                            if flag == True:
                                                break
                                    #Finally, if there is only one pair left then we have a hidden pair and we can remove all other candidates from the two cells
                                    if len(final_combi) == 1:
                                        rm_1 = len(grid[i][j]) - 2
                                        rm_2 = len(grid[k][l]) - 2
                                        removed += rm_1 + rm_2
                                        grid[i][j] = list(final_combi[0])
                                        grid[k][l] = list(final_combi[0])
    return (grid, removed)

#===============================================================================================================================================

#3. and 4. : Intersection removal
#The next two methods are part of a technique called intersection removal
#The idea is that if any one number occurs twice or thrice in just one unit (any row, column or box) then we can remove that number from the intersection of another unit
#There are four types of intersection :
#A Pair or Triple in a box - if they are aligned on a row, n can be removed from the rest of the row
#A Pair or Triple in a box - if they are aligned on a column, n can be removed from the rest of the column
#A Pair or Triple on a row - if they are all in the same box, n can be removed from the rest of the box
#A Pair or Triple on a column - if they are all in the same box, n can be removed from the rest of the box

#===============================================================================================================================================

#3. Pointing pairs
#The idea is the following : we look at each box and if there a number appears twice or thrice in the box, on the same row or column, then we know that
#this number MUST appear on that row or column, so we can remove it from the rest of the row or column on which it appears
def pointing_pairs(grid):
    print()

#===============================================================================================================================================

#4. Box/line reduction
#The idea is the exact same than with pointing pairs, but we look at rows and columns instead of boxes and remove from boxes instead of rows and columns
def box_line_reduction(grid):
    print()

#===============================================================================================================================================

#Define a solve function that will apply the different methods until the puzzle is solved or no more candidates can be removed
def solve(grid):
    left = 81
    removed = 1
    steps = 0
    while(left!=0 and removed!=0):
        removed = 0
        grid, rm = simple_elimination(grid)
        removed += rm
        grid, rm = naked_pairs(grid)
        removed += rm
        grid, rm = hidden_singles(grid)
        removed += rm
        grid, rm = hidden_pairs(grid)
        removed += rm
        left = cells_left(grid)
        steps += 1
    if left == 0:
        print("Solved in " + str(steps) + " steps")
        print_grid(grid)
    else:
        print("Could not solve the puzzle with these methods")
        print("Cells left : " + str(cells_left(grid)))
        print("Final grid :")
        print_grid(grid)

#===============================================================================================================================================

#Test the functions
to_solve = puzzle
grid = grid_from_string(to_solve)
grid = fill_candidates(grid)
print()
print_grid(grid)
print()
solve(grid)