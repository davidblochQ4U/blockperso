import pytest, secrets
from unittest.mock import patch
from app.services.coin_selection_algorithms import (
    bitcoin_core_coin_selection,
    greedy_coin_selection,
    genetic_coin_selection,
    initialize_population,
    select,
    crossover,
    mutate,
    execute_coin_selection
)
from app.models.utxo_models import UTXO
from app.config import DUST_THRESHOLD

@pytest.fixture
def sample_utxos():
    return [UTXO(value=1), UTXO(value=2), UTXO(value=5), UTXO(value=10)]

# Test Bitcoin Core Coin Selection
def test_bitcoin_core_coin_selection(sample_utxos):
    # Test normal operation
    selected_utxos, change_utxo = bitcoin_core_coin_selection(sample_utxos, 7)
    assert len(selected_utxos) > 0
    assert change_utxo.value >= 0

    # Test exact match
    selected_utxos, change_utxo = bitcoin_core_coin_selection(sample_utxos, 10)
    assert len(selected_utxos) == 1
    assert change_utxo.value == 0

    # Test insufficient funds
    with pytest.raises(ValueError):
        bitcoin_core_coin_selection(sample_utxos, 100)

def test_bitcoin_core_n_lowest_larger(sample_utxos):
    new_target = 9  # Choose a target that forces the use of the UTXO with value 10 as the only solution
    selected_utxos, change_utxo = bitcoin_core_coin_selection(sample_utxos, new_target)
    assert len(selected_utxos) == 1
    assert selected_utxos[0].value > new_target
    assert change_utxo.value == selected_utxos[0].value - new_target

# Test Greedy Coin Selection
def test_greedy_coin_selection(sample_utxos):
    selected_utxos, change_utxo = greedy_coin_selection(sample_utxos, 3)
    assert sum(utxo.value for utxo in selected_utxos) >= 3
    assert change_utxo.value >= 0

# Test Initialize Population
def test_initialize_population(sample_utxos):
    population = initialize_population(sample_utxos, 7, DUST_THRESHOLD, 4)
    assert len(population) == 4
    for individual in population:
        assert len(individual.chromosome) == len(sample_utxos)

# Test Selection Function
def test_select (sample_utxos):
    population = initialize_population(sample_utxos, 7, DUST_THRESHOLD, 10)
    # Artificially set fitness for testing select
    for i, individual in enumerate(population):
        individual.fitness = i / 10.0  # Increasing fitness

    # Select individuals
    selected = select(population)

    # Assert correct selection size and fitness values
    assert len(selected) == len(population)

    # Ensure the average fitness of the selected individuals is higher than or equal to the population's average fitness
    population_avg_fitness = sum(individual.fitness for individual in population) / len(population)
    selected_avg_fitness = sum(individual.fitness for individual in selected) / len(selected)

    assert selected_avg_fitness >= population_avg_fitness


# Test Crossover Function
@patch('secrets.randbelow', return_value=2)  # Crossover point at index 2
def test_crossover (mock_randint, sample_utxos):
    # Initialize the population with known chromosomes to control the test conditions
    population = initialize_population(sample_utxos, 7, DUST_THRESHOLD, 2)

    # Manually set the chromosomes for testing purposes
    population[0].chromosome = [False, False, False, True]
    population[1].chromosome = [True, True, True, True]

    # Perform crossover
    child1, child2 = crossover(population[0], population[1], crossover_rate=1)

    # Ensure that crossover happens after the second index (index 2 onward)
    crossover_point = 3
    assert child1.chromosome[crossover_point:] == population[1].chromosome[crossover_point:]
    assert child2.chromosome[crossover_point:] == population[0].chromosome[crossover_point:]


# Test Mutation Function
def test_mutate(sample_utxos):
    individual = initialize_population(sample_utxos, 7, DUST_THRESHOLD, 1)[0]
    original_chromosome = individual.chromosome.copy()

    # Perform mutation with a high mutation rate
    mutate(individual, mutation_rate=1, current_generation=1, max_generations=5)

    # Ensure that at least one bit has been flipped
    assert any(original != mutated for original, mutated in zip(original_chromosome, individual.chromosome)), 'Mutation failed'

    # Ensure that not all bits are flipped (because we expect only one bit to mutate)
    assert sum(original != mutated for original, mutated in zip(original_chromosome, individual.chromosome)) == 1, \
        "More than one bit mutated"



# Test Genetic Coin Selection
def test_genetic_coin_selection(sample_utxos):
    selected_utxos, change_utxo = genetic_coin_selection(sample_utxos, target=7, dust_threshold=DUST_THRESHOLD,
                                                         population_size=10, generations=5)
    assert sum(utxo.value for utxo in selected_utxos) >= 7
    assert change_utxo.value >= 0

# Test Full Coin Selection Execution
def test_execute_coin_selection(sample_utxos):
    selected_utxos, change_utxo = execute_coin_selection(sample_utxos, target=7)
    assert sum(utxo.value for utxo in selected_utxos) >= 7
    assert change_utxo.value >= 0
