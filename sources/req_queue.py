from request import Request

class ReqQueue:
    """
    This class stores a list of Request instances.
    This class implements functionality for adding and removing Requests to the queue.

    Attributes:
        requests (list[Request]): A list containing the Request objects currently in the queue.

    Methods:
        __init__():
            The constructor initialises an empty queue.

        get_requests() -> list[Request]:
            Returns the list of Requests in the queue.

        add_request(req: Request) -> None:
            Add a new instance of Request to the queue.

        remove_request(req: Request) -> None:
            Remove a specified request from the queue (if it does indeed exist).
        
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
