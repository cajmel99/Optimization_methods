import csv
import pandas as pd
import random

class CSVReader:
    """ Utility class for reading CSV files """
    @staticmethod
    def read_csv(file_name):
        with open(file_name, 'r') as file:
            csv_reader = csv.reader(file)
            return list(csv_reader)

class CSVData:
    def __init__(self, config_file_name, schedule_matrix_file_name, match_matrix_file_name):
        self.config_file_name = config_file_name
        self.schedule_matrix_file_name = schedule_matrix_file_name
        self.match_matrix_file_name = match_matrix_file_name
        self.load_data()
        self.header_written = False

    def load_data(self):
        self.config = CSVReader.read_csv(self.config_file_name)
        self.config_value = [[float(value) for value in row] for row in self.config[1:]]

        self.schedule_matrix = CSVReader.read_csv(self.schedule_matrix_file_name)
        self.schedule_matrix_values = [[int(value) for value in row[1:]] for row in self.schedule_matrix[1:]]

        self.match_matrix = CSVReader.read_csv(self.match_matrix_file_name)
        self.match_matrix_values = [[float(value) for value in row[1:]] for row in self.match_matrix[1:]]

    def print_data_summary(self):
        print("-" * 100)
        for data, name in [(self.config, self.config_file_name), 
                           (self.schedule_matrix, self.schedule_matrix_file_name), 
                           (self.match_matrix, self.match_matrix_file_name)]:
            print(f"File: {name}")
            print(f"Rows loaded: {len(data) - 1}\n")
            table = pd.DataFrame(data[1:], columns=data[0])
            print(table)
            print("-" * 100)

    def write_csv(self, file_name, array):
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            if not self.header_written:
                writer.writerow(['Max', 'Min', 'Avg'])
                self.header_written = True
            writer.writerow(array)

class GeneticAlgorithm:
    """ Class implementing a basic genetic algorithm """
    def __init__(self):
        self.data = CSVData('./data/config.csv', './data/scheduleMatrix.csv', './data/matchMatrix.csv')
        self.initialize_parameters()

    def initialize_parameters(self):
        self.schedule_matrix = self.data.schedule_matrix_values
        self.match_matrix = self.data.match_matrix_values
        self.match_matrix_header = self.data.match_matrix[0][1:]
        self.cross_probability = self.data.config_value[0][0]
        self.mutation_probability = self.data.config_value[0][1]
        self.populations = int(self.data.config_value[0][2])
        self.generations = int(self.data.config_value[0][3])
        self.selections = int(self.data.config_value[0][4])

    def run(self):
        # Initial population generation and evaluation
        population = [self.random_generator(self.schedule_matrix) for _ in range(100)]
        best_match = self.evaluate_population(population)

        # Evolution process
        for _ in range(self.generations):
            new_population = [self.selection(population) for _ in range(self.populations)]
            population = [self.mutation(ind) if random.random() > self.cross_probability else ind for ind in new_population]

    def selection(self, population):
        return max(population, key=lambda ind: self.fitness(ind))

    def mutation(self, individual):
        if random.random() < self.mutation_probability:
            idx1, idx2 = random.sample(range(len(individual)), 2)
            individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
        return individual

    def evaluate_population(self, population):
        fitness_scores = [self.fitness(ind) for ind in population]
        max_fitness = max(fitness_scores)
        print(f"Maximum Fitness: {max_fitness}")
        return max_fitness

    def fitness(self, individual):
        return sum(self.match_matrix[ind][idx] if ind != -1 else 0 for idx, ind in enumerate(individual))

    def random_generator(self, matrix):
        individual = [random.choice(row[1:]) for row in matrix]
        random.shuffle(individual)
        return individual


# Test CSV class
data = CSVData('./data/config.csv', './data/scheduleMatrix.csv', './data/matchMatrix.csv')
data.print_data_summary()

# Usage
ga = GeneticAlgorithm()
ga.run()
#ga.random_generator()