import lift
from queue import Queue
from request import Request


def main():
    Lift = lift.Lift(10)

    request1 = Request(2, 5)
    request2 = Request(1, 3)
    request3 = Request(2, 3)
    request4 = Request(4, 2)
    request5 = Request(5, 1)

    Lift.print()

if __name__ == "__main__":
    main()


