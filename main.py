import csv
import pandas as pd
import random

#Ustawienia wyświetlania tabel
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', None)

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
        #Tylko wartości jako INT
        self.scheduleMatrixValues = [row[1:] for row in self.scheduleMatrix]
        del self.scheduleMatrixValues[0]
        self.scheduleMatrixValues= [[int(value) for value in row] for row in self.scheduleMatrixValues]
        
        self.matchMatrix = self.readCsv(self.matchMatrixFileName)
        #Tylko wartości jako FLOAT
        self.matchMatrixValues = [row[1:] for row in self.matchMatrix]
        del self.matchMatrixValues[0]
        self.matchMatrixValues= [[float(value) for value in row] for row in self.matchMatrixValues]
        
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
        
        

class geneticAlghoritm:
    def __init__(self):
        self.data = CSVData('./data/config.csv','./data/scheduleMatrix.csv','./data/matchMatrix.csv')
        
        self.scheduleMatrix = self.data.scheduleMatrixValues
        self.matchMatrix = self.data.matchMatrixValues
        self.matchMatrixHeader = self.data.matchMatrix[0][1:]
        
        self.crossProbability = self.data.configValue[0][0]
        self.mutationProbability = self.data.configValue[0][1]
        self.populations = int(self.data.configValue[0][2])
        self.generations = int(self.data.configValue[0][3])
        self.selections = int(self.data.configValue[0][4])
        self.randomGenerator(self.scheduleMatrix)
        
        self.run()

    def run(self):
        firstPopulation = self.generatePopulation(100)
        bestMatch = self.evalutaPopulation(firstPopulation)
        newPopulation = firstPopulation
        
        for x in range(self.generations):
            population = []
            for y in range(self.populations):
                parent1 = self.selection(newPopulation)
                parent2 = self.selection(newPopulation)
            
                if random.random() < self.crossProbability:
                    continue  
                else:
                    population.append(self.mutation(parent1))
            
    def selection(self, population):
        bestFitness = -float("inf")
        bestIndividual = []
        for x in range(self.selections):
            index = random.randint(0,len(self.matchMatrix[0]))
            fitness = self.fitness(population[index])
            if fitness > bestFitness:
                bestFitness = fitness
                bestIndividual = population[x]
        
        return bestIndividual
    
    def mutation(self, individual):
        for x in range(len(individual)):
            if random.random() < self.mutationProbability:
                index1 = random.randint(0, len(individual) - 1)
                index2 = random.randint(0, len(individual) - 1)
                
                individual[index1], individual[index2] = individual[index2], individual[index1]
         
        return individual  
    
    def cross(self, parent1, parent2):
        start = random.random(0, len(parent1) - 1)
        end = random.random(0, len(parent1) - 1)
        
        if start > end:
            start, end = end, start

        
        
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
        
        return schedule
    
    def generatePopulation(self, populationSize):
        population = []
        
        for x in range(populationSize):
            population.append(self.randomGenerator(self.scheduleMatrix))
        
        table = pd.DataFrame(population, columns=self.matchMatrixHeader)
        print(table)
        
        return population

    def evalutaPopulation(self, population):
        evaluatedPopulation = []
        
        for x in range(len(population)):
            fitness = self.fitness(population[x])
            pair = (fitness, population[x])
            evaluatedPopulation.append(pair)
        
        maxFitness = "{:.1f}".format(max(evaluatedPopulation, key=lambda x: x[0])[0])
        minFitness = "{:.1f}".format(min(evaluatedPopulation, key=lambda x: x[0])[0])
        avgFitness = "{:.2f}".format(sum(pair[0] for pair in evaluatedPopulation) / len(evaluatedPopulation))
        
        print("Maximum:", maxFitness)
        print("Minimum:", minFitness)
        print("Average:", avgFitness)
        
        populationFitness = [maxFitness, minFitness, avgFitness]
        self.data.writeCSV("./results.csv", populationFitness)

        return maxFitness
    
    def fitness(self, array):
        fitnessSum = 0.0
        
        for index, value in enumerate(array):
            if value != -1:
                fitnessSum += self.matchMatrix[value][index]
                
        return fitnessSum
 
    def countOccurrences(self, array, value, day):
        """
        Function which help ensure no taking asistant for one day
        """
        filteredArray = []
        
        for element in range(len(array)):
            if array[element][day] == value:
                filteredArray.append(element)
            else:
                filteredArray.append(-1)

        return filteredArray
    
geneticAlghoritm()
        
    


