"""
Coin Selection Algorithms for UTXO based Transactions.

This module provides implementations of various coin selection algorithms,
including the Bitcoin Core algorithm, a greedy approach, and a genetic algorithm.
These algorithms aim to optimize transaction fees and selection efficiency.
"""

import secrets, random
from typing import List, Tuple
from app.models.utxo_models import UTXO


def bitcoin_core_coin_selection(utxos: List[UTXO], target: float) -> Tuple[List[UTXO], UTXO]:
    """
    Bitcoin Core's coin selection algorithm.

    Parameters:
        utxos (List[UTXO]): A list of available UTXOs.
        target (float): The target amount to achieve with selected UTXOs.

    Returns:
        Tuple[List[UTXO], UTXO]: A tuple containing the list of selected UTXOs and the change UTXO.
    """
    utxos.sort(key=lambda x: x.value)

    # Step 1: Exact match
    exact_match = next((utxo for utxo in utxos if utxo.value == target), None)
    if exact_match:
        return [exact_match], UTXO(value=0)  # Exact match found, no change needed

    # Step 2: Sum of UTXOs smaller than the target matches the target
    small_utxos = [utxo for utxo in utxos if utxo.value < target]
    total_small_utxos = sum(utxo.value for utxo in small_utxos)
    if total_small_utxos == target:
        return small_utxos, UTXO(value=0)  # Exact match with smaller UTXOs, no change needed

    # Step 3: Use the smallest UTXO greater than the target if sum of small UTXOs is insufficient
    if total_small_utxos < target:
        smallest_larger_utxo = next((utxo for utxo in utxos if utxo.value > target), None)
        if smallest_larger_utxo:
            return [smallest_larger_utxo], UTXO(value=smallest_larger_utxo.value - target)
        else:
            raise ValueError("Insufficient balance to meet target amount")

    # Step 4: Random combinations of UTXOs to find a match
    min_combination = None
    min_combination_value = float('inf')
    for _ in range(1000):
        random.shuffle(utxos)
        combination = []
        combination_value = 0
        for utxo in utxos:
            if combination_value >= target:
                break
            combination.append(utxo)
            combination_value += utxo.value
        if combination_value == target:
            return combination, UTXO(value=0)
        if target <= combination_value < min_combination_value:
            min_combination = combination
            min_combination_value = combination_value

    # Step 5: Settle for the best option
    smallest_larger_utxo = next((utxo for utxo in utxos if utxo.value > target), None)
    if smallest_larger_utxo and min_combination:
        if smallest_larger_utxo.value < min_combination_value:
            return [smallest_larger_utxo], UTXO(value=smallest_larger_utxo.value - target)
    if min_combination:
        change_value = min_combination_value - target
        change_utxo = UTXO(value=change_value) if change_value > 0 else None
        return min_combination, change_utxo

    raise ValueError("Insufficient balance to meet target amount")


def greedy_coin_selection(utxos: List[UTXO], target: float) -> Tuple[List[UTXO], UTXO]:
    """
    Greedy algorithm for coin selection.

    Parameters:
        utxos (List[UTXO]): A list of available UTXOs.
        target (float): The target amount to achieve with selected UTXOs.

    Returns:
        Tuple[List[UTXO], UTXO]: A tuple containing the list of selected UTXOs and the change UTXO.
    """
    sorted_utxos = sorted(utxos, key=lambda x: x.value, reverse=True)
    selected = []
    total_value = 0
    for utxo in sorted_utxos:
        if total_value < target:
            selected.append(utxo)
            total_value += utxo.value
    change = total_value - target if total_value > target else 0
    change_utxo = UTXO(value=change)
    return selected, change_utxo


class Individual:
    """
    Represents an individual in the genetic algorithm with a chromosome.

    Attributes:
        chromosome (List[bool]): A list representing the presence of UTXOs.
        utxos (List[UTXO]): The available UTXOs.
        target (float): The target transaction amount.
        dust_threshold (float): The dynamically calculated dust threshold.
    """
    def __init__(self, chromosome: List[bool], utxos: List[UTXO], target: float, dust_threshold: float):
        """
        Initializes an individual with a chromosome, available UTXOs, and target amount.
        """
        self.chromosome = chromosome
        self.utxos = utxos
        self.target = target
        self.dust_threshold = dust_threshold
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self) -> float:
        """
        Calculates the fitness of the individual based on the total value of selected UTXOs.

        Returns:
            A float representing the fitness score.
        """
        total_value = sum(utxo.value for utxo, selected in zip(self.utxos, self.chromosome) if selected and
                          utxo.value > self.dust_threshold)
        selected_count = sum(1 for utxo, selected in zip(self.utxos, self.chromosome) if selected)

        if total_value < self.target:
            return 0 # Penalty for not reaching the target

        # Fitness function calculation
        return 1 / (self.target - total_value + selected_count)


