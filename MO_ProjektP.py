import csv
import pandas as pd
import random


class CSVData:
    def __init__(self, configFileName, scheduleMatrixFileName, matchMatrixFileName):
        pd.set_option('display.max_columns', None)
        pd.set_option('display.expand_frame_repr', False)
        pd.set_option('display.max_rows', None)
        
        self.configFileName = configFileName
        self.scheduleMatrixFileName = scheduleMatrixFileName
        self.matchMatrixFileName = matchMatrixFileName
        
        self.config = self.readCsv(self.configFileName)
        
        self.scheduleMatrix = self.readCsv(self.scheduleMatrixFileName)
        self.scheduleMatrixValues = [row[1:] for row in self.scheduleMatrix]
        del self.scheduleMatrixValues[0]
        self.scheduleMatrixValues= [[int(value) for value in row] for row in self.scheduleMatrixValues]
        
        self.matchMatrix = self.readCsv(self.matchMatrixFileName)
        self.matchMatrixValues = [row[1:] for row in self.matchMatrix]
        del self.matchMatrixValues[0]
        self.matchMatrixValues= [[float(value) for value in row] for row in self.matchMatrixValues]
        
        print("-" * 100)
        self.printData(self.config, self.configFileName)
        self.printData(self.scheduleMatrix, self.scheduleMatrixFileName)
        self.printData(self.matchMatrix, self.matchMatrixFileName)

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
        

class geneticAlghoritm:
    def __init__(self):
        data = CSVData('./config.csv','./scheduleMatrix.csv','./matchMatrix.csv')
        
        self.scheduleMatrix = data.scheduleMatrixValues
        self.matchMatrix = data.matchMatrixValues
        self.matchMatrixHeader = data.matchMatrix[0][1:]
        self.randomGenerator(self.scheduleMatrix)
    
    def randomGenerator(self, array):
        print("-" * 41, "Random generation","-" * 42, sep="")
        
        schedule = self.countOccurrences(array, 1, 0)
        if len(schedule) <= len(self.matchMatrix[0]):
            for x in range(len(self.matchMatrix[0]) - len(schedule)):
                schedule.append(-1)
        
        random.shuffle(schedule)
        
        table = pd.DataFrame([schedule], columns=self.matchMatrixHeader)
        print(table)
        
        fitness = self.fitness(schedule)
        print("Match =", fitness)
    
    def fitness(self, array):
        fitnessSum = 0.0
        for index, value in enumerate(array):
            if value != -1:
                fitnessSum += self.matchMatrix[value][index]
                
        return fitnessSum
 
    def countOccurrences(self, array, value, day):
        filteredArray = []
        for element in range(len(array)):
            if array[element][day] == value:
                filteredArray.append(element)
            else:
                filteredArray.append(-1)

        return filteredArray
    
geneticAlghoritm()
        
    


