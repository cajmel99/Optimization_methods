import pandas as pd
import numpy as np
from load_data import *

data = CSVData('./data/config.csv', './data/scheduleMatrix.csv', './data/matchMatrix.csv')


def create_cost_matrix(schedule_matrix, match_matrix):
    # Find the maximum suitability score in the match matrix to convert to costs
    max_value = np.max(match_matrix)
    
    cost_matrix = []
    for i in range(len(schedule_matrix)):
        cost_row = []
        for j in range(len(schedule_matrix[i])):
            if schedule_matrix[i][j] == 1:
                # Cost is the max value minus the suitability score
                cost = max_value - match_matrix[i][j]
                cost_row.append(cost)
            else:
                # Set a very high cost for places where no assistant is needed
                cost_row.append(np.inf)
        cost_matrix.append(cost_row)
    return np.array(cost_matrix)

# Example usage to create the cost matrix
cost_matrix = create_cost_matrix(data.scheduleMatrixValues, data.matchMatrixValues)
print("Cost Matrix:\n", cost_matrix)


class HungarianAlgorithm:
    def __init__(self, cost_matrix, max_iterations=1000):
        self.cost_matrix = np.array(cost_matrix)
        self.n, self.m = self.cost_matrix.shape
        self.row_covered = np.zeros(self.n, dtype=bool)
        self.col_covered = np.zeros(self.m, dtype=bool)
        self.marked_zeros = np.zeros((self.n, self.m), dtype=int)
        self.max_iterations = max_iterations

    def subtract_row_min(self):
        for i in range(self.n):
            self.cost_matrix[i] -= self.cost_matrix[i].min()

    def subtract_col_min(self):
        for j in range(self.m):
            self.cost_matrix[:, j] -= self.cost_matrix[:, j].min()

    def cover_zeros(self):
        zero_locations = np.where(self.cost_matrix == 0)
        for i, j in zip(*zero_locations):
            if not self.row_covered[i] and not self.col_covered[j]:
                self.marked_zeros[i, j] = 1
                self.row_covered[i] = True
                self.col_covered[j] = True
        self.row_covered[:] = False
        self.col_covered[:] = False

    def cover_columns_with_marked_zeros(self):
        for i in range(self.n):
            for j in range(self.m):
                if self.marked_zeros[i, j] == 1:
                    self.col_covered[j] = True

    def find_min_uncovered_value(self):
        # Get the matrix of uncovered elements
        uncovered_elements = self.cost_matrix[~self.row_covered][:, ~self.col_covered]
        
        # Check if the uncovered elements array is empty or full of inf
        if uncovered_elements.size == 0 or np.all(np.isinf(uncovered_elements)):
            return np.inf  # No valid uncovered elements to minimize
        else:
            return np.min(uncovered_elements)

    def adjust_cost_matrix(self):
        min_val = self.find_min_uncovered_value()
        
        if min_val == np.inf:
            return  # If no valid uncovered element is found, do nothing
        
        for i in range(self.n):
            for j in range(self.m):
                if not self.row_covered[i] and not self.col_covered[j]:
                    self.cost_matrix[i, j] -= min_val
                if self.row_covered[i] and self.col_covered[j]:
                    self.cost_matrix[i, j] += min_val

    def find_a_zero(self):
        for i in range(self.n):
            for j in range(self.m):
                if self.cost_matrix[i, j] == 0 and not self.row_covered[i] and not self.col_covered[j]:
                    return (i, j)
        return None

    def run(self):
        self.subtract_row_min()
        self.subtract_col_min()
        self.cover_zeros()
        self.cover_columns_with_marked_zeros()

        iteration_count = 0

        while np.sum(self.col_covered) < self.n and iteration_count < self.max_iterations:
            zero = self.find_a_zero()
            while zero and iteration_count < self.max_iterations:
                row, col = zero
                self.marked_zeros[row, col] = 2
                star_col = np.where(self.marked_zeros[row] == 1)[0]
                if len(star_col) == 0:
                    # no star in the row, we need to find augmenting path and adjust zeros
                    self.step_four(row, col)
                    self.cover_columns_with_marked_zeros()
                else:
                    self.row_covered[row] = True
                    self.col_covered[star_col[0]] = False
                zero = self.find_a_zero()
                iteration_count += 1
            
            if np.sum(self.col_covered) < self.n and iteration_count < self.max_iterations:
                self.adjust_cost_matrix()
                self.cover_zeros()
                self.cover_columns_with_marked_zeros()
                iteration_count += 1

            # Increment iteration count at the end of each while loop iteration
            iteration_count += 1

        return self.get_results()

    def step_four(self, row, col):
        path = [(row, col)]
        while True:
            star_row = np.where(self.marked_zeros[:, col] == 1)[0]
            if len(star_row) == 0:
                break
            path.append((star_row[0], col))
            col = np.where(self.marked_zeros[star_row[0]] == 2)[0][0]
            path.append((star_row[0], col))
        for r, c in path:
            if self.marked_zeros[r, c] == 1:
                self.marked_zeros[r, c] = 0
            if self.marked_zeros[r, c] == 2:
                self.marked_zeros[r, c] = 1
        self.row_covered[:] = False
        self.col_covered[:] = False
        self.marked_zeros[self.marked_zeros == 2] = 0

    def get_results(self):
        results = []
        for i in range(self.n):
            for j in range(self.m):
                if self.marked_zeros[i, j] == 1:
                    results.append((i, j))
        return results

# Applying Hungarian Algorithm
hungarian_algorithm = HungarianAlgorithm(cost_matrix, max_iterations=1000000)
optimal_assignment = hungarian_algorithm.run()

print("Optimal assignment (Assistant, Place):", optimal_assignment)

# Function to interpret results and print them
def interpret_results(assignments, match_matrix_values):
    interpreted_results = []
    for assignment in assignments:
        assistant, place = assignment
        score = match_matrix_values[assistant][place]
        interpreted_results.append((assistant, place, score))
    return interpreted_results

# Interpret the results
assignments = interpret_results(optimal_assignment, data.matchMatrixValues)
print("Assignments (Assistant, Place, Suitability Score):")
for assignment in assignments:
    print(assignment)
