import random

from request import Request

def simulate_requests(n_requests: int, max_floor: int) -> list[Request]:
    """Generate random requests with floors between 1 and max_floor."""
    requests = []
    for _ in range(n_requests):
        start_floor = random.randint(1, max_floor)
        end_floor = random.randint(1, max_floor)

        # Ensure start and end are different.
        while end_floor == start_floor:
            end_floor = random.randint(1, max_floor)
        
        req = Request(start_floor, end_floor)
        requests.append(req)
    return requests