def initialize_population(utxos: List[UTXO], target: float, dust_threshold: float, population_size: int) -> List[
    Individual]:
    """
    Initializes a population of individuals for the genetic algorithm. The first individual is generated using a greedy
    algorithm, and the remaining population is randomly generated.

    Parameters:
        utxos (List[UTXO]): The list of available UTXOs.
        target (float): The target transaction amount.
        dust_threshold (float): The threshold value to consider a UTXO as dust.
        population_size (int): The size of the population to be generated.

    Returns:
        List[Individual]: A list of initialized individuals.
    """
    # Step 1: Use the greedy_coin_selection function to create the first individual
    selected_utxos, _ = greedy_coin_selection(utxos, target)

    # Create a chromosome based on the selected UTXOs
    chromosome = [utxo in selected_utxos for utxo in utxos]

    # Create the first individual with the greedy-selected UTXOs
    best_individual = Individual(chromosome, utxos, target, dust_threshold)

    # Step 2: Randomly generate the remaining population
    population = [best_individual] + [
        Individual([secrets.randbelow(2) > 0 for _ in utxos], utxos, target, dust_threshold)
        for _ in range(population_size - 1)
    ]

    return population


def select(population: List[Individual]) -> List[Individual]:
    """
    Selects a subset of the population for next generation selection based on fitness.

    Returns:
        List[Individual]: The selected individuals for the next generation.
    """
    if not population:
        raise ValueError("Population cannot be empty.")

    # Calculate total fitness of the population
    f_total = sum(individual.fitness for individual in population)

    # Compute selection probability for each individual
    selection_probs = [individual.fitness / f_total for individual in population]

    # Compute cumulative probability
    cumulative_probs = [sum(selection_probs[:i + 1]) for i in range(len(selection_probs))]

    # Select individuals based on the roulette wheel approach
    selected_individuals = []
    for _ in range(len(population)):
        rand_value = secrets.randbelow(100) / 100.0
        for i, individual in enumerate(population):
            if rand_value <= cumulative_probs[i]:
                selected_individuals.append(individual)
                break

    return selected_individuals


def crossover(parent1: Individual, parent2: Individual, crossover_rate: float) -> Tuple[Individual, Individual]:
    """
    Performs a crossover between two parent individuals to produce offspring.

    Parameters:
        parent1 (Individual): The first individual.
        parent2 (Individual): The second individual.
        crossover_rate_rate (float): The current mutation rate.

    Returns:
        A tuple containing two new Individual objects (the offspring).
    """
    if not 0 <= crossover_rate <= 1:
        raise ValueError("Crossover rate must be between 0 and 1.")

    r = secrets.randbelow(100) / 100.0
    if r < crossover_rate:
        crossover_point = secrets.randbelow(len(parent1.chromosome) - 1) + 1
        child1_chromosome = parent1.chromosome[:crossover_point] + parent2.chromosome[crossover_point:]
        child2_chromosome = parent2.chromosome[:crossover_point] + parent1.chromosome[crossover_point:]
    else:
        child1_chromosome = parent1.chromosome[:]
        child2_chromosome = parent2.chromosome[:]

    return (Individual(child1_chromosome, parent1.utxos, parent1.target, parent1.dust_threshold),
            Individual(child2_chromosome, parent2.utxos, parent2.target, parent2.dust_threshold))


def mutate(individual: Individual, mutation_rate: float, current_generation: int, max_generations: int) -> float:
    """
    Mutates an individual's chromosome based on a given mutation rate.

    Parameters:
        individual (Individual): The individual to mutate.
        mutation_rate (float): The current mutation rate.
        current_generation (int): The current generation number.
        max_generations (int): The total number of generations in the genetic algorithm.

    Returns:
        float: The updated mutation rate for the next generation.
    """
    if not 0 <= mutation_rate <= 1:
        raise ValueError("Mutation rate must be between 0 and 1.")

    r = secrets.randbelow(100) / 100.0
    if r < mutation_rate:
        mutation_position = secrets.randbelow(len(individual.chromosome) - 1)
        individual.chromosome[mutation_position] = not individual.chromosome[mutation_position]

    # Update the mutation rate based on the current generation
    new_mutation_rate = mutation_rate * (1 - 1 / (max_generations + 1 - current_generation))
    return new_mutation_rate


