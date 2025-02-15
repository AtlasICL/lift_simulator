from request import Request

class ReqQueue:
    """
    Queue class, which stores the queue of requests for a particular instance of a lift.
    
    Attributes:
        - requests: list of requests, each of which is an instance of the 'Request' class.
    
    Methods:
        - add_request: add a request to the queue.
        - remove_request: remove a specific request from the queue.
        - remove_duplicate_requests: remove duplicate requests (same origin and destination).
        - remove_served_requests: remove any requests that have been effectively served by the lift.
          For example, if the lift stops at floors 2, 4, 5, 8, then remove any request with
          (2,4), (2,5), (2,8), (4,5), (4,8), or (5,8).
    """
    requests: list[Request]

    def __init__(self):
        self.requests = []

    def get_requests(self) -> list[Request]:
        return self.requests

    def add_request(self, req: Request) -> None:
        self.requests.append(req)

    def remove_request(self, req: Request) -> None:
        if req in self.requests:
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

    def remove_served_requests(self, visited_floors: list[int]) -> None:
        # build a new list of requests that are still pending.
        pending_requests = []
        for req in self.requests:
            if req.origin_floor in visited_floors and req.destination_floor in visited_floors:
                # Determine the order in which the floors were visited.
                origin_index = visited_floors.index(req.origin_floor)
                dest_index = visited_floors.index(req.destination_floor)
                # If the origin comes before the destination, the request is considered served.
                if origin_index < dest_index:
                    continue  # Skip adding this request, as it's been served.
            # Otherwise, keep the request.
            pending_requests.append(req)
        self.requests = pending_requests

    def __repr__(self) -> str:
        return f"ReqQueue({self.requests})"
