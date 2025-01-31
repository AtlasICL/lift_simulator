from queue import Queue

class Lift:
    """
    Lift class. Represents one particular lift. 

    Attributes:
        current_position: int - indicates the current floor of the lift.
        num_floors: int - indicates the number of floors served by the lift.
        queue: Queue - stores the queue of requests for the lift.

    Methods:
        constructor
        find_next_destination
        move

    """

    current_position: int
    num_floors: int
    queue: Queue

    pass

