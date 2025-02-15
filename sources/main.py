import time
from lift import Lift
from request_simulator import simulate_requests
from input_parser import parse_config

def run_simulation(config_file: str):
    config = parse_config(config_file)
    total_floors = config["total_floors"]
    capacity = config["capacity"]
    num_requests = config["num_requests"]

    lift = Lift(total_floors, capacity)
    requests = simulate_requests(n_requests=num_requests, max_floor=total_floors)

    print("Generated Requests:")
    for req in requests:
        print(req)
        lift.add_request(req)

    while lift.request_queue.get_requests():
        lift.move()
        print(lift)
        time.sleep(0.5)

    print("FINISHED - ALL REQUESTS SERVED")

if __name__ == "__main__":
    run_simulation("sources/config.json")
