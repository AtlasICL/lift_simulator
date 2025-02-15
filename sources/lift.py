from req_queue import ReqQueue
from request import Request
import time

class Lift:
    def __init__(self, total_floors: int, capacity: int):
        self.current_floor = 1          # Start at floor 1
        self.total_floors = total_floors
        self.capacity = capacity
        self.request_queue = ReqQueue()  # Waiting requests
        self.onboard_requests = []       # Requests already picked up
        self.direction = None            # "up" or "down"
        self.visited_floors = []         # Track visited floors

    def add_request(self, req: Request) -> None:
        self.request_queue.add_request(req)
    
    def next_stop(self) -> int | None:
        """
        Determine the next floor to move to.
        Candidates are:
          - All destinations of onboard requests.
          - All origins of waiting requests (if there's capacity).
        The method then chooses the candidate in the current direction (or sets a direction if idle).
        """
        candidates = []
        # Include onboard requests (their destination floors)
        for req in self.onboard_requests:
            candidates.append(req.destination_floor)
        # Include waiting requests (their origin floors) if capacity allows
        if len(self.onboard_requests) < self.capacity:
            for req in self.request_queue.get_requests():
                candidates.append(req.origin_floor)
        
        if not candidates:
            return None

        # If idle, pick a direction based on the first candidate relative to current floor.
        if self.direction is None:
            for candidate in candidates:
                if candidate > self.current_floor:
                    self.direction = "up"
                    break
                elif candidate < self.current_floor:
                    self.direction = "down"
                    break

        # Depending on direction, filter candidates.
        if self.direction == "up":
            up_candidates = [floor for floor in candidates if floor > self.current_floor]
            if up_candidates:
                return min(up_candidates)
            else:
                # No upward candidate; switch direction.
                down_candidates = [floor for floor in candidates if floor < self.current_floor]
                if down_candidates:
                    self.direction = "down"
                    return max(down_candidates)
        elif self.direction == "down":
            down_candidates = [floor for floor in candidates if floor < self.current_floor]
            if down_candidates:
                return max(down_candidates)
            else:
                up_candidates = [floor for floor in candidates if floor > self.current_floor]
                if up_candidates:
                    self.direction = "up"
                    return min(up_candidates)
        return None

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

        # Update visited floors (record every unique stop)
        if self.current_floor not in self.visited_floors:
            self.visited_floors.append(self.current_floor)
            print(f"Visited floors updated: {self.visited_floors}")

        # Drop off any onboard requests that have reached their destination.
        served_requests = [req for req in self.onboard_requests if req.destination_floor == self.current_floor]
        for req in served_requests:
            print(f"Served: {req}")
            self.onboard_requests.remove(req)

        # Pick up waiting requests if the lift is at their origin and there's capacity.
        # Iterate over a copy since we might modify the queue.
        waiting_requests = self.request_queue.get_requests().copy()
        for req in waiting_requests:
            if req.origin_floor == self.current_floor and len(self.onboard_requests) < self.capacity:
                print(f"Picked up: {req}")
                req.picked_up = True
                self.onboard_requests.append(req)
                self.request_queue.remove_request(req)

        # Reset direction if there are no pending requests.
        if not self.request_queue.get_requests() and not self.onboard_requests:
            self.direction = None

    def run(self) -> None:
        """Run the lift simulation until all requests are served."""
        while self.request_queue.get_requests() or self.onboard_requests:
            self.move()
            print(self)
            time.sleep(0.5)

    def __repr__(self) -> str:
        return (f"Lift(current_floor={self.current_floor}, "
                f"direction={self.direction}, "
                f"visited_floors={self.visited_floors}, "
                f"waiting_queue={self.request_queue}, "
                f"onboard_requests={self.onboard_requests})")
