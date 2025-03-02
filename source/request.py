class Request:
    """
    Request class denotes an individual lift request.
    In our simulation, a request indicates a call to the lift from an origin floor to a destination floor.
    """

    def __init__(self, origin: int, destination: int):
        self.origin_floor = origin
        self.destination_floor = destination
        self.picked_up = False 

    def is_upward(self) -> bool:
        return self.destination_floor > self.origin_floor

    def is_downward(self) -> bool:
        return self.destination_floor < self.origin_floor

    def __repr__(self) -> str:
        """Function for printing to the console."""
        status = "picked up" if self.picked_up else "waiting"
        return f"Request({self.origin_floor} -> {self.destination_floor}, {status})"
