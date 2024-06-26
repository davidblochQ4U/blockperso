"""
Coin Selection Algorithms for UTXO based Transactions.

This module provides implementations of various coin selection algorithms,
including the Bitcoin Core algorithm, a greedy approach, and a genetic algorithm.
These algorithms aim to optimize transaction fees and selection efficiency.
"""


import secrets
from typing import List, Tuple
from utxo_models import UTXO

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
    n_total_lower = sum(utxo.value for utxo in utxos if utxo.value < target)
    n_lowest_larger = next((utxo for utxo in reversed(utxos) if utxo.value > target), None)
    exact_match = next((utxo for utxo in utxos if utxo.value == target), None)

    if exact_match:
        return [exact_match], UTXO(value=0)  # Exact match found, no change needed

    if n_total_lower < target:
        if n_lowest_larger:
            return [n_lowest_larger], UTXO(value=n_lowest_larger.value - target)  # Use the UTXO just larger than target
        else:
            raise ValueError("Insufficient balance to meet target amount")

    selected_utxos = []
    for _ in range(50):  # Random approximation attempts
        # This is a simplified version, actual implementation should randomly select UTXOs
        selected_utxos = [utxo for utxo in utxos if utxo.value < target]  # Placeholder for random selection logic
        if sum(utxo.value for utxo in selected_utxos) >= target:
            break

    change_value = sum(utxo.value for utxo in selected_utxos) - target
    change_utxo = UTXO(value=change_value) if change_value > 0 else None

    return selected_utxos, change_utxo


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
        fitness (float): The fitness score of the individual.
    """
    def __init__(self, chromosome: List[bool], utxos: List[UTXO], target: float):
        """
        Initializes an individual with a chromosome, available UTXOs, and target amount.
        """
        self.chromosome = chromosome
        self.utxos = utxos
        self.target = target
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self) -> float:
        """
        Calculates the fitness of the individual based on the total value of selected UTXOs.

        Returns:
            A float representing the fitness score.
        """
        total_value = sum(utxo.value for utxo, selected in zip(self.utxos, self.chromosome) if selected)
        if total_value < self.target:
            return 0
        return 1 / (1 + total_value - self.target)

def initialize_population(utxos: List[UTXO], target: float, population_size: int) -> List[Individual]:
    """
    Initializes a population of individuals for the genetic algorithm.

    Returns:
        A list of Individual objects representing the initial population.
    """
    return [Individual([secrets.randbelow(2) > 0 for _ in utxos], utxos, target) for _ in range(population_size)]

def select(population: List[Individual]) -> List[Individual]:
    """
    Selects a subset of the population based on fitness to survive to the next generation.

    Returns:
        A list of Individual objects that survived.
    """
    population.sort(key=lambda individual: individual.fitness, reverse=True)
    survivors = population[:len(population) // 2]

    # Securely sample half of the population without replacement
    sampled_indices = set()
    while len(sampled_indices) < len(population) // 2:
        index = secrets.randbelow(len(population))
        sampled_indices.add(index)

    sampled_population = [population[i] for i in sampled_indices]
    return survivors + sampled_population

def crossover(parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
    """
    Performs a crossover between two parent individuals to produce offspring.

    Returns:
        A tuple containing two new Individual objects (the offspring).
    """
    crossover_point = secrets.randbelow(len(parent1.chromosome) - 1) + 1
    child1_chromosome = parent1.chromosome[:crossover_point] + parent2.chromosome[crossover_point:]
    child2_chromosome = parent2.chromosome[:crossover_point] + parent1.chromosome[crossover_point:]
    return (Individual(child1_chromosome, parent1.utxos, parent1.target),
            Individual(child2_chromosome, parent2.utxos, parent2.target))

def mutate(individual: Individual, mutation_rate: float = 0.01) -> None:
    """
    Mutates an individual's chromosome based on a given mutation rate.

    Parameters:
        individual (Individual): The individual to mutate.
        mutation_rate (float): The probability of any given gene mutating.
    """
    for i in range(len(individual.chromosome)):
        if secrets.randbelow(100) / 100.0 < mutation_rate:
            individual.chromosome[i] = not individual.chromosome[i]


def genetic_coin_selection(utxos: List[UTXO], target: float, population_size: int = 100, generations: int = 100,
                           mutation_rate: float = 0.01) -> Tuple[List[UTXO], UTXO]:
    """
    Executes the genetic algorithm to find an optimal selection of UTXOs.

    Returns:
        A tuple of the selected UTXOs and a UTXO representing any change.
    """
    population = initialize_population(utxos, target, population_size)
    for _ in range(generations):
        selected = select(population)
        offspring = []
        for i in range(0, len(selected), 2):
            child1, child2 = crossover(selected[i], selected[min(i + 1, len(selected) - 1)])
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            offspring.extend([child1, child2])
        population = offspring

    best_individual = max(population, key=lambda individual: individual.fitness)
    selected_utxos = [utxo for utxo, selected in zip(best_individual.utxos, best_individual.chromosome) if selected]
    total_value = sum(utxo.value for utxo in selected_utxos)

    change_value = total_value - target
    change_utxo = UTXO(value=change_value)

    return selected_utxos, change_utxo