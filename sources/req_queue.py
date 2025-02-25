from request import Request

class ReqQueue:
    """
    A queue manager for Request objects.

    The ReqQueue class provides a data structure to store and manage Request objects.
    It supports adding and removing requests, eliminating duplicate requests based on 
    their origin and destination floors, and purging requests that have been served 
    according to a specified order of visited floors.

    Attributes:
        requests (list[Request]): A list containing the Request objects currently in the queue.

    Methods:
        __init__():
            Initializes an empty ReqQueue.

        get_requests() -> list[Request]:
            Returns the list of Request objects in the queue.

        add_request(req: Request) -> None:
            Adds a new Request object to the queue.

        remove_request(req: Request) -> None:
            Removes the specified Request object from the queue if it exists.
        
        __repr__() -> str:
            Returns a string representation of the current state of the queue.
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

    def __repr__(self) -> str:
        return f"ReqQueue({self.requests})"
