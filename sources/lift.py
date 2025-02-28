from enum import Enum

from req_queue import ReqQueue
from request import Request

class Direction(Enum):
    UP = "up"
    DOWN = "down"
    NONE = None


class Lift:
    """
    This lass implements the main functionality of the lift, namely deciding where to go next (using __next_floor() method),
    and removing served requests from its request_queue.

    Attributes:
        current_floor (int): The current floor of the lift (starts at 1).
        total_floors (int): Number of floors in the building.
        capacity (int): Capacity of the lift (max requests on board).
        request_queue (ReqQueue): Queue with the requests for the lift.
        onboard_requests (list[Request]): List of requests which are onboard the lift at given time.
        direction (Direction): Current direction of the elevator - enum: (UP, DOWN, or NONE).

    """

    def __init__(self, total_floors: int, capacity: int):
        self.current_floor: int = 1                     # Start at floor 1
        self.total_floors: int = total_floors
        self.capacity: int = capacity
        self.request_queue: ReqQueue = ReqQueue()       # Waiting requests
        self.onboard_requests: list[Request] = []       # Requests already picked up
        self.direction = Direction.NONE                 # enum, direction is initialised to NONE
        self.current_floor_stop: bool = True            # whether or not the lift needs to stop at the current floor


    def __get_candidate_floors(self) -> list[int]:
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


    def __filter_candidates(self, candidates: list[int], compare, select) -> int | None:
        """
        Helper function to filter candidate requests in __next_floor() method.
        Retrurns the selected floor, or None if no valid candidate.
        Compare takes in an inline (lambda) function which compares the candidate to the current floor based on 
        the lift's current direction (so x>y or x<y based on if lift direction is upward or downward).
        Select takes in a function, min if upward, max if downward. 
        """
        valid_floors: list[int] = [floor for floor in candidates if compare(floor, self.current_floor) == True]
        return select(valid_floors) if valid_floors else None
    

    def __need_to_stop(self) -> bool:
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
    
    
    def __next_floor(self) -> int | None:
        """
        Determine the next floor to move to.

        The lift has a direction, up or down. If the lift is upbound, the __next_floor() function filters requests by ones which 
        are upbound, and picks them up if their origin floor is the lift's current floor, and the lift is not full.
        """
        candidates = self.__get_candidate_floors()

        if self.direction == Direction.NONE:
            self.direction = Direction.UP # if the lift is idle, we arbitrarily set direction to up
            # if there are no upward requests, the rest of this method will deal with it appropriately

        # filter the candidates based on the direction of the lift
        # Explanation: if the lift is moving upward, we do not want to pick up any requests which want to go downwards
        # so we filter those requests which are upward
        if self.direction == Direction.UP:
            next_up = self.__filter_candidates(candidates, lambda x, y: x > y, min)
            if next_up is not None:
                return next_up
            # no one wants to go upwards (no valid up_candidates) so we switch direction
            next_down = self.__filter_candidates(candidates, lambda x, y: x < y, max)
            if next_down is not None:
                self.direction = Direction.DOWN  # we switched direction, so we update self.direction
                return next_down
        
        elif self.direction == Direction.DOWN:
            next_down = self.__filter_candidates(candidates, lambda x, y: x < y, max)
            if next_down is not None:
                return next_down
            # if no downward candidates were found, we switch direction to upwards
            next_up = self.__filter_candidates(candidates, lambda x, y: x > y, min)
            if next_up is not None:
                self.direction = Direction.UP  # we switched direction, so we update self.direction
                return next_up
        return None  # if no candidates were valid, we return None and the lift goes idle
    

    def __offload_and_onload_requests(self) -> None:
        served_requests = [req for req in self.onboard_requests if req.destination_floor == self.current_floor]
        for req in served_requests:
            self.onboard_requests.remove(req)

        # IF the lift is at the origin of a request, AND the capacity is not full, we pick up the request
        # we iterate over a COPY of the queue (.copy()) since we might modify it
        waiting_requests = self.request_queue.get_requests().copy()
        for req in waiting_requests:
            if req.origin_floor == self.current_floor and len(self.onboard_requests) < self.capacity:
                req.picked_up = True
                self.onboard_requests.append(req)
                self.request_queue.remove_request(req)


    def move(self) -> None:
        """
        The move() method updates the current_floor based on which way the lift is moving (which is determined by __next_floor() method).
        move() also calls the member method need_to_stop() to see if the lift needs to stop at the current floor (to pick up or
        drop off any requests).
        """
        next_floor = self.__next_floor()
        if next_floor is None:
            return
        
        if self.current_floor < next_floor:
            self.current_floor += 1
        elif self.current_floor > next_floor:
            self.current_floor -= 1

        self.current_floor_stop = self.__need_to_stop()  # update the member variable which shows whether or not the lift needs to stop

        if self.current_floor_stop:
            self.__offload_and_onload_requests()

        # if there are no more requests, and no one onboard, reset direction to None
        if not self.request_queue.get_requests() and not self.onboard_requests:
            self.direction = Direction.NONE


    def __repr__(self) -> str:
        return (f"Lift(current_floor={self.current_floor}, "
                f"direction={self.direction}, "
                f"waiting_queue={self.request_queue}, "
                f"onboard_requests={self.onboard_requests}), "
                f"stopping={self.current_floor_stop}")
