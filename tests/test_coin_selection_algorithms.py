import pytest
from unittest.mock import patch
from coin_selection_algorithms import (
    bitcoin_core_coin_selection,
    greedy_coin_selection,
    genetic_coin_selection,
    initialize_population,
    select,
    crossover,
    mutate
)
from utxo_models import UTXO

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
    new_target = 11  # Choose a target that forces the use of the UTXO with value 10 as the only solution
    selected_utxos, change_utxo = bitcoin_core_coin_selection(sample_utxos, new_target)
    assert len(selected_utxos) == 1
    assert selected_utxos[0].value > new_target
    assert change_utxo.value == selected_utxos[0].value - new_target

# Test Greedy Coin Selection
def test_greedy_coin_selection(sample_utxos):
    selected_utxos, change_utxo = greedy_coin_selection(sample_utxos, 3)
    assert sum(utxo.value for utxo in selected_utxos) >= 3
    assert change_utxo.value >= 0

# Test Genetic Coin Selection Functions
def test_initialize_population(sample_utxos):
    population = initialize_population(sample_utxos, 7, 4)
    assert len(population) == 4
    for individual in population:
        assert len(individual.chromosome) == len(sample_utxos)

def test_select(sample_utxos):
    # Given a mock population
    population = initialize_population(sample_utxos, 7, 10)
    # Artificially set fitness for testing select
    for i, individual in enumerate(population):
        individual.fitness = i / 10.0  # Increasing fitness
    selected = select(population)
    assert len(selected) == len(population)
    # Assert that individuals with higher fitness are selected
    assert all(individual.fitness >= 0.5 for individual in selected[:len(population)//2])

@patch('random.randint', return_value=2)
def test_crossover(mock_randint, sample_utxos):
    population = initialize_population(sample_utxos, 7, 2)
    child1, child2 = crossover(population[0], population[1])
    # Check if crossover occurred at mocked index
    assert child1.chromosome[2:] == population[1].chromosome[2:]
    assert child2.chromosome[2:] == population[0].chromosome[2:]

@patch('random.random', side_effect=[0.01, 0.99, 0.01, 0.99])
def test_mutate(sample_utxos):
    individual = initialize_population(sample_utxos, 7, 1)[0]
    original_chromosome = individual.chromosome.copy()
    # Call mutate without trying to control the randomness
    mutate(individual, mutation_rate=1)  # Set high to ensure mutation
    # Check that at least one gene has been mutated
    assert individual.chromosome != original_chromosome


# Test the full genetic coin selection algorithm
def test_genetic_coin_selection(sample_utxos):
    selected_utxos, change_utxo = genetic_coin_selection(sample_utxos, target=7, population_size=10, generations=5)
    assert sum(utxo.value for utxo in selected_utxos) >= 7
    assert change_utxo.value >= 0