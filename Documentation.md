### Lift (Elevator) Control System 

### Module: ECM1414 - Data Structures and Algorithms 

### Group members: Emre Acarsoy, Etienne Hackett, Luca Croci, Luca Pacitti, Akkshay Sharrma

---

## Introduction 
In modern multi-story buildings, efficient lift systems are crucial for ensuring smooth operations and enhancing the user experience. Lift control systems, which are responsible for scheduling and managing the movement of lifts in response to passenger requests, play a signifcant role in achieving this efficiency. Traditional lift control systems often operate on simple algorithms, which may not adapt well to varying traffic patterns, leading to unnecessary wait times and inefficient response usage.
This project aims to develop an inteligent and highly adaptable lift control system using advanced data structures and scheduling algorithms, including SCAN andf LOOK. By simulating real-world scenarios with multiple passengers and varying requests, the system will prioritise requests based on factors such as travel direction, waiting times and proximity to the lift. The design is scalable, able to accomodate a configurable numnber of floors and passengers. Additionally, this system will integrate performance metrics to compare the efficiency of different algorithms, ultimately demonstrating a comprehensive approach to managing lift operations while optimising user satisfaction. 
Through the use of data structures like queues and priority queues, and implementing algorithms such as SCAN and LOOK, this project will explore how dynamic scheduling can improve lift systems' responsiveness to user requests, contributing to reduced wait times and overall operational efficiency.

--- 

## The main objectives of this project are:

1. **Efficient Request Handling**:  
   Develop a system that can efficiently handle incoming requests from passengers, which include both up and down requests, and prioritize them based on factors such as request direction, waiting time, and floor proximity.

2. **Algorithm Implementation**:  
   Implement two scheduling algorithms — **SCAN** and **LOOK** — to manage the movement of the lift in response to passenger requests. Additionally, design a **MYLIFT algorithm** that competes with the above algorithms and potentially improves upon their performance by considering various optimization strategies.

3. **Performance Simulation**:  
   Simulate real-world scenarios in which multiple passengers make lift requests. Implement constraints such as lift capacity and time taken to move between floors, ensuring the system accurately reflects real-world limitations. Analyze the efficiency of the implemented algorithms by generating performance data through the simulation.

4. **Data Structure Implementation**:  
   Use appropriate data structures, such as queues and priority queues, to manage the requests and ensure the system responds to them in a structured and efficient manner. Implement priority handling where certain requests may have higher priority due to longer waiting times.

5. **Analysis and Optimization**:  
   Collect performance metrics from the simulation and compare the efficiency of the different scheduling algorithms. Identify areas where the system performs well and where improvements are needed, leading to an enhanced understanding of how these algorithms can be optimized for better results.

6. **Exploration of Advanced Features (Optional)**:  
   Explore the development of a Graphical User Interface (GUI) for visualizing the lift movement and requests. Additionally, implement the extension of the system to support multiple lifts, allowing for a more complex and scalable solution.

---

## Main Components 

1. **Lift Class (lift.py)**:
This class manages the lifts operations, including its movement, request queue, and the people inside. It uses attributes such as: current_floor (the current floor the lift is at); capacity (the max number of people the lift can hold); onboard_requests (a list of requests currently in the lift); and request_queue (a queue for handling requests outside of the lift). The methods for this class are as follows: add_requests (adds a new request to the lifts reqeust queue); move (moves the lift to the next requested floor based on its direction); and get_current_direction (determines wether the lift is moving up or down). 

2. **Request Class (request_simulator.py)**:
This class represents the individual lift requests, made from a specific floor to another. Attributes used are: origin_floor (the floor where the request originated); destination_floor (the target floor for the lift); and picked_up (a flag indicating wether a request has been fulfilled). The methods utilised are: is_valid_request (checks if the request is valid (e.g, floors must be within range and cannot be the same)); is_upward (checks if the reqeut is for an upward movement); and is_downward (checks if the request is for a downward movement).

3. **GUI class (gui.py)**:
This class manages the user interface for simulating the lift's behaviour using the tkinter library. It uses the following attributes: master (the root window of the GUI); config (configuration settings loaded from a JSON floor I(e.g., total floors)); lift (an instance of the lift class); requests (list of generated requests for the simulation); canvas (the canvas where the building and lift are drawn); start_button (the button to start the simulation); and status_label (a label to display the status of the simulation). The methods used within this class are: init (initialises the GUI, loads config, creates the lift object and prepares the canvas); draw_building (draws the bjuilding layout, including the floors and floor numbers); update_lift_position (updates the position of the lift on the canvas as it moves); update_waiting_indicators (draws circles representing people waiting at each floor); simulation_step (advances the simulation by one step, moving the lift and updating the display); and start_simulation (starts the simulation and disables the start button to prevent multiple starts).


