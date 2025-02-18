# Documentation for the Lift manager

---

# Table of contents

- ## [1) Project overview and features](#1-project-overview-and-features-1)
    - ### [a) Project description](#a-project-description-1)
    - ### [b) Scope](#b-scope-1)

- ## [2) Usage instructions](#2-usage-instructions-1)
    - ### [a) Requirements](#a-requirements-1)
    - ### [b) Configuration instructions](#b-configuration-instructions-1)
    - ### [c) Build](#c-build-1)

- ## [3) Code documentation](#3-code-documentation-1)

- ## [4) Screenshots and demo](#4-screenshots-and-demo-1)



# 1) Project overview and features

## a) Project description

In modern multi-story buildings, efficient lift systems are crucial for ensuring smooth operations and enhancing the user experience. Lift control systems, which are responsible for scheduling and managing the movement of lifts in response to passenger requests, play a signifcant role in achieving this efficiency. Traditional lift control systems often operate on simple algorithms, which may not adapt well to varying traffic patterns, leading to unnecessary wait times and inefficient response usage.

This project aims to develop an inteligent and highly adaptable lift control system using advanced data structures and scheduling algorithms, including SCAN andf LOOK. By simulating real-world scenarios with multiple passengers and varying requests, the system will prioritise requests based on factors such as travel direction, waiting times and proximity to the lift. The design is scalable, able to accomodate a configurable numnber of floors and passengers. Additionally, this system will integrate performance metrics to compare the efficiency of different algorithms, ultimately demonstrating a comprehensive approach to managing lift operations while optimising user satisfaction. 

Through the use of data structures like queues and priority queues, and implementing algorithms such as SCAN and LOOK, this project will explore how dynamic scheduling can improve lift systems' responsiveness to user requests, contributing to reduced wait times and overall operational efficiency.

## b) Scope

TODO: Describe scope of project
example: we did not implement multiple lifts per building, but we do have GUI, etc

# 2) Usage instructions

## a) Requirements

The project runs on Python 3.13.  
The GUI (graphical user interface) requires the Python module tkinter. This library can be installed using 
```
pip install tk
```

## b) Configuration instructions

The program requires a configuration file, where the user provides parameters for the program.  

These should be included in a `config.json` file, located at `/sources/config.json`.  

Here is an example file; the formatting should look like the following:  
```
{
    "total_floors": 10,
    "capacity": 5,
    "num_requests": 30
}
```
The file must be a valid json file.  

- `total_floors` parameter specifies the number of floors in the building. **Note:** this value must be **strictly greater than 1** to be valid (explanation: a building with 1 floor does not require a lift, and a building with 0 or negative floors does not make sense).  
- `capacity` parameter denotes the capacity of the lift, measured as $x$ number of people. In the example file, the lift has a maximum capacity of 5 people. **Note:** this value must be **greater than or equal to 0** (explanation: a lift with a capacity of 0 people does not make sense, and idem for negative capacity).
- `num_requests` parameter specifies the number of requests (people wanting to go to a different floor) to be simulated. This value will affect both main.py and gui.py entry points. 

## c) Build

The program has **3 entry points**:
- 'main.py': this entry point is to run the simulation in the command line.
- 'gui.py': this entry point is to run the simulation with the graphical user interface.
- 'testing.py': this entry point is to run multiple repeated simulations, in order to generate simulation data.

We recommend that the user runs
```
python sources/gui.py
```

---

# 3) Code documentation

- **Lift Class (lift.py)**:
This class manages the lifts operations, including its movement, request queue, and the people inside. It uses attributes such as: current_floor (the current floor the lift is at); capacity (the max number of people the lift can hold); onboard_requests (a list of requests currently in the lift); and request_queue (a queue for handling requests outside of the lift). The methods for this class are as follows: add_requests (adds a new request to the lifts reqeust queue); move (moves the lift to the next requested floor based on its direction); and get_current_direction (determines wether the lift is moving up or down). 

- **Request Class (request_simulator.py)**:
This class represents the individual lift requests, made from a specific floor to another. Attributes used are: origin_floor (the floor where the request originated); destination_floor (the target floor for the lift); and picked_up (a flag indicating wether a request has been fulfilled). The methods utilised are: is_valid_request (checks if the request is valid (e.g, floors must be within range and cannot be the same)); is_upward (checks if the reqeut is for an upward movement); and is_downward (checks if the request is for a downward movement).

- **GUI class (gui.py)**:
This class manages the user interface for simulating the lift's behaviour using the tkinter library. It uses the following attributes: master (the root window of the GUI); config (configuration settings loaded from a JSON floor I(e.g., total floors)); lift (an instance of the lift class); requests (list of generated requests for the simulation); canvas (the canvas where the building and lift are drawn); start_button (the button to start the simulation); and status_label (a label to display the status of the simulation). The methods used within this class are: init (initialises the GUI, loads config, creates the lift object and prepares the canvas); draw_building (draws the bjuilding layout, including the floors and floor numbers); update_lift_position (updates the position of the lift on the canvas as it moves); update_waiting_indicators (draws circles representing people waiting at each floor); simulation_step (advances the simulation by one step, moving the lift and updating the display); and start_simulation (starts the simulation and disables the start button to prevent multiple starts).

---

# 4) Screenshots and demo

TODO: we should complete this later, when the project is almost finished.

