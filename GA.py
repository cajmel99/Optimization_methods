from load_data import *

class geneticAlgorithm:
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
        
        timeStart = process_time_ns()
        self.run()
        timeStop = process_time_ns()
        print(timeStart, timeStop)
        print("Timer:", timeStop - timeStart)

    def run(self):
        firstPopulation = self.generatePopulation(self.populations)
        self.bestFitness, self.bestIndividual = self.evalutaPopulation(firstPopulation)
        print(f"----->First popoulation{firstPopulation}")
        print(f"----->First besst, fitness, best individual{self.bestFitness, self.bestIndividual}")
        population = firstPopulation
        mutationCount = 0
        crossoverCount = 0
        
        for x in range(self.generations):
            newPopulation = []
            for _ in range(self.populations):
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
            print(f"--->Fitnesss {fitness}, {self.bestFitness}")

            if fitness > self.bestFitness:
                self.bestFitness = fitness
                self.bestIndividual = bestIndividual
                population = newPopulation

        print("Best fitness:", self.bestFitness)
        print("Best individual:", self.bestIndividual)
            
    def selection(self, population):
        bestFitness = -float("inf")
        bestIndividual = []
        for x in range(self.selections): # Wybieramy 5 najlepszych osobnikow
            matrix = self.matchMatrix[0] # Wartosci funckji dobroci
            index = random.randint(0, len(population)-1) # Losujemy osobnika z populacji
            fitness = self.fitness(population[index])

            if fitness > bestFitness:
                bestFitness = fitness
                bestIndividual = population[index]
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
        schedule = self.countOccurrences(array, 1, 0)
        if len(schedule) <= len(self.matchMatrix[0]):
            for x in range(len(self.matchMatrix[0]) - len(schedule)):
                schedule.append(-1)
        
        random.shuffle(schedule)
        
        return schedule
    
    def generatePopulation(self, populationSize):
        population = []
        
        for x in range(populationSize):
            population.append(self.randomGenerator(self.scheduleMatrix))
        
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
    
class randomAlghoritm:
    def __init__(self, iterations):
        print("-" * 41, "Random generation","-" * 42, sep="")
        self.data = CSVData('./data/config.csv','./data/scheduleMatrix.csv','./data/matchMatrix.csv')
        
        self.scheduleMatrix = self.data.scheduleMatrixValues
        self.matchMatrix = self.data.matchMatrixValues
        self.result = []
        
        self.columnHeader = self.data.matchMatrix[0][1:]
        self.columnHeader.append('Fitness')
        timeStart = process_time()
        for _ in range(iterations):
            self.randomGenerator(self.scheduleMatrix)
        timeStop = process_time()

        print("Timer", timeStop - timeStart)

        table = pd.DataFrame(self.result,columns=self.columnHeader)
        table.index.name = 'Iteration'
        print(table)

    def countOccurrences(self, array, value, day):
        filteredArray = []
        
        for element in range(len(array)):
            if array[element][day] == value:
                filteredArray.append(element)
            else:
                filteredArray.append(-1)

        return filteredArray 
    
    def randomGenerator(self, array):
        result = []
        schedule = self.countOccurrences(array, 1, 0)
        if len(schedule) <= len(self.matchMatrix[0]):
            for x in range(len(self.matchMatrix[0]) - len(schedule)):
                schedule.append(-1)
        
        random.shuffle(schedule)
        fitness = self.fitness(schedule)
        for index in range(len(schedule)):
            result.append(schedule[index])

        result.append("{:.1f}".format(fitness))

        self.data.writeCSVRows('./data/result_random.csv', self.columnHeader, result)
        self.result.append(result)
    
    def fitness(self, array):
        fitnessSum = 0.0
        
        for index, value in enumerate(array):
            if value != -1:
                fitnessSum += self.matchMatrix[value][index]
                
        return fitnessSum
    

geneticAlgorithm()
#randomAlgorithm(10000)
