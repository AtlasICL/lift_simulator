import tkinter as tk

from lift import Lift
from lift import Direction
from request_simulator import simulate_requests
from input_parser import parse_config


# CONSTANTS:

STEP_DELAY_MS: int = 700                             # delay between lift steps in ms
LIFT_STOP_DELAY_MS: int = 700                  # waiting time for lift stop at a floor

GUI_BACKGROUND_COLOUR: str = "white"                 # background colour for the main window
GUI_WINDOW_TITLE: str = "Best Team Lift Simulator"   # window title
GUI_DEFAULT_FONT: str = "Arial"

GUI_LIFT_COLOUR: str = "blue"                        # fill colour of the lift rectangle 

GUI_FLOOR_HEIGHT: int = 40                           # height of each floor

GUI_LIFT_TEXT_COLOUR: str = "white"                  # text colour for onboard counter in lift rectangle
GUI_LIFT_TEXT_FONT: str = GUI_DEFAULT_FONT           # text font for onboard counter in lift rectangle
GUI_LIFT_TEXT_FONT_SIZE: int = 13                    # text font size for onboard counter in lift rectangle

GUI_STATUS_TEXT_TITLE: str = "Lift Status"           # title for the status text
GUI_STATUS_TEXT_FONT: str = GUI_DEFAULT_FONT         # text font for status text (set to default, Arial)
GUI_STATUS_TEXT_FONT_SIZE: int = 14                  # text font size for status text


class LiftSimulatorGUI:
    def __init__(self, master, config_file):
        self.master = master
        self.master.title(GUI_WINDOW_TITLE)
        
        self.config = parse_config(config_file)
        self.total_floors = self.config["total_floors"]
        self.capacity = self.config["capacity"]
        self.num_requests = self.config["num_requests"]

        self.floor_height = GUI_FLOOR_HEIGHT # i had to move this up because self.canvas = tk.Canvas(...)
        # required the floor_height to determine the size of the window
        
        # these are the simulation objects
        self.lift = Lift(self.total_floors, self.capacity)
        self.requests = simulate_requests(n_requests=self.num_requests, max_floor=self.total_floors)
        for req in self.requests:
            self.lift.request_queue.add_request(req)
        
        canvas_height = self.total_floors * self.floor_height # this line dynamically adapts
        # the height of the window based on the number of floors the user has specified.
        # i implemented this otherwise the window looked really ugly for certain input parameters
        self.canvas = tk.Canvas(master, width=350, height=canvas_height, bg=GUI_BACKGROUND_COLOUR)

        self.canvas.pack(side="left", fill="both", expand=True)
        
        # create the tk frame
        self.info_frame = tk.Frame(master)
        self.info_frame.pack(side="right", fill="y", padx=10, pady=10)
        
        self.status_label = tk.Label(self.info_frame, text=GUI_STATUS_TEXT_TITLE, font=(GUI_STATUS_TEXT_FONT, GUI_STATUS_TEXT_FONT_SIZE))
        self.status_label.pack(pady=10)
        
        self.start_button = tk.Button(self.info_frame, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack(pady=10)
        
        self.draw_building()
        self.lift_rect = None
    
    def draw_building(self):
        """Draw floor lines and labels on the canvas based on the current canvas width."""
        self.canvas.delete("floor")
        canvas_width = int(self.canvas["width"]) # gets current canvas width
        LEFT_MARGIN = 10
        RIGHT_MARGIN = 10
        line_start = LEFT_MARGIN
        line_end = canvas_width - RIGHT_MARGIN

        for i in range(1, self.total_floors + 1):
            # calculate y-coordinate for i-th floor
            y = (self.total_floors - i + 1) * self.floor_height
            # floor line
            self.canvas.create_line(line_start, y, line_end, y, fill="gray", tags="floor")
            # write floor number
            self.canvas.create_text(LEFT_MARGIN + 20, y - self.floor_height/2, text=str(i), tags="floor")

    
    def update_lift_position(self):
        canvas_height = int(self.canvas["height"])
        canvas_width = int(self.canvas["width"])
        y = canvas_height - (self.lift.current_floor - 0.5) * self.floor_height # this gets the y coordinate for the lift rect
        LIFT_WIDTH = 50  # width of the lift rectangle

        # lift is positioned 20 px from right edge
        x2 = canvas_width - 20
        x1 = x2 - LIFT_WIDTH

        if self.lift_rect is None:
            self.lift_rect = self.canvas.create_rectangle(x1, y - 15, x2, y + 15, fill=GUI_LIFT_COLOUR, tags="lift")
        else:
            self.canvas.coords(self.lift_rect, x1, y - 15, x2, y + 15)

        # display the number of people onboard inside the lift rectangle
        onboard_count = len(self.lift.onboard_requests)
        if not hasattr(self, 'lift_text') or self.lift_text is None:
            self.lift_text = self.canvas.create_text(
                (x1 + x2) // 2, y,
                text=str(onboard_count),
                fill=GUI_LIFT_TEXT_COLOUR,
                font=(GUI_LIFT_TEXT_FONT, GUI_LIFT_TEXT_FONT_SIZE, "bold"),
                tags="lift_text"
            )
        else:
            self.canvas.itemconfig(self.lift_text, text=str(onboard_count))
            self.canvas.coords(self.lift_text, (x1 + x2) // 2, y)


    def update_waiting_indicators(self):
        """
        Draws little circles on each floor representing the number of waiting people,
        positioned so that they do not overlap the floor numbers.
        """
        # reset waiting indicators
        self.canvas.delete("waiting")
        
        # get waiting request count per floor, to draw circles
        waiting_counts = {}
        for req in self.lift.request_queue.get_requests():
            waiting_counts[req.origin_floor] = waiting_counts.get(req.origin_floor, 0) + 1

        # draw circles for waiting requests
        for floor, count in waiting_counts.items():
            canvas_height = int(self.canvas["height"])
            y = canvas_height - (floor - 0.5) * self.floor_height

            start_x = 60  
            radius = 5
            for i in range(count):
                circle_x = start_x + i * (2 * radius + 2)
                self.canvas.create_oval(
                    circle_x - radius, y - radius,
                    circle_x + radius, y + radius,
                    fill="red", tags="waiting"
                )

    def __gui_display_lift_direction(self, lift_direction) -> str:
        direction_display: dict = {Direction.UP: "up  ", Direction.DOWN : "down", Direction.NONE : "none"}
        return direction_display[lift_direction]

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
                f"Direction: {self.__gui_display_lift_direction(self.lift.direction)}\n"
                f"Waiting: {len(self.lift.request_queue.get_requests())}\n"
                f"Onboard: {len(self.lift.onboard_requests)}\n"
                f"Stopping: {"Yes" if self.lift.current_floor_stop else "No"}\n"
            )
            self.status_label.config(text=status_text)
            
            # next step after delay_ms milliseconds, depending on whether the lift needed to stop at current floor
            delay_ms: int = STEP_DELAY_MS + LIFT_STOP_DELAY_MS * self.lift.current_floor_stop
            self.master.after(delay_ms, self.simulation_step)
        else:
            self.status_label.config(text="Simulation finished!")
            self.start_button.config(state="normal")
    
    def start_simulation(self):
        self.start_button.config(state="disabled") # should not be able to press start button once the simulation has been started
        self.simulation_step()
