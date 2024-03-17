import random
from typing import List, Tuple
from utxo_models import UTXO

def bitcoin_core_coin_selection(utxos: List[UTXO], target: float) -> Tuple[List[UTXO], UTXO]:
    utxos.sort(key=lambda x: x.value)
    nTotalLower = sum(utxo.value for utxo in utxos if utxo.value < target)
    nLowestLarger = next((utxo for utxo in reversed(utxos) if utxo.value > target), None)
    exact_match = next((utxo for utxo in utxos if utxo.value == target), None)

    if exact_match:
        return [exact_match], UTXO(value=0)  # Exact match found, no change needed

    if nTotalLower < target:
        if nLowestLarger:
            return [nLowestLarger], UTXO(value=nLowestLarger.value - target)  # Use the UTXO just larger than target
        else:
            raise ValueError("Insufficient balance to meet target amount")

    selected_utxos = []
    for _ in range(50):  # Random approximation attempts
        # This is a simplified version, actual implementation should randomly select UTXOs
        selected_utxos = [utxo for utxo in utxos if utxo.value < target]  # Placeholder for random selection logic
        if sum(utxo.value for utxo in selected_utxos) >= target:
            break

    if not selected_utxos or sum(utxo.value for utxo in selected_utxos) < target:
        raise ValueError("Failed to find a suitable combination of UTXOs")

    change_value = sum(utxo.value for utxo in selected_utxos) - target
    change_utxo = UTXO(value=change_value) if change_value > 0 else None

    return selected_utxos, change_utxo


def greedy_coin_selection(utxos: List[UTXO], target: float) -> Tuple[List[UTXO], UTXO]:
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
    def __init__(self, chromosome: List[bool], utxos: List[UTXO], target: float):
        self.chromosome = chromosome
        self.utxos = utxos
        self.target = target
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self) -> float:
        total_value = sum(utxo.value for utxo, selected in zip(self.utxos, self.chromosome) if selected)
        if total_value < self.target:
            return 0
        return 1 / (1 + total_value - self.target)

def initialize_population(utxos: List[UTXO], target: float, population_size: int) -> List[Individual]:
    return [Individual([random.choice([True, False]) for _ in utxos], utxos, target) for _ in range(population_size)]

def select(population: List[Individual]) -> List[Individual]:
    population.sort(key=lambda individual: individual.fitness, reverse=True)
    survivors = population[:len(population) // 2]
    return survivors + random.sample(population, len(population) // 2)

def crossover(parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
    crossover_point = random.randint(1, len(parent1.chromosome) - 2)
    child1_chromosome = parent1.chromosome[:crossover_point] + parent2.chromosome[crossover_point:]
    child2_chromosome = parent2.chromosome[:crossover_point] + parent1.chromosome[crossover_point:]
    return (Individual(child1_chromosome, parent1.utxos, parent1.target),
            Individual(child2_chromosome, parent2.utxos, parent2.target))

def mutate(individual: Individual, mutation_rate: float = 0.01) -> None:
    for i in range(len(individual.chromosome)):
        if random.random() < mutation_rate:
            individual.chromosome[i] = not individual.chromosome[i]


def genetic_coin_selection(utxos: List[UTXO], target: float, population_size: int = 100, generations: int = 100,
                           mutation_rate: float = 0.01) -> Tuple[List[UTXO], UTXO]:
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
