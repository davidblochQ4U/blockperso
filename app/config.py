# app/config.py

# Transaction Parameters
DUST_THRESHOLD = 0.00000546 # in BTC
FEE_RATE = 20  # satoshis per byte
# Average sizes in bytes for transaction components
INPUT_SIZE = 148  # bytes
OUTPUT_SIZE = 34  # bytes
BASE_SIZE = 10  # bytes

# Genetic Algorithm parameters
GA_POPULATION_SIZE = 200
GA_CROSSOVER_PROB = 0.5
GA_MUTATION_PROB = 0.01
GA_TERMINATION_GEN = 200
