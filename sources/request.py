class Request:
    """
    Request class denotes an individual lift request.
    In our simulation, a request indicates a call to the lift from an origin floor to a destination floor.
    """

    def __init__(self, origin: int, destination: int, total_floors: int):
        self.NUM_FLOORS = total_floors
        if not self.is_valid_request(origin, destination):
            raise ValueError(
                f"Invalid request: {origin} -> {destination} (must be within 1 and {total_floors} and not equal)"
            )
        self.origin_floor = origin
        self.destination_floor = destination
        self.picked_up = False 

    def is_valid_request(self, origin_floor: int, destination_floor: int) -> bool:
        if origin_floor < 1 or destination_floor < 1:
            return False
        if origin_floor > self.NUM_FLOORS or destination_floor > self.NUM_FLOORS:
            return False
        if origin_floor == destination_floor:
            return False
        return True

    def is_upward(self) -> bool:
        return self.destination_floor > self.origin_floor

    def is_downward(self) -> bool:
        return self.destination_floor < self.origin_floor

    def __repr__(self) -> str:
        status = "picked up" if self.picked_up else "waiting"
        return f"Request({self.origin_floor} -> {self.destination_floor}, {status})"
