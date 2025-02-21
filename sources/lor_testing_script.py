import time
import csv
import random
from lift import Lift
from request_simulator import simulate_requests
from input_parser import parse_config

"""
NOTE:
This file is identical to testing.py, but incorporates the LOR attribute.
"""

def run_single_simulation(config_file: str) -> dict:
    """
    Run a single simulation and record performance metrics.
    
    Returns a dictionary with:
        - visited_floors: List of floors the lift visited.
        - total_requests: Number of requests processed.
        - capacity: The lift capacity used for this run.
        - ttsw: Accumulation of total time spent waiting across all floors.
        - lor: Ratio of how full the lift is at each time period of a single simulation.
    """
    config = parse_config(config_file)
    # These two parameters kept constant.
    num_requests = config["num_requests"]
    capacity = 20
    # Vary number of floors.
    total_floors = random.randint(3, 20)
    

    # Create a lift instance and generate requests.
    lift = Lift(total_floors, capacity)
    requests = simulate_requests(n_requests=num_requests, max_floor=total_floors)
    for req in requests:
        lift.add_request(req)

    # Run the simulation.
    move_count = 0
    lor = []
    while lift.request_queue.get_requests() or getattr(lift, "onboard_requests", []):
        # Each list index of lor corresponds to the time instance at which that value of lor was recorded.
        lor.append(float(len(lift.onboard_requests) / capacity))
        lift.move()
        move_count += 1

    return {
        "total_floors": total_floors,
        "visited_floors": lift.visited_floors,
        "total_requests": num_requests,
        "capacity": capacity,
        "lor": lor
    }

def run_multiple_simulations(config_file: str, runs: int, output_file: str) -> None:
    """
    Run the simulation 'runs' times and log the performance metrics to an output CSV file.
    """
    results = []
    for i in range(runs):
        print(f"Running simulation {i+1}/{runs}...")
        result = run_single_simulation(config_file)
        # Add simulation number to the result.
        result['simulation'] = i + 1
        results.append(result)

    # Define CSV columns.
    fieldnames = ['simulation', 'total_floors', 'capacity', 'total_requests', 'lor', 'visited_floors']

    # Write the results to a CSV file.
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            # Convert visited_floors to string to ensure proper CSV formatting.
            result['visited_floors'] = str(result['visited_floors'])
            writer.writerow(result)
    
    print(f"Results written to {output_file}")

if __name__ == "__main__":
    CONFIG_FILE: str = "sources/config.json"
    RUNS: int = 10  # Number of simulation runs
    OUTPUT_FILE: str = "results/data/lor_vs_floors.csv"
    run_multiple_simulations(CONFIG_FILE, RUNS, OUTPUT_FILE)
