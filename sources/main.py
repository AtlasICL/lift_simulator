import json
import lift
from queue import Queue
from request import Request


def main():
    f = "input.json"
    generate_requests(f)
    """
    Lift = lift.Lift()

    request1 = Request(2, 5)
    request2 = Request(1, 3)
    request3 = Request(2, 3)
    request4 = Request(4, 2)
    request5 = Request(5, 1)

    Lift.print()

    Lift.queue.add_request(request1)

    Lift.print()
    """
def generate_requests(input):
    Lift = lift.Lift()
    with open(input, "r") as file:
        data = json.load(file)
    start_floor = data.get("start")
    if start_floor == None:
        print("ERROR: Starting floor undefined")
        start_floor = int(input("Please enter starting floor: "))
        while ValueError or start_floor < 0:
            start_floor = int(input("Please enter starting floor: "))
    total_floors = data.get("floors")
    if total_floors == None:
        print("ERROR: Total floors undefined")
        total_floors = int(input("Please enter total floors: "))
        while ValueError or total_floors < start_floor:
            total_floors = int(input("Please enter total floor: "))
    for origin in range(start_floor, total_floors):
        floor_requests = data.get("requests", {}).get(origin, {})
        if floor_requests == None:
            print("NOTE: No request class defined for Floor", origin)
            continue
        for destination in floor_requests:
            request = Request(origin, destination)
            Lift.queue.add_request(request)
            Lift.print()

if __name__ == "__main__":
    main()


