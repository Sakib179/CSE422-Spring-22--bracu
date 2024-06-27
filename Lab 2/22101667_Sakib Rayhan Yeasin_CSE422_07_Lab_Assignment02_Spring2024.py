import random

population_size = 10
max_generation = 100


# Creating transaction register
def create_register(transactions):
    return [amount if action == 'd' else -amount for action, amount in transactions]


def calculate_fitness(register, bitstring):
    if all(bit == 0 for bit in bitstring):
        return float('inf')  # igmore all-zero solutions
    total = sum(register[i] for i in range(len(bitstring)) if bitstring[i] == 1)
    return abs(total)


def create_population(size, length):
    return [[random.randint(0, 1) for _ in range(length)] for _ in range(size)]


def mutate(bitstring):
    mutation_point = random.randint(0, len(bitstring) - 1)
    bitstring[mutation_point] = 1 - bitstring[mutation_point]  # Mutating one bit


def genetic_algorithm(transactions):
    register = create_register(transactions)
    population = create_population(population_size, len(register))

    for _ in range(max_generation):
        fitness = [calculate_fitness(register, individual) for individual in population]

        for i, individual in enumerate(population):
            if fitness[i] == 0:
                return ''.join(map(str, individual)) 

        sorted_population = [x for _, x in sorted(zip(fitness, population), key=lambda pair: pair[0])]
        new_population = sorted_population[:2]  # Keeping the best two chromose

        while len(new_population) < population_size:
            for i in range(0, len(sorted_population) - 3, 2):
                parent1, parent2 = sorted_population[i], sorted_population[i + 1]
                child = [parent1[j] if j % 2 == 0 else parent2[j] for j in range(len(parent1))]
                mutate(child)
                new_population.append(child)

        population = new_population[:population_size]

    return '-1'


# Taking input from txt file
with open("22101667_Sakib Rayhan Yeasin_CSE422_07_Lab_Assignment02_InputFile_Spring2024.txt", "r") as input_file:
    transaction_num = input_file.readline()

    transactions_sample = []

    for _ in range(int(transaction_num)):
        transaction = input_file.readline()
        action, amount = transaction.split()
        amount = int(amount)
        transactions_sample.append((action, amount))

    # Running the algorithm
    print(genetic_algorithm(transactions_sample))
