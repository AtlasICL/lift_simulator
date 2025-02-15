from req_queue import ReqQueue
from request import Request
import time

class Lift:
    """
    Lift class that simulates the behavior of an elevator.
    
    Attributes:
        current_floor (int): The floor where the lift is currently located.
        total_floors (int): The total number of floors in the building.
        capacity (int): Maximum number of requests (or passengers) the lift can handle at once.
        request_queue (ReqQueue): A custom queue storing the lift's requests.
        direction (str | None): The current direction of the lift ("up", "down", or None when idle).
        visited_floors (list[int]): Tracks floors that the lift has visited.
    
    Methods:
        add_request: Adds a new request to the queue.
        next_stop: Determines the next floor to move to based on the pending requests.
        move: Moves the lift one floor at a time towards the next stop and handles arrival logic.
    """
    def __init__(self, total_floors: int, capacity: int):
        self.current_floor = 1          # Start at floor 1
        self.total_floors = total_floors
        self.capacity = capacity
        self.request_queue = ReqQueue()
        self.direction = None           # "up", "down", or None when idle
        self.visited_floors = []        # Keep track of floors the lift has stopped at

    def add_request(self, req: Request) -> None:
        """Add a new request to the lift's queue."""
        self.request_queue.add_request(req)
    
    def next_stop(self) -> int | None:
        """
        Decide the next stop based on the queued requests.
        
        Strategy:
            - If the lift is not at the request's origin floor, head there.
            - If already at the origin, move to the destination floor.
        Returns:
            The floor number of the next stop, or None if no requests are pending.
        """
        if not self.request_queue.get_requests():
            return None

        # Always look at the first request in the queue.
        req = self.request_queue.get_requests()[0]
        
        # If the request has not been picked up, head to its origin.
        if not req.picked_up:
            return req.origin_floor
        else:
            # If already picked up, head to its destination.
            return req.destination_floor

    def move(self) -> None:
        next_stop = self.next_stop()
        if next_stop is None:
            print("No pending requests. Lift is idle.")
            return

        # Move one floor toward next_stop.
        if self.current_floor < next_stop:
            self.current_floor += 1
            self.direction = "up"
        elif self.current_floor > next_stop:
            self.current_floor -= 1
            self.direction = "down"

        print(f"Moving {self.direction} to floor {self.current_floor}")

        # Check if we've arrived at our intended stop.
        if self.current_floor == next_stop:
            self.visited_floors.append(self.current_floor)
            print(f"Arrived at floor {self.current_floor}")

            # Get the first request (which determined our next stop).
            req = self.request_queue.get_requests()[0]
            
            if not req.picked_up and self.current_floor == req.origin_floor:
                req.picked_up = True
                print(f"Picked up request: {req}")
            elif req.picked_up and self.current_floor == req.destination_floor:
                print(f"Served: {req}")
                self.request_queue.remove_request(req)
            
            # Optional: Clear direction if no more requests.
            if not self.request_queue.get_requests():
                self.direction = None


    def run(self) -> None:
        """
        Run the lift simulation until all requests are served.
        This method simulates the lift moving continuously.
        """
        while self.request_queue.get_requests():
            self.move()
            print(self)  # Show the current state of the lift.
            time.sleep(0.5)  # Simulate time delay between moves.

    def __repr__(self) -> str:
        return (f"Lift(current_floor={self.current_floor}, "
                f"direction={self.direction}, "
                f"visited_floors={self.visited_floors}, "
                f"queue={self.request_queue})")
