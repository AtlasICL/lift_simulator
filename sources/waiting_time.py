import time
from lift import Lift
from request_simulator import simulate_requests
from input_parser import parse_config
import random

"""
NOTE:
This file is identical to testing.py, but incoporates the TTSW attribute.
"""

def run_single_simulation(config_file: str) -> dict:
    """
    Run a single simulation and record performance metrics.
    
    Returns a dictionary with:
        - runtime: Total simulation time in seconds.
        - moves: Total number of lift moves executed.
        - visited_floors: List of floors the lift visited.
        - total_requests: Number of requests processed.
        - capacity: The lift capacity used for this run.
        - TTSW: Accumulation of total time spent waiting across all floors.
    """
    config = parse_config(config_file)
    total_floors = config["total_floors"]
    # Randomly vary the capacity between 2 and 15.
    capacity = random.randint(2, 15)
    num_requests = config["num_requests"]

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
    Run the simulation 'runs' times and log the performance metrics to an output file.
    """
    results = []
    for i in range(runs):
        print(f"Running simulation {i+1}/{runs}...")
        result = run_single_simulation(config_file)
        results.append(result)

    # Write results to the output file.
    with open(output_file, "w") as f:
        f.write("Lift Simulation Performance Results\n")
        f.write("=" * 40 + "\n\n")
        for i, result in enumerate(results):
            f.write(f"Simulation {i+1}:\n")
            f.write(f"  Total Floors  : {result['total_floors']}\n")
            f.write(f"  Capacity      : {result['capacity']}\n")
            f.write(f"  Total Requests: {result['total_requests']}\n")
            f.write(f"  TTSW          : {result['ttsw']}\n")
            # f.write(f"  Runtime       : {result['runtime']:.4f} seconds\n")
            f.write("\n")
    
    print(f"Results written to {output_file}")

if __name__ == "__main__":
    CONFIG_FILE: str = "sources/config.json"
    RUNS: int = 50  # Number of simulation runs
    OUTPUT_FILE: str = "results/data/TTSW_vs_capacity_simulation.txt"
    run_multiple_simulations(CONFIG_FILE, RUNS, OUTPUT_FILE)

    