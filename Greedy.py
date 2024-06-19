from load_data import *
        
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

        timeStart = process_time_ns()
        self.run()
        timeStop = process_time_ns()
        print(timeStart, timeStop)
        print("Timer:", timeStop - timeStart)

        for _ in range(len(self.rowIndex)):
            self.rowIndexName.append(self.rowNames[self.rowIndex[_]])
        table = pd.DataFrame(self.result,columns=self.columnHeader, index=self.rowIndexName)
        table.index.name = 'Start point'
        print(table)
        self.result = [self.rowIndex[i:i+1] + row for i, row in enumerate(self.result)]
        self.columnHeader.insert(0, 'Start point')
        self.data.writeCSVArray('./data/result_greedy.csv', self.result, self.columnHeader)
        print()

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
            print("----------------------------------")
            start = start[1:] + [start[0]]
        
    def fitness(self, array):
        fitnessSum = 0.0
        
        for index, value in enumerate(array):
            if value != -1:
                fitnessSum += self.matchMatrix[value][index]
                print(self.matchMatrix[value][index])
                print(array[index])
                print("--------------------")

        return fitnessSum

greedyAlghoritm()