import csv
import pandas as pd

class CSVData:
    def __init__(self, configFileName, sheduleMatrixFileName, matchMatrixFileName):
        pd.set_option('display.max_columns', None)
        pd.set_option('display.expand_frame_repr', False)
        pd.set_option('display.max_rows', None)
        
        self.configFileName = configFileName
        self.sheduleMatrixFileName = sheduleMatrixFileName
        self.matchMatrixFileName = matchMatrixFileName
        
        self.config = self.readCsv(self.configFileName)
        self.sheduleMatrix = self.readCsv(self.sheduleMatrixFileName)
        self.matchMatrix = self.readCsv(self.matchMatrixFileName)
        
        print("-" * 100)
        self.printData(self.config, self.configFileName)
        self.printData(self.sheduleMatrix, self.sheduleMatrixFileName)
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

CSVData('./config.csv','./sheduleMatrix.csv','./matchMatrix.csv')
