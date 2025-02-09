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
def generate_requests(input_file):
    Lift = lift.Lift()
    with open(input_file, "r") as file:
        data = json.load(file)
    valid_input = False
    try:
        start_floor = int(data.get("start"))
        if start_floor < 0:
            print("ERROR: Starting floor undefined")
        else: 
            valid_input = True
    except:
        print("ERROR: Starting floor undefined")
    while valid_input == False:
        try:
            start_floor = int(input("Please enter starting floor: "))
            if start_floor < 0:
                print("ERROR: Starting floor must equal or exceed 0")
            else:
                valid_input = True
        except:
            print("ERROR: Invalid input")
    valid_input = False
    try:
        total_floors = int(data.get("floors"))
        if total_floors < start_floor:
            print("ERROR: Total floors undefined")
        else: 
            valid_input = True
    except:
        print("ERROR: Total floors undefined")
    while valid_input == False:
        try:
            total_floors = int(input("Please enter total floors: "))
            if total_floors < start_floor:
                print("ERROR: Total floors must equal or exceed starting floor")
            else:
                valid_input = True
        except:
            print("ERROR: Invalid input")
    for origin in range(start_floor, total_floors + 1):
        floor_requests = data.get("requests", {}).get(str(origin), {})
        if floor_requests == {}:
            print("NOTE: No request class defined for Floor", origin)
            continue
        for destination in floor_requests:
            request = Request(origin, destination)
            Lift.queue.add_request(request)
    Lift.print()

if __name__ == "__main__":
    main()


