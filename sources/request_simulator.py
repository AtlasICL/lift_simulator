import random

from request import Request

def generate_random_requests(n_requests: int, max_floor: int) -> list[Request]:
    """
    Function to generate random pairs, to simulate requests.
    """
    requests = []
    for _ in range(n_requests):
        # prevent start_floor == end_floor in generation:
        start_floor = random.randint(0, max_floor-1)
        end_floor = random.randint(0, max_floor-1)

        while end_floor == start_floor:
            end_floor = random.randint(0, max_floor-1)
        
        req = Request(start_floor, end_floor)
        requests.append(req)
    return requests