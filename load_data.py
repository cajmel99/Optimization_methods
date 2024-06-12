import csv
import pandas as pd
import random
from time import process_time 
from time import process_time_ns 

#Table display settings
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)


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
        
        self.hederWrited = False
        self.hederWritedRows = False

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
        if self.hederWrited == False:
            with open(fileName, mode='w', newline='') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(['Max', 'Min', 'Avg'])
                self.hederWrited = True

        with open(fileName, mode='a', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(array)
    
    def writeCSVRows(self, fileName, header, array):
        if self.hederWritedRows == False:
            with open(fileName, mode='w', newline='') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(header)
                self.hederWritedRows = True

        with open(fileName, mode='a', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(array)
    
    def writeCSVArray(self, fileName, array, header):
        with open(fileName, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(header)
            writer.writerows(array)