import random


# Define the problem and the fitness function
def knapsack_fitness(items, values, weights, max_weight, solution):
    total_value = sum(values[i] for i in range(len(items)) if solution[i] == 1)
    total_weight = sum(weights[i] for i in range(len(items)) if solution[i] == 1)
    if total_weight > max_weight:
        fitness = 0  # return a very low fitness value for invalid solutions
    else:
        fitness = total_value
    return fitness


# Define the parameters of the SGA
population_size = 300
crossover_probability = 0.8
mutation_probability = 0.1
max_generations = 1000

# Define the items, values, and weights of the knapsack
items = ['item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'item7', 'item8', 'item9', 'item10']
#weights = [16, 25, 20, 15, 18, 22, 10, 10, 15, 15, 11, 16, 16, 11, 15]
#values = [40, 30, 40, 20, 30, 40, 40, 50, 40, 45, 50, 40, 45, 40, 42]
#weights = [15, 15, 16, 25, 20, 15, 18, 22, 10, 10, 11, 16, 16, 11, 15, 16, 25, 20, 15, 18, 22, 11, 16, 16, 11, 15]
#values = [45, 40, 40, 30, 40, 20, 30, 40, 40, 50, 40, 45, 45, 40, 42, 40, 30, 40, 20, 30, 40, 50, 40, 45, 40, 42]
# weights = [10, 15, 25, 20, 15, 10, 18, 22, 15, 16, 16, 16, 11, 15, 16, 25, 20, 15, 11, 10, 22, 11, 16, 16, 11, 15, 16,
#          25, 20, 15, 18, 22, 11, 16, 16, 11, 15]
# values = [40, 20, 30, 40, 40, 50, 30, 40, 45, 40, 45, 40, 40, 42, 40, 30, 40, 20, 50, 30, 40, 50, 40, 45, 40, 42, 40,
#         30, 40, 20, 30, 40, 50, 40, 45, 40, 42]

weights = [10, 15, 25, 16, 15, 10, 15, 25, 10, 15, 20, 15, 18, 22, 11, 16, 16, 11, 15, 18, 22, 15, 16, 16, 16, 11, 15,
           16, 25, 20, 15, 11, 10, 22, 11, 16, 16, 11, 15, 16,
           25, 20, 15, 18, 22, 11, 16, 16, 11, 15]
values = [40, 20, 30, 40, 20, 20, 40, 30, 50, 45, 40, 20, 30, 40, 50, 40, 45, 40, 42, 30, 40, 45, 40, 45, 40, 40, 42,
          40, 30, 40, 20, 50, 30, 40, 50, 40, 45, 40, 42, 40,
          30, 40, 20, 30, 40, 50, 40, 45, 40, 42]
max_weight = 50
chromosome_length = len(values)

# Select a selection method randomly
bro1 = 1
if bro1 < 0.5:
    selection_method = "tournament"
else:
    selection_method = "rank"

# Initialize the population
population = []
for i in range(population_size):
    chromosome = [random.randint(0, 1) for j in range(chromosome_length)]
    population.append(chromosome)

# Evaluate the fitness of each solution in the population
fitness_scores = []
for chromosome in population:
    fitness = knapsack_fitness(items, values, weights, max_weight, chromosome)
    fitness_scores.append(fitness)

# Calculate selection probabilities based on fitness scores
total_fitness = sum(fitness_scores)
probabilities = [fitness / total_fitness for fitness in fitness_scores]

# Evolution loop
best_fitness = 0
for generation in range(max_generations):
    # Select parents for reproduction
    if selection_method == "tournament":
        parent1 = population[random.randint(0, population_size - 1)]
        parent2 = population[random.randint(0, population_size - 1)]
    else:
        if len(probabilities) != len(population):
            raise ValueError("The number of probabilities does not match the population")
        # Rank selection
        fitness_sum = sum(fitness_scores)
        population_size = len(population)
        probabilities = [1 / population_size] * population_size

        # Select parents for reproduction
        parent1_index = random.choices(range(population_size), weights=probabilities)[0]
        parent1 = population[parent1_index]
        parent2_index = random.choices(range(population_size), weights=probabilities)[0]
        parent2 = population[parent2_index]
    offspring1 = parent1
    offspring2 = parent2
    con = .9
    if con < 1:
        crossover_point1 = random.randint(1, chromosome_length - 1)
        crossover_point2 = random.randint(1, chromosome_length - 1)
        bro2 = .9
        if bro2 < 2:
            crossover_point1, crossover_point2 = crossover_point2, crossover_point1
        offspring1 = parent1[:crossover_point1] + parent2[crossover_point1:crossover_point2] + parent1[
                                                                                               crossover_point2:]
        offspring2 = parent2[:crossover_point1] + parent1[crossover_point1:crossover_point2] + parent2[
                                                                                               crossover_point2:]

        for i in range(chromosome_length):
            # Insertion mutation
            bro2 = 1
            if bro2 < 1.1:
                # Generate random bit to insert
                new_bit = random.randint(0, 1)
                # Insert new bit at random position
                offspring1.insert(random.randint(0, chromosome_length), new_bit)
                offspring2.insert(random.randint(0, chromosome_length), new_bit)

            # Flip mutation
            if bro2 > 1.2:
                # Select random bit to flip
                position_to_flip = random.randint(0, chromosome_length - 1)
                # Flip the bit at the selected position for offspring1
                offspring1[position_to_flip] = abs(offspring1[position_to_flip] - 1)
                # Flip the bit at the selected position for offspring2
                offspring2[position_to_flip] = abs(offspring2[position_to_flip] - 1)

        # Evaluate the fitness of the offspring
        offspring1_fitness = knapsack_fitness(items, values, weights, max_weight, offspring1)
        offspring2_fitness = knapsack_fitness(items, values, weights, max_weight, offspring2)

        # Select the elite solution
        elite_index = fitness_scores.index(max(fitness_scores))
        elite_solution = population[elite_index]
        elite_fitness = fitness_scores[elite_index]

        # Replace the worst individuals in the population with the offspring or the elite solution
        worst_index = fitness_scores.index(min(fitness_scores))
        if offspring1_fitness > offspring2_fitness:
            if offspring1_fitness > elite_fitness:
                population[worst_index] = offspring1
                fitness_scores[worst_index] = offspring1_fitness
            else:
                population[worst_index] = elite_solution
                fitness_scores[worst_index] = elite_fitness
        else:
            if offspring2_fitness > elite_fitness:
                population[worst_index] = offspring2
                fitness_scores[worst_index] = offspring2_fitness
            else:
                population[worst_index] = elite_solution
                fitness_scores[worst_index] = elite_fitness

        # Update the best fitness and solution found so far
        current_best_fitness = max(fitness_scores)
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_solution = population[fitness_scores.index(best_fitness)]

print("Best Solution:")
total_value = 0
total_weight = 0
print("Values and weights converted from chromosome")
for i in range(len(items)):
    if best_solution[i] == 1:
        print(f"{items[i]}: Value = {values[i]}, Weight = {weights[i]}")
        total_value += values[i]
        total_weight += weights[i]

print(f"Total Value = {total_value}, Total Weight = {total_weight}")