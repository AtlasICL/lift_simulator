import lift
from request import Request

Lift = lift.Lift()

request1 = Request(2, 5)
request2 = Request(1, 3)
request3 = Request(2, 3)
request4 = Request(4, 2)
request5 = Request(5, 1)

example_requests = [request1, request2, request3, request4, request5]

Lift.print()

for req in example_requests:
    Lift.queue.add_request(req)

Lift.print()