def genetic_coin_selection(utxos: List[UTXO], target: float, dust_threshold: float, population_size: int = 200,
                           generations: int = 2000, crossover_rate: float = 0.5, mutation_rate: float = 0.01) \
        -> Tuple[List[UTXO], UTXO]:
    """
    Executes the genetic algorithm to find an optimal selection of UTXOs.
    Empirical parameters: M = 200 (population size), Pc = 0.5 (crossover prob), Pm = 0.01 (mutation prob), T = 200
    (termination time)

    Parameters:
        utxos (List[UTXO]): A list of available UTXOs.
        target (float): The target amount to achieve with selected UTXOs.
        dust_threshold (float): The threshold value to consider a UTXO as dust.
        population_size (int): The size of the population for the genetic algorithm.
        generations (int): The maximum number of generations.
        mutation_rate (float): The initial mutation rate.

    Returns:
        A tuple of the selected UTXOs and a UTXO representing any change.
    """
    population = initialize_population(utxos, target, dust_threshold, population_size)

    for generation in range(generations):
        population = select(population)
        offspring = []
        for i in range(0, len(population), 2):
            parent1 = population[i]
            parent2 = population[i + 1] if i + 1 < len(population) else population[0]
            child1, child2 = crossover(parent1, parent2, crossover_rate)
            mutation_rate = mutate(child1, mutation_rate, generation, generations)
            mutation_rate = mutate(child2, mutation_rate, generation, generations)
            offspring.extend([child1, child2])
        population = offspring

    best_individual = max(population, key=lambda individual: individual.fitness)
    selected_utxos = [utxo for utxo, selected in zip(best_individual.utxos, best_individual.chromosome) if selected]
    total_value = sum(utxo.value for utxo in selected_utxos)
    change_value = total_value - target
    change_utxo = UTXO(value=change_value)

    return selected_utxos, change_utxo


def execute_coin_selection(utxos: List[UTXO], target: float, dust_threshold: float) -> Tuple[List[UTXO], UTXO]:
    """
       Executes the entire process of coin selection using a combination of Greedy, and Genetic algorithms.
       1. Sorts UTXOs in ascending order.
       2. Checks if the total UTXO value is less than the target, equal to the target, or greater than the target.
       3. If the total is equal to the target, the UTXOs are selected directly.
       4. If UTXOs are greater than the target, the closest to the target is selected.
       5. If neither of the above conditions is met, the Greedy algorithm is used to find a near-optimal solution.
       6. The Genetic algorithm is then applied to find optimal solution.

       Parameters:
           utxos (List[UTXO]): A list of available UTXOs to be considered for the transaction.
           target (float): The target amount for the transaction.
           dust_threshold (float): The threshold below which a UTXO is considered as dust and is not used in fitness calculation.

       Returns:
           Tuple[List[UTXO], UTXO]:
               - A list of selected UTXOs that sum up to the target or as close as possible.
               - A UTXO representing the change amount, if any.

       Raises:
           ValueError: If the UTXOs cannot meet the target amount.
       """
    # Step S1: Exact match
    exact_match = next((utxo for utxo in utxos if utxo.value == target), None)
    if exact_match:
        return [exact_match], UTXO(value=0)  # Exact match found, no change needed

    # Step S2: Sort UTXOs in ascending order
    utxos.sort(key=lambda x: x.value)

    # Step S3: Calculate the total balance of UTXOs
    total_balance = sum(utxo.value for utxo in utxos)

    # Step S4: Check if the total balance is less than the target
    if total_balance < target:
        raise ValueError("Insufficient balance to meet target amount")

    # Step S5: Check if the total balance equals the target
    if total_balance == target:
        return utxos, UTXO(value=0)  # Exact match, no change needed

    # Step S6: Sum of UTXOs smaller than the target matches the target
    small_utxos = [utxo for utxo in utxos if utxo.value < target]
    total_small_utxos = sum(utxo.value for utxo in small_utxos)
    if total_small_utxos == target:
        return small_utxos, UTXO(value=0)  # Exact match with smaller UTXOs, no change needed

    # Step S7: Random combinations of UTXOs to find a match
    min_combination_value = float('inf')
    for _ in range(2000):
        random.shuffle(utxos)
        combination = []
        combination_value = 0
        for utxo in utxos:
            if combination_value >= target:
                break
            combination.append(utxo)
            combination_value += utxo.value
        if combination_value == target:
            return combination, UTXO(value=0)
        if target <= combination_value < min_combination_value:
            min_combination_value = combination_value

    # Step S8: Check if there's a UTXO larger than the target
    largest_utxo = next((utxo for utxo in utxos if utxo.value >= target), None)
    if largest_utxo:
        return [largest_utxo], UTXO(value=largest_utxo.value - target)  # Use the closest larger UTXO

    # Step S9: Apply the Greedy and Genetic algorithms to refine the selection
    selected_utxos, change_utxo = genetic_coin_selection(utxos, target, dust_threshold)

    return selected_utxos, change_utxo
