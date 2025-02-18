import time
from lift import Lift
from request_simulator import simulate_requests
from input_parser import parse_config
import random

"""
NOTE:
This file serves as an alternate entry point.
Run this script to generate simulation output while varying the number of floors.
"""

def run_single_simulation(config_file: str) -> dict:
    """
    Run a single simulation and record performance metrics.

    Returns a dictionary with:
        - runtime: Total simulation time in seconds.
        - moves: Total number of lift moves executed.
        - visited_floors: List of floors the lift visited.
        - total_requests: Number of requests processed.
        - capacity: The fixed lift capacity (5).
        - total_floors: The number of floors used for this run.
    """
    config = parse_config(config_file)
    
    # Vary the number of floors randomly; for example, between 5 and 20.
    total_floors = random.randint(5, 20)
    
    # Fixed capacity and number of requests.
    capacity = 5
    num_requests = config["num_requests"]

    # Create a lift instance and generate requests.
    lift = Lift(total_floors, capacity)
    requests = simulate_requests(n_requests=num_requests, max_floor=total_floors)
    for req in requests:
        lift.add_request(req)

    # Run the simulation.
    start_time = time.time()
    move_count = 0
    while lift.request_queue.get_requests() or getattr(lift, "onboard_requests", []):
        lift.move()
        move_count += 1
    runtime = time.time() - start_time

    return {
        "runtime": runtime,
        "moves": move_count,
        "visited_floors": lift.visited_floors,
        "total_requests": num_requests,
        "capacity": capacity,
        "total_floors": total_floors,
    }

def run_multiple_simulations(config_file: str, runs: int, output_file: str) -> None:
    """
    Run the simulation 'runs' times and log performance metrics to an output file.
    """
    results = []
    for i in range(runs):
        print(f"Running simulation {i+1}/{runs}...")
        result = run_single_simulation(config_file)
        results.append(result)

    # Write results to the output file.
    with open(output_file, "w") as f:
        f.write("Lift Simulation Performance Results (Fixed Capacity & Requests, Varying Floors)\n")
        f.write("=" * 80 + "\n\n")
        for i, result in enumerate(results):
            f.write(f"Simulation {i+1}:\n")
            f.write(f"  Total Floors  : {result['total_floors']}\n")
            f.write(f"  Capacity      : {result['capacity']}\n")
            f.write(f"  Total Requests: {result['total_requests']}\n")
            f.write(f"  Moves         : {result['moves']}\n")
            f.write(f"  Runtime       : {result['runtime']:.4f} seconds\n")
            f.write("\n")
    
    print(f"Results written to {output_file}")

if __name__ == "__main__":
    CONFIG_FILE: str = "sources/config.json"
    RUNS: int = 30  # Number of simulation runs
    OUTPUT_FILE: str = "results/data/simulation_results_FLOORS_VAR.txt"
    run_multiple_simulations(CONFIG_FILE, RUNS, OUTPUT_FILE)
