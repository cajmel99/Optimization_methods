import csv
import pandas as pd
import random

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
    
    def writeCSVArray(self, fileName, array, header):
        with open(fileName, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(header)
            writer.writerows(array)
        
class greedyAlghoritm:
    def __init__(self):
        print("-" * 41, "Greedy Alghoritm","-" * 41)
        self.data = CSVData('./data/config.csv','./data/scheduleMatrix.csv','./data/matchMatrix.csv')

        self.scheduleMatrix = self.data.scheduleMatrixValues
        self.matchMatrix = self.data.matchMatrixValues
        
        self.columnHeader = self.data.matchMatrix[0][1:]
        self.columnHeader.append('Fitness')
        self.rowNames = [row[0] for row in self.data.matchMatrix[1:]]
        self.rowIndex = []
        self.rowIndexName = []

        self.result = []

        self.run()

        for _ in range(len(self.rowIndex)):
            self.rowIndexName.append(self.rowNames[self.rowIndex[_]])
        table = pd.DataFrame(self.result,columns=self.columnHeader, index=self.rowIndexName)
        table.index.name = 'Start point'
        print(table)
        self.result = [self.rowIndex[i:i+1] + row for i, row in enumerate(self.result)]
        self.columnHeader.insert(0, 'Start point')
        self.data.writeCSVArray('./data/result_greedy.csv', self.result, self.columnHeader)

    def run(self):
        start = list(range(len(self.matchMatrix)))
        daySchedule = []
        for _ in range(len(self.scheduleMatrix)):
            daySchedule.append(self.scheduleMatrix[_][0])

        indices = [index for index, value in enumerate(daySchedule) if value == 0]
        for _ in indices:
            start.remove(_)
        
        self.rowIndex = start

        for i in range(len(start)):
            matchedAssistant = []
            used = []
            for productionID in start:
                bestTempFitness = 0
                bestAssistant = None
                for assistantID in range(len(self.matchMatrix[0])):
                    tempFitness = self.matchMatrix[productionID][assistantID]
                    if tempFitness > bestTempFitness and assistantID not in used:
                        bestTempFitness = tempFitness
                        bestAssistant = assistantID
     
                used.append(bestAssistant)
                matchedAssistant.append([productionID, bestAssistant] )
            
            tMatchedAssistant = [-1] * len(self.matchMatrix[0])
            for ProductionIndex in range(len(matchedAssistant)):
                tMatchedAssistant[matchedAssistant[ProductionIndex][1]] = matchedAssistant[ProductionIndex][0]
            tMatchedAssistant.append("{:.1f}".format(self.fitness(tMatchedAssistant)))
            self.result.append(tMatchedAssistant)

            start = start[1:] + [start[0]]
        
    def fitness(self, array):
        fitnessSum = 0.0
        
        for index, value in enumerate(array):
            if value != -1:
                fitnessSum += self.matchMatrix[value][index]
                
        return fitnessSum


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
        self.bestFitness = -float("inf")
        self.bestIndividual = []
        
        self.run()

    def run(self):
        firstPopulation = self.generatePopulation(self.populations)
        self.bestFitness, self.bestIndividual = self.evalutaPopulation(firstPopulation)
        population = firstPopulation
        mutationCount = 0
        crossoverCount = 0
        
        for x in range(self.generations):
            newPopulation = []
            for y in range(self.populations):
                parent1 = self.selection(population)
                parent2 = self.selection(population)
            
                if random.random() < self.crossProbability:
                    newPopulation.append(self.crossover(parent1, parent2))
                    crossoverCount += 1
                elif random.random() < self.mutationProbability:
                    newPopulation.append(self.mutation(parent1))
                    mutationCount += 1
                else:
                    newPopulation.append(parent1)

            fitness, bestIndividual = self.evalutaPopulation(newPopulation)

            if fitness > self.bestFitness:
                self.bestFitness = fitness
                self.bestIndividual = bestIndividual

            population = newPopulation

        print("Best fitness:", self.bestFitness)
        print("Best individual:", self.bestIndividual)
            
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
                index1 = random.randint(0, len(individual) - 1)
                index2 = random.randint(0, len(individual) - 1)
                
                individual[index1], individual[index2] = individual[index2], individual[index1]
         
        return individual  
    
    def crossover(self, parent1, parent2):
        cross = [-1] * len(parent1)
        start = random.randint(0, len(parent1) - 1)
        end = random.randint(0, len(parent1) - 1)
        
        if start > end:
            start, end = end, start

        for i in range(start, end + 1):
            cross[i] = parent1[i]

        j = 0
        used_genes = set(parent1[start:end + 1])
        j = end + 1
        for i in range(len(parent2)):
            if j == len(cross):
                break
            
            if parent2[i] not in used_genes or parent2[i] == -1:
                cross[j] = parent2[i]
                used_genes.add(parent2[i])
                j += 1
            
        return cross
        
    def randomGenerator(self, array):
        #print("-" * 41, "Random generation","-" * 42, sep="")
        
        schedule = self.countOccurrences(array, 1, 0)
        if len(schedule) <= len(self.matchMatrix[0]):
            for x in range(len(self.matchMatrix[0]) - len(schedule)):
                schedule.append(-1)
        
        random.shuffle(schedule)
        
        #table = pd.DataFrame([schedule], columns=self.matchMatrixHeader)
        #print(table)
        
        #fitness = self.fitness(schedule)
        #print("Match =", fitness)
        
        return schedule
    
    def generatePopulation(self, populationSize):
        population = []
        
        for x in range(populationSize):
            population.append(self.randomGenerator(self.scheduleMatrix))
        
        #table = pd.DataFrame(population, columns=self.matchMatrixHeader)
        #print(table)
        
        return population

    def evalutaPopulation(self, population):
        evaluatedPopulation = []

        for x in range(len(population)):
            fitness = self.fitness(population[x])
            pair = (fitness, population[x])
            evaluatedPopulation.append(pair)

        bestIndividual = max(evaluatedPopulation, key=lambda x: x[0])[1]
        maxFitness = "{:.1f}".format(max(evaluatedPopulation, key=lambda x: x[0])[0])
        minFitness = "{:.1f}".format(min(evaluatedPopulation, key=lambda x: x[0])[0])
        avgFitness = "{:.2f}".format(sum(pair[0] for pair in evaluatedPopulation) / len(evaluatedPopulation))

        #print("Maximum:", maxFitness)
        #print("Minimum:", minFitness)
        #print("Average:", avgFitness)
        
        populationFitness = [maxFitness, minFitness, avgFitness]
        self.data.writeCSV("./data/results.csv", populationFitness)

        return float(maxFitness), bestIndividual
    
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
    
greedyAlghoritm()
geneticAlghoritm()
