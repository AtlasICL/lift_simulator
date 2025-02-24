import tkinter as tk

from lift import Lift
from request_simulator import simulate_requests
from input_parser import parse_config

# NOTE: This file is a SECONDARY entry point to the program
# The user should run EITHER sources/main.py OR sources/gui.py based on their desired usecase 

# TODO: floor numbers are ugly (low priority)
# TODO: general UI is ugly(?) (low priority)
# TODO: start simulation button doesn't work. Once the simulation has ended, can't start it again. (high priority)
# TODO: make the lift wait at each floor? (would be good, but I'm scared it's gonna mess up the whole Lift logic)
# TODO: make the lift show the people inside (high priority)
# TODO: make self.canvas height based on number of floors

# CONSTANTS:
STEP_DELAY_MS: int = 800 # delay between lift steps in ms
# this could be implemented using delta time class
# but i am not smart enough -emre
CONFIG_FILEPATH: str = "sources/config.json" # filepath for config.json
# TODO: is it normal that it has to be sources/config.json?
GUI_BACKGROUND_COLOUR: str = "white"
GUI_LIFT_COLOUR: str = "blue"

class LiftSimulatorGUI:
    def __init__(self, master, config_file):
        self.master = master
        self.master.title("Best Team Lift Simulator")
        
        self.config = parse_config(config_file)
        self.total_floors = self.config["total_floors"]
        self.capacity = self.config["capacity"]
        self.num_requests = self.config["num_requests"]

        self.floor_height = 40 # I had to move this up because self.canvas = tk.Canvas(...)
        # required the floor_height to determine the size of the window
        
        # Create the simulation objects
        self.lift = Lift(self.total_floors, self.capacity)
        self.requests = simulate_requests(self.num_requests, self.total_floors)
        for req in self.requests:
            self.lift.add_request(req)
        
        # Create a canvas for drawing the building and lift
        canvas_height = self.total_floors * self.floor_height # this line dynamically adapts
        # the height of the window based on the number of floors the user has specified.
        self.canvas = tk.Canvas(master, width=350, height=canvas_height, bg=GUI_BACKGROUND_COLOUR)

        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create a frame for controls and status display
        self.info_frame = tk.Frame(master)
        self.info_frame.pack(side="right", fill="y", padx=10, pady=10)
        
        self.status_label = tk.Label(self.info_frame, text="Lift Status", font=("Arial", 14))
        self.status_label.pack(pady=10)
        
        self.start_button = tk.Button(self.info_frame, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack(pady=10)
        
        # Drawing settings for floors and lift
        self.draw_building()
        self.lift_rect = None  # Will hold the lift representation on the canvas
    
    def draw_building(self):
        """Draw floor lines and labels on the canvas based on the current canvas width."""
        self.canvas.delete("floor")
        # Get current canvas width
        canvas_width = int(self.canvas["width"])
        left_margin = 10
        right_margin = 10
        line_start = left_margin
        line_end = canvas_width - right_margin

        for i in range(1, self.total_floors + 1):
            # Calculate y-coordinate for floor i.
            y = (self.total_floors - i + 1) * self.floor_height
            # Draw the floor line to span the full width of the canvas.
            self.canvas.create_line(line_start, y, line_end, y, fill="gray", tags="floor")
            # Draw the floor number near the left margin (adjust as needed).
            self.canvas.create_text(left_margin + 20, y - self.floor_height/2, text=str(i), tags="floor")

    
    def update_lift_position(self):
        canvas_height = int(self.canvas["height"])
        canvas_width = int(self.canvas["width"])
        # Calculate y-coordinate for the center of the lift rectangle.
        y = canvas_height - (self.lift.current_floor - 0.5) * self.floor_height
        lift_width = 50  # width of the lift rectangle

        # Position the lift 20 pixels from the right edge.
        x2 = canvas_width - 20
        x1 = x2 - lift_width

        if self.lift_rect is None:
            self.lift_rect = self.canvas.create_rectangle(x1, y - 15, x2, y + 15, fill=GUI_LIFT_COLOUR, tags="lift")
        else:
            self.canvas.coords(self.lift_rect, x1, y - 15, x2, y + 15)


    def update_waiting_indicators(self):
        """
        Draws little circles on each floor representing the number of waiting people,
        positioned so that they do not overlap the floor numbers.
        """
        # Clear previous waiting indicators.
        self.canvas.delete("waiting")
        
        # Count waiting requests per floor.
        waiting_counts = {}
        for req in self.lift.request_queue.get_requests():
            waiting_counts[req.origin_floor] = waiting_counts.get(req.origin_floor, 0) + 1

        # Draw circles for each floor that has waiting requests.
        for floor, count in waiting_counts.items():
            canvas_height = int(self.canvas["height"])
            # Position at the vertical center of the floor's section.
            y = canvas_height - (floor - 0.5) * self.floor_height

            # Adjust the x-coordinate so the circles don't overlap floor numbers.
            # For example, if floor numbers are drawn at x ~30, start circles at x=60.
            start_x = 60  
            radius = 5
            for i in range(count):
                circle_x = start_x + i * (2 * radius + 2)
                self.canvas.create_oval(
                    circle_x - radius, y - radius,
                    circle_x + radius, y + radius,
                    fill="red", tags="waiting"
                )


    def simulation_step(self):
        """Performs a simulation step and schedules the next one."""
        # the following if statement checks whether there is, either
        # at least 1 request still remaining, or at least 1 person still on the lift
        # if so, we go through the logic
        if self.lift.request_queue.get_requests() or self.lift.onboard_requests:
            self.lift.move() # simulation goes forward by 1 move
            self.update_lift_position() # update the position of the lift
            self.update_waiting_indicators() # update the little circles of people waiting on each floor
            
            # update status label (on the right) with current info
            status_text = (
                f"Current Floor: {self.lift.current_floor}\n"
                f"Direction: {self.lift.direction}\n"
                f"Waiting: {len(self.lift.request_queue.get_requests())}\n"
                f"Onboard: {len(self.lift.onboard_requests)}"
            )
            self.status_label.config(text=status_text)
            
            # next step after STEP_DELAY_MS milliseconds (we have chose ~750), can be changed at top of file
            self.master.after(STEP_DELAY_MS, self.simulation_step)
        else:
            self.status_label.config(text="Simulation finished!")
            self.start_button.config(state="normal")
    
    def start_simulation(self):
        self.start_button.config(state="disabled") # should not be able to press start button once the simulation has been started
        self.simulation_step()

if __name__ == "__main__":
    root = tk.Tk()
    app = LiftSimulatorGUI(root, CONFIG_FILEPATH)
    root.mainloop()
