from enum import Enum

from req_queue import ReqQueue
from request import Request

class Direction(Enum):
    UP = "up"
    DOWN = "down"
    NONE = None


class Lift:
    """
    This class implements the main functionality of the lift. This class contains the queue of requests for the lift, 
    as well as the implementation for determining which floor to go to.

    Attributes:
        current_floor (int):                  The current floor of the lift (starts at 1).
        total_floors (int):                   Number of floors in the building.
        capacity (int):                       Capacity of the lift (max requests on board).
        request_queue (ReqQueue):             Queue with the requests for the lift.
        onboard_requests (list[Request]):     List of requests which are onboard the lift at given time.
        direction (enum):                     Current direction of the elevator - enum: (UP, DOWN, or NONE).

    Public methods:
        __init__()
        move()
        __repr__()

    """

    def __init__(self, total_floors: int, capacity: int):
        """
        Instantiates an instance of Lift class. Requires total_floors and capacity to be passed in by the caller.
        """
        self.current_floor: int = 1                     # Start at floor 1
        self.total_floors: int = total_floors
        self.capacity: int = capacity
        self.request_queue: ReqQueue = ReqQueue()       # Waiting requests
        self.onboard_requests: list[Request] = []       # Requests already picked up
        self.direction = Direction.NONE                 # enum, direction is initialised to NONE
        self.current_floor_stop: bool = True            # whether or not the lift needs to stop at the current floor


    def _is_full(self) -> bool:
        """Returns True if lift is at max capacity, False otherwise."""
        return len(self.onboard_requests) >= self.capacity


    def _get_candidate_floors(self) -> list[int]:
        """
        Helper function to get candidate floors for next_stop().
        next_stop() will then filter these candidates and select appropriately.
        """
        candidate_floors: list[int] = []
        # include onboard requests (their destination floors)
        for req in self.onboard_requests:
            candidate_floors.append(req.destination_floor)
        # include waiting requests (their origin floors) if capacity allows
        if len(self.onboard_requests) < self.capacity:
            for req in self.request_queue.get_requests():
                candidate_floors.append(req.origin_floor)
        return candidate_floors


    def _filter_candidates(self, candidates: list[int], compare, select) -> int | None:
        """
        Helper function to filter candidate requests in _next_floor() method.
        Retrurns the selected floor, or None if no valid candidate.
        Compare takes in an inline (lambda) function which compares the candidate to the current floor based on 
        the lift's current direction (so x>y or x<y based on if lift direction is upward or downward).
        Select takes in a function, min if upward, max if downward. 
        """
        valid_floors: list[int] = [floor for floor in candidates if compare(floor, self.current_floor) == True]
        return select(valid_floors) if valid_floors else None
    

    def _need_to_stop(self) -> bool:
        """Helper function which returns True if the lift needs to stop and open the doors at current floor"""
        # check if any onboard requests have reached their destination
        # print(self.onboard_requests)
        for req in self.onboard_requests:
            if req.destination_floor == self.current_floor:
                return True
        # check if anyone is waiting for the lift at current floor
        for req in self.request_queue.get_requests():
            if req.origin_floor == self.current_floor:
                return True
        return False
    
    
    def _next_floor(self) -> int | None:
        """
        This function determines which floor the lift should move to next. It achieves this by looking at the destinations of
        onboard requests, and the origin floors of waiting requests. 
        """
        candidates = self._get_candidate_floors()

        if self.direction == Direction.NONE:
            self.direction = Direction.UP # if the lift is idle, we arbitrarily set direction to up
            # if there are no upward requests, the rest of this method will deal with it appropriately

        # filter the candidates based on the direction of the lift
        if self.direction == Direction.UP:
            next_up = self._filter_candidates(candidates, lambda x, y: x > y, min)
            if next_up is not None:
                return next_up
            # no one wants to go upwards (no valid up_candidates) so we switch direction
            next_down = self._filter_candidates(candidates, lambda x, y: x < y, max)
            if next_down is not None:
                self.direction = Direction.DOWN  # we switched direction, so we update self.direction
                return next_down
        
        elif self.direction == Direction.DOWN:
            next_down = self._filter_candidates(candidates, lambda x, y: x < y, max)
            if next_down is not None:
                return next_down
            # if no downward candidates were found, we switch direction to upwards
            next_up = self._filter_candidates(candidates, lambda x, y: x > y, min)
            if next_up is not None:
                self.direction = Direction.UP  # we switched direction, so we update self.direction
                return next_up
        return None  # if no candidates were valid, we return None and the lift goes idle
    

    def _offload_and_onload_requests(self) -> None:
        """
        This function offloads onboard requests which have reached their destination, and, if space is available,
        picks up any waiting requests.
        """
        # drop off any served requests
        served_requests = [req for req in self.onboard_requests if req.destination_floor == self.current_floor]
        for req in served_requests:
            self.onboard_requests.remove(req)

        # we iterate over a COPY of the queue (.copy()) since we might modify it
        waiting_requests = self.request_queue.get_requests().copy()
        for req in waiting_requests:
            if req.origin_floor == self.current_floor and not self._is_full():
                self.onboard_requests.append(req) # add the request to list of onboard requests
                self.request_queue.remove_request(req) # remove that request from the waiting request queue
                req.picked_up = True


    def move(self) -> None:
        """
        The move() method updates the current_floor based on which way the lift is moving (which is determined by _next_floor() method).
        move() also calls the member method need_to_stop() to see if the lift needs to stop at the current floor (to pick up or
        drop off any requests).
        """
        next_floor = self._next_floor()
        if next_floor is None:
            return
        
        if self.current_floor < next_floor:
            self.current_floor += 1
        elif self.current_floor > next_floor:
            self.current_floor -= 1

        self.current_floor_stop = self._need_to_stop()  # update the member variable which shows whether or not the lift needs to stop

        if self.current_floor_stop:
            self._offload_and_onload_requests()

        # if there are no more requests, and no one onboard, reset direction to None
        if not self.request_queue.get_requests() and not self.onboard_requests:
            self.direction = Direction.NONE


    def __repr__(self) -> str:
        return (f"Lift(current_floor={self.current_floor}, "
                f"direction={self.direction}, "
                f"waiting_queue={self.request_queue}, "
                f"onboard_requests={self.onboard_requests}), "
                f"stopping={self.current_floor_stop}")
