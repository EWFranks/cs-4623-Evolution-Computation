import random
import math

# Define the problem and the fitness function
def knapsack_fitness(items, values, weights, max_weight, solution):
    total_value = sum(values[i] for i in range(len(items)) if solution[i] == 1)
    total_weight = sum(weights[i] for i in range(len(items)) if solution[i] == 1)
    if total_weight > max_weight:
        fitness = 0
    else:
        fitness = total_value
    return fitness

def perturb_flip(current_solution, index):
    new_solution = current_solution.copy()
    new_solution[index] = 1 - new_solution[index]
    return new_solution

def perturb_swap(current_solution, index1, index2):
    new_solution = current_solution.copy()
    new_solution[index1], new_solution[index2] = new_solution[index2], new_solution[index1]
    return new_solution

# Define the parameters of the SA
items = ['item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'item7', 'item8', 'item9', 'item10']
items = ['item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'item7', 'item8', 'item9', 'item10']
#weights = [16, 25, 20, 15, 18, 22, 10, 10, 15, 15, 11, 16, 16, 11, 15]
#values = [40, 30, 40, 20, 30, 40, 40, 50, 40, 45, 50, 40, 45, 40, 42]
#weights = [15, 15, 16, 25, 20, 15, 18, 22, 10, 10, 11, 16, 16, 11, 15, 16, 25, 20, 15, 18, 22, 11, 16, 16, 11, 15]
#values = [45, 40, 40, 30, 40, 20, 30, 40, 40, 50, 40, 45, 45, 40, 42, 40, 30, 40, 20, 30, 40, 50, 40, 45, 40, 42]
weights = [10, 15, 25, 20, 15, 10, 18, 22, 15, 16, 16, 16, 11, 15, 16, 25, 20, 15, 11, 10, 22, 11, 16, 16, 11, 15, 16,
          25, 20, 15, 18, 22, 11, 16, 16, 11, 15]
values = [40, 20, 30, 40, 40, 50, 30, 40, 45, 40, 45, 40, 40, 42, 40, 30, 40, 20, 50, 30, 40, 50, 40, 45, 40, 42, 40,
         30, 40, 20, 30, 40, 50, 40, 45, 40, 42]
chromosome_length = len(weights)
max_weight = 50
initial_temperature = 1000
cooling_rate = 0.95
iterations_per_temperature = 1000

# Initialize the current solution
current_solution = [random.randint(0, 1) for j in range(chromosome_length)]
current_fitness = knapsack_fitness(items, values, weights, max_weight, current_solution)

# Set the initial temperature
temperature = initial_temperature

# SA loop
while temperature > 1e-8:
    for i in range(iterations_per_temperature):
        # Generate a new solution
        bro1 = 2
        if bro1 < 0.5:
            index = random.randint(0, chromosome_length - 1)
            new_solution = perturb_flip(current_solution, index)
        else:
            index1, index2 = random.sample(range(chromosome_length), 2)
            new_solution = perturb_swap(current_solution, index1, index2)
        new_fitness = knapsack_fitness(items, values, weights, max_weight, new_solution)

        # Decide whether to accept the new solution
        delta = new_fitness - current_fitness
        if delta > 0:
            current_solution = new_solution
            current_fitness = new_fitness
        else:
            acceptance_probability = math.exp(delta / temperature)
            if random.random() < acceptance_probability:
                current_solution = new_solution
                current_fitness = new_fitness

    # Cool the temperature
    temperature *= cooling_rate

# Print the best solution and its fitness
print("Best Solution:")
best_solution = current_solution
total_value = 0
total_weight = 0
print("The chromosomes converted from binary to list")
for i in range(len(items)):
    if best_solution[i] == 1:
        print(f"{items[i]}: Value = {values[i]}, Weight = {weights[i]}")
        total_value += values[i]
        total_weight += weights[i]

print("Best Fitness: ", current_fitness)
