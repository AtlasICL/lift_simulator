from request import Request

class ReqQueue:
    """
    Queue class, which stores the queue of requests for a particular instance of a lift.

    Attributes:
        - requests: list of requests, each of which is an instance of 'Request' class.
    
    Methods:
        - add_request: add a request to the queue
        - remove_request: remove a request from the queue
        NOTE: we need to make sure we remove every visited combination, i.e. if lift stops at 2, 4, 5, 8, then we need to remove:
        (2, 4), (2, 5), (2, 8), (4, 5), (4, 8), (5, 8)
    """
    requests: list[Request]

    def __init__(self):
        self.requests = []

    def get_requests(self) -> list[Request]:
        return self.requests

    def add_request(self, req: Request) -> None:
        self.requests.append(req)

    def remove_request(self, req: Request) -> None:
        self.requests.remove(req)

    def remove_duplicate_requests(self) -> None:
        """
        Removes exact duplicates (start=floorA, end=floorB) from the queue.
        After this, self.requests contains only unique start/end combinations.
        """
        unique_requests = []
        seen_pairs = set()
        for req in self.requests:
            pair = (req.origin_floor, req.destination_floor)
            if pair not in seen_pairs:
                unique_requests.append(req)
                seen_pairs.add(pair)
        self.requests = unique_requests

    def remove_visited_combinations(self, visited_floors: list[int]) -> None:
        """
        Remove all requests whose start and end floors are within the visited floors.
        For instance, if visited_floors = [2, 4, 5, 8], remove any request where
        (start, end) is one of (2,4), (2,5), (2,8), (4,5), (4,8), (5,8).
        (using the same example as earlier)
        """
        visited_floors = sorted(visited_floors) # sorting in ascending order
        visited_pairs = set()

        # Generate all pairs of visited floors
        for i in range(len(visited_floors)):
            for j in range(i + 1, len(visited_floors)):
                visited_pairs.add((visited_floors[i], visited_floors[j]))

        self.requests = [req for req in self.requests if (req.origin_floor, req.destination_floor) not in visited_pairs]



    