import json

import lift
from request import Request # not used currently
from request_simulator import generate_random_requests


CONFIG_FILENAME: str = "config.json"

def read_config(filename: str = CONFIG_FILENAME) -> int:
    with open('sources/config.json', 'r') as f:
        data = json.load(f)
        return (data["floors"])


def main():

    MAX_FLOOR: int = read_config() - 1 # we are starting from floor 0, hence the - 1

    random_requests = generate_random_requests(n_requests=10, max_floor=MAX_FLOOR)
    
    Lift = lift.Lift()

    for req in random_requests:
        Lift.queue.add_request(req)

    Lift.print()



if __name__ == "__main__":
    main()


