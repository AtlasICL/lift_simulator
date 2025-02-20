# Documentation for the Lift manager


# Table of contents

- ## [1) Project overview and features](#1-project-overview-and-features-1)
    - [a) Project description](#a-project-description-1)
    - [b) Scope](#b-scope-1)

- ## [2) Usage instructions](#2-usage-instructions-1)
    - [a) Requirements](#a-requirements-1)
    - [b) Configuration instructions](#b-configuration-instructions-1)
    - [c) Build](#c-build-1)

- ## [3) Performance analysis](#3-performance-analysis-1)
    - [a) Overview](#a-overview)
    - [b) Parameters](#b-parameters)
    - [c) Testing methodology](#c-testing-methodology)
    - [d) Output format and generating graphs](#d-output-format-and-generating-graphs)
    - [e) Interpretation of results](#e-interpretation-of-results)

- ## [4) Code documentation](#4-code-documentation-1)

- ## [5) Screenshots and demo](#5-screenshots-and-demo-1)









# 1) Project overview and features

## a) Project description

In modern multi-story buildings, efficient lift systems are crucial for ensuring smooth operations and enhancing the user experience. Lift control systems, which are responsible for scheduling and managing the movement of lifts in response to passenger requests, play a signifcant role in achieving this efficiency. Traditional lift control systems often operate on simple algorithms, which may not adapt well to varying traffic patterns, leading to unnecessary wait times and inefficient response usage.

This project aims to develop an inteligent and highly adaptable lift control system using advanced data structures and scheduling algorithms, including SCAN andf LOOK. By simulating real-world scenarios with multiple passengers and varying requests, the system will prioritise requests based on factors such as travel direction, waiting times and proximity to the lift. The design is scalable, able to accomodate a configurable numnber of floors and passengers. Additionally, this system will integrate performance metrics to compare the efficiency of different algorithms, ultimately demonstrating a comprehensive approach to managing lift operations while optimising user satisfaction. 

Through the use of data structures like queues and priority queues, and implementing algorithms such as SCAN and LOOK, this project will explore how dynamic scheduling can improve lift systems' responsiveness to user requests, contributing to reduced wait times and overall operational efficiency.

## b) Scope

TODO: Describe scope of project
example: we did not implement multiple lifts per building, but we DO have GUI, etc














# 2) Usage instructions

## a) Requirements

The project runs on Python 3.13.  
The GUI (graphical user interface) requires the Python module tkinter. This library can be installed using 
```
pip install tk
```
For generation of graphs, we used the following libraries:
- pandas
- matplotlib
- numpy
- seaborn

However you do not need to install these to run the code. They are only necessary for generation of result graphs.


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

The program has **2 main entry points**:
- `sources/main.py`: this entry point is to run the simulation in the command line.
- `sources/gui.py`: this entry point is to run the simulation with the graphical user interface.  

We recommend that the user runs
```
python sources/gui.py
```
  
Optionally, there are 2 additional entry points to the program, used for simulation data generation: 
- `sources/testing/testing_script.py`: this entry point is to run multiple repeated simulations to generate simulation data. It outputs the 'moves' variable.
- `sources/testing/ttsw_testing_script.py`: this entry point is to run multiple repeated simulations to generate simulation data. It outputs the 'TTSW' variable.















# 3) Performance analysis

### a) Overview  
We performed thorough analysis of our lift manager's performance. We made use of test scripts, which repeatedly simulated the lift operation, while randomly varying parameters such as floor count, lift capacity, and number of requests.  
We systematically saved the results of our simulations in csv files, which are located in the `results/data/` directory.

### b) Parameters

We measured the performance of the lift using 3 output values:
- **Moves**: represents the number of moves the lift has to make over time.  
For examplemoving from floor 2 to floor 5 corresponds to 3 moves; moving from floor 1 to floor 6, then down to floor 3, corresponds to 5+3 = 8 moves.
- **TTSW**: TTSW stands for Total Time Spent Waiting.  
This variable accumulates the sum of waiting requests at each simulation step.  
At every iteration of the simulation loop, the number of waiting requests is added to `ttsw`. Since each simulation step represents one unit of time, TTSW is a good metric for waiting time experienced by all passengers in the simulation.
A higher `ttsw` value indicates that, on average, passengers waited longer before being served.  
The higher the TTSW, the more waiting has happened. 
- **LOROT**: LOROT stands for Lift Occupancy Ratio Over Time.  
This variable represents the occupancy ratio of the lift (how full it is) over time. On one hand, this ratio being low means the lift has more available capacity at any given moment, which would imply we would want to minimise it, vis-a-vis lift availability. On the other hand, maximising this variable means the lift is carrying as close as possible to its maximum capacity, which implies the lift is operating more efficiently.

**Equations**  

Formula for TTSW:  
$$
\text{TTSW(t)} = \sum_{t = \text{beginning of simulation}}^{\text{end of simulation}}{\text{NumberOfPeopleWaiting}(t)}
$$
  
Formula for LOROT:  
$$
\text{LOR}(t) = \frac{\text{occupancy}(t)}{\text{max\_capacity}}
$$

$$
\cdot
$$


$$
\text{LOROT} = \int_{t = \text{beginning of simulation}}^{\text{end of simulation}}{\text{LOR}(t)}\:dt
$$
  
Average LOROT over a run:
$$
\text{LOROT}_{\text{average}} = \frac{1}{T} \: \cdot \: \int_{t = \text{beginning of simulation}}^{\text{end of simulation}}{\text{LOR}(t)}\:dt
$$


### c) Testing methodology



### d) Output format and generating graphs


### e) Interpretation of results












# 4) Code documentation

- **Lift Class (lift.py)**:
![Image](https://github.com/user-attachments/assets/47118910-a8e9-4f09-af65-644c535aa326)

This class manages the lifts operations, including its movement, request queue, and the people inside. It uses attributes such as: current_floor (the current floor the lift is at); capacity (the max number of people the lift can hold); onboard_requests (a list of requests currently in the lift); and request_queue (a queue for handling requests outside of the lift). The methods for this class are as follows: add_requests (adds a new request to the lifts reqeust queue); move (moves the lift to the next requested floor based on its direction); and get_current_direction (determines wether the lift is moving up or down). 

- **Request Class (request.py)**:

![Image](https://github.com/user-attachments/assets/c171f149-75e4-483e-aec2-e79da4fb6c96)

This class represents each individual lift request, a request indicates a call to the lift from an origin floor to a destination floor. The attributes used are: origin_floor (the floor where the request originated); destination_floor (the target floor for the lift); and picked_up (a flag indicating whether the request has been fulfilled). The methods utilized are: is_valid_request (checks if the request is valid, ensuring both floors are within range and not the same); is_upward (checks if the request is for an upward movement); is_downward (checks if the request is for a downward movement); and __repr__ (returns a string representation of the request, displaying its status as either waiting or picked up).

- **Request Simulator Class (request_simulator.py)**:
This class represents the individual lift requests, made from a specific floor to another. Attributes used are: origin_floor (the floor where the request originated); destination_floor (the target floor for the lift); and picked_up (a flag indicating wether a request has been fulfilled). The methods utilised are: is_valid_request (checks if the request is valid (e.g, floors must be within range and cannot be the same)); is_upward (checks if the reqeut is for an upward movement); and is_downward (checks if the request is for a downward movement).

- **GUI class (gui.py)**:
This class manages the user interface for simulating the lift's behaviour using the tkinter library. It uses the following attributes: master (the root window of the GUI); config (configuration settings loaded from a JSON floor I(e.g., total floors)); lift (an instance of the lift class); requests (list of generated requests for the simulation); canvas (the canvas where the building and lift are drawn); start_button (the button to start the simulation); and status_label (a label to display the status of the simulation). The methods used within this class are: init (initialises the GUI, loads config, creates the lift object and prepares the canvas); draw_building (draws the bjuilding layout, including the floors and floor numbers); update_lift_position (updates the position of the lift on the canvas as it moves); update_waiting_indicators (draws circles representing people waiting at each floor); simulation_step (advances the simulation by one step, moving the lift and updating the display); and start_simulation (starts the simulation and disables the start button to prevent multiple starts).










# 5) Screenshots and demo

TODO: we should complete this later, when the project is almost finished.

