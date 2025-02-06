class Request:
    """
    Request class denotes an individual request. A request is someone calling the lift.
    In our simulation, someone calling the lift indicates which floor they would like to go to.

    Attributes:
        current_floor: int
        destination: int

    Methods:
        constructor: instantiates an instance of a request class with the specified origin floor and destination floor.

    The request class is responsible for ensuring that a given request is valid, implemented at the constructor level.
    Explanation: a request to go from floor 1 to floor 1 is not valid, as well as any requests not within the bounds
    of the number of floors in the building as initially specified.
    
    """
    
    origin_floor: int
    destination_floor: int

    def __init__(self, origin: int, destination: int):
        self.origin_floor = origin
        self.destination_floor = destination

    def print(self) -> None:
        print(f"REQ | o: {self.origin_floor}; d: {self.destination_floor}")
    