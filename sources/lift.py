from queue import Queue
from request import Request

class Lift:
    """
    Lift class. Represents one instance of a lift. 

    Attributes:
        current_position: int - indicates the current floor of the lift.
        num_floors: int - indicates the number of floors served by the lift.
        queue: Queue - stores the queue of requests for the lift.

    Methods:
        constructor
        find_next_destination
        move
    """

    NUMBER_OF_FLOORS: int
    current_position: int
    destination: int
    queue: Queue

    def __init__(self):
        self.current_position = 0
        self.destination = 0
        self.queue = Queue()


    def print(self) -> None:
        """
        debugging function
        prints current info about lift instance
        """
        print("--LIFT--")
        print(f"FLOOR: {self.current_position}")
        print(f"QUEUE OF REQS: {self.queue}")
        for request in self.queue.get_requests():
            request.print()
        print("--------")



    pass

