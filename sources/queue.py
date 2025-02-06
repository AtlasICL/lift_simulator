from request import Request

class Queue:
    """
    Queue class, which stores the queue of requests for a particular instance of a lift.

    Attributes:
        - requests: list of requests, each of which is an instance of 'Request' class.
    
    Methods:
        - add_request: add a request to the queue
        - remove_request: remove a request from the queue
        NOTE: we need to make sure we remove every visited combination, i.e. if lift stops at 2, 4, 5, 8, then we need to remove:
        (2, 4), (2, 5), (2, 8), (4, 5), (4, 8), (5, 8)

    """
    
    requests: list[Request]

    def add_request(self, req: Request) -> None:
        self.requests.append(req)

    def remove_request(self, req: Request) -> None:
        self.requests.remove(req)

    

    