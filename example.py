import csv
import pandas as pd
import random

class CSVData:
    def __init__(self, config_file_name, schedule_matrix_file_name, match_matrix_file_name):
        self.config_file_name = config_file_name
        self.schedule_matrix_file_name = schedule_matrix_file_name
        self.match_matrix_file_name = match_matrix_file_name
        self.load_data()

    def load_data(self):
        self.config = self.read_csv(self.config_file_name)
        self.config_value = [row[:] for row in self.config[1:]]
        self.config_value = [[float(value) for value in row] for row in self.config_value]

        self.schedule_matrix = self.read_csv(self.schedule_matrix_file_name)
        self.schedule_matrix_values = [[int(value) for value in row[1:]] for row in self.schedule_matrix[1:]]

        self.match_matrix = self.read_csv(self.match_matrix_file_name)
        self.match_matrix_values = [[float(value) for value in row[1:]] for row in self.match_matrix[1:]]

    def read_csv(self, file_name):
        data = []
        with open(file_name, 'r') as file:
            csv_reader = csv.reader(file)
            data = list(csv_reader)
        return data

    def print_data_summary(self):
        print("-" * 100)
        self.print_data(self.config, self.config_file_name)
        self.print_data(self.schedule_matrix, self.schedule_matrix_file_name)
        self.print_data(self.match_matrix, self.match_matrix_file_name)
        print("-" * 100)

    def print_data(self, array, file_name):
        print(f"File: {file_name}")
        print(f"Rows loaded: {len(array) - 1}\n")
        table = pd.DataFrame(array[1:], columns=array[0])
        print(table)
        print("-" * 100)


# Example of usage
data = CSVData('./config.csv', './scheduleMatrix.csv', './matchMatrix.csv')
data.print_data_summary()

class GeneticAlgorithm:
    def __init__(self):
        self.data = CSVData('./config.csv', './scheduleMatrix.csv', './matchMatrix.csv')
        
        self.schedule_matrix = self.data.schedule_matrix_values
        self.match_matrix = self.data.match_matrix_values
        self.match_matrix_header = self.data.match_matrix[0][1:]
        
        self.cross_probability = self.data.config_value[0][0]
        self.mutation_probability = self.data.config_value[0][1]
        self.populations = int(self.data.config_value[0][2])
        self.generations = int(self.data.config_value[0][3])
        self.selections = int(self.data.config_value[0][4])
        
        self.run()

    def run(self):
        population = self.generate_population(100)
        for _ in range(self.generations):
            new_population = []
            for _ in range(self.populations):
                parent1 = self.selection(population)
                parent2 = self.selection(population)
                print(f"Type of Parent1: {type(parent1)}, Parent1: {parent1}")
                print(f"Type of Parent2: {type(parent2)}, Parent2: {parent2}")
                if isinstance(parent1, int) or isinstance(parent2, int):
                    raise Exception("Parent is an integer, expected a list. Check selection and mutation logic.")
                child = self.cross(parent1, parent2)
                new_population.append(child)
            population = new_population



    def selection(self, population):
    # Ensures that each individual in the population is indeed a tuple of (fitness, individual)
        best_individual = max(population, key=lambda individual: individual[0])
        return best_individual[1]  # Return the individual part, not the fitness score


    def mutation(self, individual):
        if random.random() < self.mutation_probability:
            index1, index2 = random.sample(range(len(individual)), 2)
            individual[index1], individual[index2] = individual[index2], individual[index1]
        return individual  # Make sure this always returns the entire list


    
    def selection(self, population):
        best_individual = max(population, key=lambda individual: individual[0])
        return list(best_individual[1])  # Return a copy of the list to avoid accidental mutations affecting the population


    def cross(self, parent1, parent2):
        if not isinstance(parent1, list) or not isinstance(parent2, list):
            raise ValueError("Expected both parents to be lists.")
        start, end = sorted(random.sample(range(len(parent1)), 2))
        child = parent1[:start] + parent2[start:end] + parent1[end:]
        return child

    
    def generate_population(self, population_size):
        population = []
        for _ in range(population_size):
            individual = self.random_generator(self.schedule_matrix)  # Ensure this returns a list
            population.append((self.fitness(individual), individual))
        return population

    def evaluate_population(self, population):
        evaluated = [(self.fitness(ind), ind) for ind in population]
        return max(evaluated)[0]

    def fitness(self, individual):
        # Ensures that individual is a list of integers representing indices in the match matrix
        return sum(self.match_matrix[i][index] if index != -1 else 0 for index, i in enumerate(individual))

    def random_generator(self, array):
        schedule = self.count_occurrences(array, 1, 0)
        random.shuffle(schedule)
        return schedule

    def count_occurrences(self, array, value, day):
        return [i if array[i][day] == value else -1 for i in range(len(array))]

# Usage
if __name__ == "__main__":
    GeneticAlgorithm()