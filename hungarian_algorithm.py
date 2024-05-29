import numpy as np
import csv
import pandas as pd

def hungarian_algorithm(cost_matrix):
    # Step 1: Subtract row minima
    cost_matrix = np.array(cost_matrix)  # Ensure cost_matrix is a NumPy array
    cost_matrix -= cost_matrix.min(axis=1)[:, np.newaxis]
    
    # Step 2: Subtract column minima
    cost_matrix -= cost_matrix.min(axis=0)
    
    # Step 3: Cover all zeros with a minimum number of lines
    num_rows, num_cols = cost_matrix.shape
    covered_rows = np.zeros(num_rows, dtype=bool)
    covered_cols = np.zeros(num_cols, dtype=bool)
    starred_zeros = np.zeros_like(cost_matrix, dtype=bool)
    primed_zeros = np.zeros_like(cost_matrix, dtype=bool)
    
    def cover_zeros():
        for i in range(num_rows):
            for j in range(num_cols):
                if cost_matrix[i, j] == 0 and not covered_rows[i] and not covered_cols[j]:
                    starred_zeros[i, j] = True
                    covered_rows[i] = True
                    covered_cols[j] = True
    
    def cover_columns():
        covered_cols[:] = np.any(starred_zeros, axis=0)
    
    def find_smallest_uncovered():
        min_val = np.inf
        for i in range(num_rows):
            if not covered_rows[i]:
                for j in range(num_cols):
                    if not covered_cols[j]:
                        if cost_matrix[i, j] < min_val:
                            min_val = cost_matrix[i, j]
        return min_val
    
    def adjust_matrix(min_val):
        for i in range(num_rows):
            if covered_rows[i]:
                cost_matrix[i, :] += min_val
        for j in range(num_cols):
            if not covered_cols[j]:
                cost_matrix[:, j] -= min_val
    
    cover_zeros()
    cover_columns()
    
    while not np.all(covered_cols):
        min_val = find_smallest_uncovered()
        adjust_matrix(min_val)
        cover_zeros()
        cover_columns()
        
        # Debugging: Print out cost_matrix and other variables to diagnose the issue
        print("Current cost matrix:")
        print(cost_matrix)
        print("Covered rows:")
        print(covered_rows)
        print("Covered columns:")
        print(covered_cols)
        print("-" * 50)
    
    optimal_assignment = []
    for i in range(num_rows):
        for j in range(num_cols):
            if starred_zeros[i, j]:
                optimal_assignment.append((i, j))
    
    return optimal_assignment

class CSVData:
    def __init__(self, configFileName, scheduleMatrixFileName, matchMatrixFileName):    
        self.configFileName = configFileName
        self.scheduleMatrixFileName = scheduleMatrixFileName
        self.matchMatrixFileName = matchMatrixFileName
        
        self.config = self.readCsv(self.configFileName)
        self.configValue = [row[0:] for row in self.config]
        del self.configValue[0]
        self.configValue= [[float(value) for value in row] for row in self.configValue]
        
        
        self.scheduleMatrix = self.readCsv(self.scheduleMatrixFileName)
        # Tylko wartości jako INT
        self.scheduleMatrixValues = [row[1:] for row in self.scheduleMatrix]
        del self.scheduleMatrixValues[0]
        self.scheduleMatrixValues= [[int(value) for value in row] for row in self.scheduleMatrixValues]
        
        self.matchMatrix = self.readCsv(self.matchMatrixFileName)
        # Tylko wartości jako FLOAT
        self.matchMatrixValues = [row[1:] for row in self.matchMatrix]
        del self.matchMatrixValues[0]
        self.matchMatrixValues= [[float(value) for value in row] for row in self.matchMatrixValues]
        
        # Convert matchMatrixValues to NumPy array
        self.matchMatrixValues = np.array(self.matchMatrixValues)
        
        print("-" * 100)
        self.printData(self.config, self.configFileName)
        self.printData(self.scheduleMatrix, self.scheduleMatrixFileName)
        self.printData(self.matchMatrix, self.matchMatrixFileName)
        
        self.hederWrited = False

    def readCsv(self, fileName):
        readedData = []
        
        with open(fileName, 'r') as file:
            csvReader = csv.reader(file)
            for row in csvReader:
                readedData.append(row)
                
        return readedData

    def printData(self, array, fileName):
        print("File:", fileName[2:],)
        print("Rows loaded:", len(array)-1, "\n")
        columnHeader = array[0]
        data = array[1:]
        
        table = pd.DataFrame(data, columns=columnHeader)
        print(table)
        print("-" * 100)
    
    def writeCSV(self, fileName, array):
        with open(fileName, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            if self.hederWrited == False:
                writer.writerow(['Max', 'Min', 'Avg'])
                self.hederWrited = True
            writer.writerow(array)
        
        

class hungarianAlgorithm:
    def __init__(self):
        self.data = CSVData('./data/config.csv','./data/scheduleMatrix.csv','./data/matchMatrix.csv')
        
        self.scheduleMatrix = self.data.scheduleMatrixValues
        self.matchMatrix = self.data.matchMatrixValues
        self.matchMatrixHeader = self.data.matchMatrix[0][1:]
        
        self.run()

    def run(self):
        # Get the optimal assignment using the Hungarian algorithm
        optimal_assignment = hungarian_algorithm(self.matchMatrix)

        # Display the optimal assignment
        print("Optimal assignment (crew member, task):")
        for assignment in optimal_assignment:
            print(f"Crew {assignment[0]} -> Task {assignment[1]}")

# Main program entry point
if __name__ == "__main__":
    ha = hungarianAlgorithm()
