import unittest
from human_solve import x_wing

class TestXWing(unittest.TestCase):
    
    #We have to define 2 tests, one for the check on the rows and one for the checks on the columns
    def test_grid_rows(self):
        #Define the grid before and after the xwing elimination
        #Example taken from https://www.sudokuwiki.org/X_Wing_Strategy
        grid_before = [[[1],[3, 7, 8],[3, 7],[2, 3, 4, 7, 8],[2, 7, 8],[2, 3, 4, 7, 8],[5],[6],[9]],
                       [[4],[9],[2],[3, 7],[5],[6],[1],[3, 7],[8]],
                       [[3, 7, 8],[5],[6],[1],[7, 8],[9],[2],[4],[3, 7]],
                       [[3, 5, 7],[3, 7],[9],[6],[4],[2, 7],[8],[2, 5],[1]],
                       [[5, 7],[6],[4],[2, 7, 8, 9],[1],[2, 7, 8],[3, 7, 9],[2, 5],[3, 7]],
                       [[2],[1],[8],[7, 9],[3],[5],[6],[7, 9],[4]],
                       [[3, 7, 8],[4],[3, 7],[5],[2, 7, 8, 9],[2, 3, 7, 8],[3, 7, 9],[1],[6]],
                       [[9],[3, 7, 8],[5],[3, 7, 8],[6],[1],[4],[3, 7, 8],[2]],
                       [[6],[2],[1],[3, 4, 7, 8],[7, 8, 9],[3, 4, 7, 8],[3, 7, 9],[3, 7, 8, 9],[5]]]
        grid_after = [[[1],[3, 7, 8],[3, 7],[2, 3, 4, 8],[2, 7, 8],[2, 3, 4, 7, 8],[5],[6],[9]],
                       [[4],[9],[2],[3, 7],[5],[6],[1],[3, 7],[8]],
                       [[3, 7, 8],[5],[6],[1],[7, 8],[9],[2],[4],[3, 7]],
                       [[3, 5, 7],[3, 7],[9],[6],[4],[2, 7],[8],[2, 5],[1]],
                       [[5, 7],[6],[4],[2, 8, 9],[1],[2, 7, 8],[3, 7, 9],[2, 5],[3, 7]],
                       [[2],[1],[8],[7, 9],[3],[5],[6],[7, 9],[4]],
                       [[3, 7, 8],[4],[3, 7],[5],[2, 7, 8, 9],[2, 3, 7, 8],[3, 7, 9],[1],[6]],
                       [[9],[3, 7, 8],[5],[3, 8],[6],[1],[4],[3, 8],[2]],
                       [[6],[2],[1],[3, 4, 8],[7, 8, 9],[3, 4, 7, 8],[3, 7, 9],[3, 8, 9],[5]]]

        #Run the xwing elimination
        grid, _ = x_wing(grid_before)

        #Check that the grid is as expected
        self.assertEqual(grid, grid_after)
        
    
    def test_removed_candidates_rows(self):
        #Define the grid before and the number of expected removed candidates
        grid_before = [[[1],[3, 7, 8],[3, 7],[2, 3, 4, 7, 8],[2, 7, 8],[2, 3, 4, 7, 8],[5],[6],[9]],
                       [[4],[9],[2],[3, 7],[5],[6],[1],[3, 7],[8]],
                       [[3, 7, 8],[5],[6],[1],[7, 8],[9],[2],[4],[3, 7]],
                       [[3, 5, 7],[3, 7],[9],[6],[4],[2, 7],[8],[2, 5],[1]],
                       [[5, 7],[6],[4],[2, 7, 8, 9],[1],[2, 7, 8],[3, 7, 9],[2, 5],[3, 7]],
                       [[2],[1],[8],[7, 9],[3],[5],[6],[7, 9],[4]],
                       [[3, 7, 8],[4],[3, 7],[5],[2, 7, 8, 9],[2, 3, 7, 8],[3, 7, 9],[1],[6]],
                       [[9],[3, 7, 8],[5],[3, 7, 8],[6],[1],[4],[3, 7, 8],[2]],
                       [[6],[2],[1],[3, 4, 7, 8],[7, 8, 9],[3, 4, 7, 8],[3, 7, 9],[3, 7, 8, 9],[5]]]
        expected_rm = 6

        #Run the xwing elimination
        _, removed = x_wing(grid_before)

        #Check that the number of removed candidates is as expected
        self.assertEqual(removed, expected_rm)
    
    def test_grid_cols(self):
        #Define the grid before and after the xwing elimination
        #Example taken from https://www.sudokuwiki.org/X_Wing_Strategy
        grid_before = [[[1, 3, 5, 8],[2, 3, 5],[1, 2, 3, 5, 8],[3, 5, 6, 8],[6, 7, 8],[3, 5, 6, 7, 8],[6, 7],[9],[4]],
                       [[7],[6],[4, 8],[9],[1],[4, 8],[2, 3],[5],[2, 3]],
                       [[3, 4, 5],[9],[3, 4, 5],[3, 4, 5, 6],[4, 6, 7],[2],[6, 7],[8],[1]],
                       [[3, 4, 6],[7],[2, 3, 4, 6, 9],[2, 4, 6, 8],[5],[4, 6, 8],[2, 3, 4, 8, 9],[1],[2, 3, 8, 9]],
                       [[1, 3, 4, 5, 6],[2, 3, 5],[1, 2, 3, 4, 5, 6],[7],[2, 4, 6, 8],[9],[2, 3, 4, 5, 8],[2, 3],[2, 3, 8]],
                       [[4, 5],[8],[2, 4, 5, 9],[2, 4],[3],[1],[2, 4, 5, 9],[6],[7]],
                       [[2],[4],[3, 5, 6, 8],[1],[6, 8],[3, 5, 6, 8],[3, 8, 9],[7],[3, 6, 8, 9]],
                       [[3, 6, 8],[1],[3, 6, 7, 8],[2, 3, 6, 8],[9],[3, 6, 7, 8],[2, 3, 8],[4],[5]],
                       [[9],[3, 5],[3, 5, 6, 7, 8],[2, 3, 4, 5, 6, 8],[2, 4, 6, 7, 8],[3, 4, 5, 6, 7, 8],[1],[2, 3],[2, 3, 6, 8]]]
        grid_after = [[[1, 3, 5, 8],[2, 3, 5],[1, 2, 3, 5, 8],[3, 5, 6, 8],[6, 7, 8],[3, 5, 6, 7, 8],[6, 7],[9],[4]],
                       [[7],[6],[4, 8],[9],[1],[4, 8],[2, 3],[5],[2, 3]],
                       [[3, 4, 5],[9],[3, 4, 5],[3, 4, 5, 6],[4, 6, 7],[2],[6, 7],[8],[1]],
                       [[3, 4, 6],[7],[2, 3, 4, 6, 9],[2, 4, 6, 8],[5],[4, 6, 8],[2, 3, 4, 8, 9],[1],[2, 3, 8, 9]],
                       [[1, 3, 4, 5, 6],[3, 5],[1, 3, 4, 5, 6],[7],[2, 4, 6, 8],[9],[3, 4, 5, 8],[2, 3],[3, 8]],
                       [[4, 5],[8],[2, 4, 5, 9],[2, 4],[3],[1],[2, 4, 5, 9],[6],[7]],
                       [[2],[4],[3, 5, 6, 8],[1],[6, 8],[3, 5, 6, 8],[3, 8, 9],[7],[3, 6, 8, 9]],
                       [[3, 6, 8],[1],[3, 6, 7, 8],[2, 3, 6, 8],[9],[3, 6, 7, 8],[2, 3, 8],[4],[5]],
                       [[9],[3, 5],[3, 5, 6, 7, 8],[3, 4, 5, 6, 8],[2, 4, 6, 7, 8],[3, 4, 5, 6, 7, 8],[1],[2, 3],[3, 6, 8]]]

        #Run the xwing elimination
        grid, _ = x_wing(grid_before)

        #Check that the grid is as expected
        self.assertEqual(grid, grid_after)

    def test_removed_candidates_cols(self):
        #Define the grid before and the number of expected removed candidates
        grid_before = [[[1, 3, 5, 8],[2, 3, 5],[1, 2, 3, 5, 8],[3, 5, 6, 8],[6, 7, 8],[3, 5, 6, 7, 8],[6, 7],[9],[4]],
                       [[7],[6],[4, 8],[9],[1],[4, 8],[2, 3],[5],[2, 3]],
                       [[3, 4, 5],[9],[3, 4, 5],[3, 4, 5, 6],[4, 6, 7],[2],[6, 7],[8],[1]],
                       [[3, 4, 6],[7],[2, 3, 4, 6, 9],[2, 4, 6, 8],[5],[4, 6, 8],[2, 3, 4, 8, 9],[1],[2, 3, 8, 9]],
                       [[1, 3, 4, 5, 6],[2, 3, 5],[1, 2, 3, 4, 5, 6],[7],[2, 4, 6, 8],[9],[2, 3, 4, 5, 8],[2, 3],[2, 3, 8]],
                       [[4, 5],[8],[2, 4, 5, 9],[2, 4],[3],[1],[2, 4, 5, 9],[6],[7]],
                       [[2],[4],[3, 5, 6, 8],[1],[6, 8],[3, 5, 6, 8],[3, 8, 9],[7],[3, 6, 8, 9]],
                       [[3, 6, 8],[1],[3, 6, 7, 8],[2, 3, 6, 8],[9],[3, 6, 7, 8],[2, 3, 8],[4],[5]],
                       [[9],[3, 5],[3, 5, 6, 7, 8],[2, 3, 4, 5, 6, 8],[2, 4, 6, 7, 8],[3, 4, 5, 6, 7, 8],[1],[2, 3],[2, 3, 6, 8]]]
        expected_rm = 6

        #Run the xwing elimination
        _, removed = x_wing(grid_before)

        #Check that the number of removed candidates is as expected
        self.assertEqual(removed, expected_rm)


if __name__ == '__main__':
    unittest.main()