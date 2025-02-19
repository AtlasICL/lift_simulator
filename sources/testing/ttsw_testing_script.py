import time
import csv
import random
from lift import Lift
from request_simulator import simulate_requests
from input_parser import parse_config

"""
NOTE:
This file is identical to testing.py, but incorporates the TTSW attribute.
"""

def run_single_simulation(config_file: str) -> dict:
    """
    Run a single simulation and record performance metrics.
    
    Returns a dictionary with:
        - runtime: Total simulation time in seconds.
        - visited_floors: List of floors the lift visited.
        - total_requests: Number of requests processed.
        - capacity: The lift capacity used for this run.
        - ttsw: Accumulation of total time spent waiting across all floors.
    """
    config = parse_config(config_file)
    total_floors = random.randint(3, 20)
    num_requests = config["num_requests"] 
    # Fix capacity at 5.
    capacity = 5

    # Create a lift instance and generate requests.
    lift = Lift(total_floors, capacity)
    requests = simulate_requests(n_requests=num_requests, max_floor=total_floors)
    for req in requests:
        lift.add_request(req)

    # Run the simulation.
    start_time = time.time()
    move_count = 0
    ttsw = 0
    while lift.request_queue.get_requests() or getattr(lift, "onboard_requests", []):
        lift.move()
        move_count += 1
        ttsw += len(lift.request_queue.get_requests())
    runtime = time.time() - start_time

    return {
        "runtime": runtime,
        "total_floors": total_floors,
        "visited_floors": lift.visited_floors,
        "total_requests": num_requests,
        "capacity": capacity,
        "ttsw": ttsw
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
    fieldnames = ['simulation', 'total_floors', 'capacity', 'total_requests', 'ttsw', 'runtime', 'visited_floors']

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
    RUNS: int = 50  # Number of simulation runs
    OUTPUT_FILE: str = "results/data/TTSW_vs_floors_simulation.csv"
    run_multiple_simulations(CONFIG_FILE, RUNS, OUTPUT_FILE)
