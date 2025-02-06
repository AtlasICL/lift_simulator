import random

from request import Request

def generate_random_requests(n_requests: int, max_floor: int, seed: int = None) -> list[Request]:
    requests = []
    for _ in range(n_requests):
        # prevent start_floor == end_floor in generation:
        start_floor = random.randint(1, max_floor)
        end_floor = start_floor

        while end_floor == start_floor:
            end_floor = random.randint(1, max_floor)
        
        req = Request(start_floor, end_floor)
        requests.append(req)
    return requests