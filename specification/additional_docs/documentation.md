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

NOTE: I can do this part, it's quite easy and I'm familiar with the code anyway -Emre

## a) Requirements

## b) Configuration instructions

## c) Build


# 3) Code documentation

TODO: this is the biggest part  
We need to give a detailed explanation of our code.  
We need to have diagrams of the code structure / organisation (@Luca you said you could cook on this right?)

-----

ETIENNE WORK FOR CLASSES:
## Main Components 

1. **Lift Class (lift.py)**:
This class manages the lifts operations, including its movement, request queue, and the people inside. It uses attributes such as: current_floor (the current floor the lift is at); capacity (the max number of people the lift can hold); onboard_requests (a list of requests currently in the lift); and request_queue (a queue for handling requests outside of the lift). The methods for this class are as follows: add_requests (adds a new request to the lifts reqeust queue); move (moves the lift to the next requested floor based on its direction); and get_current_direction (determines wether the lift is moving up or down). 

2. **Request Class (request_simulator.py)**:
This class represents the individual lift requests, made from a specific floor to another. Attributes used are: origin_floor (the floor where the request originated); destination_floor (the target floor for the lift); and picked_up (a flag indicating wether a request has been fulfilled). The methods utilised are: is_valid_request (checks if the request is valid (e.g, floors must be within range and cannot be the same)); is_upward (checks if the reqeut is for an upward movement); and is_downward (checks if the request is for a downward movement).

3. **GUI class (gui.py)**:
This class manages the user interface for simulating the lift's behaviour using the tkinter library. It uses the following attributes: master (the root window of the GUI); config (configuration settings loaded from a JSON floor I(e.g., total floors)); lift (an instance of the lift class); requests (list of generated requests for the simulation); canvas (the canvas where the building and lift are drawn); start_button (the button to start the simulation); and status_label (a label to display the status of the simulation). The methods used within this class are: init (initialises the GUI, loads config, creates the lift object and prepares the canvas); draw_building (draws the bjuilding layout, including the floors and floor numbers); update_lift_position (updates the position of the lift on the canvas as it moves); update_waiting_indicators (draws circles representing people waiting at each floor); simulation_step (advances the simulation by one step, moving the lift and updating the display); and start_simulation (starts the simulation and disables the start button to prevent multiple starts).

-----

# 4) Screenshots and demo

TODO: we should complete this later, when the project is almost finished.

