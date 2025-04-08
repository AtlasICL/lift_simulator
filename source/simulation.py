import tkinter as tk

from lift import Lift
from lift import Direction
from request_simulator import simulate_requests
from input_parser import parse_config


# CONSTANTS:

STEP_DELAY_MS: int = 500                             # delay between lift steps in ms
LIFT_STOP_DELAY_MS: int = 500                        # waiting time for lift stop at a floor
LIFT_DEFAULT_SPEED_FACTOR: float = 1.0               # default speed multiplier for the lift
LIFT_MIN_SPEED_FACTOR: float = 0.5                   # minimum speed multiplier for the lift
LIFT_MAX_SPEED_FACTOR: float = 3.0                   # maximum speed multiplier for the lift


GUI_BACKGROUND_COLOUR: str = "white"                 # background colour for the main window
GUI_WINDOW_TITLE: str = "Best Team Lift Simulator"   # window title
GUI_DEFAULT_FONT: str = "Arial"                      # default font used in the GUI

GUI_LIFT_COLOUR: str = "blue"                        # fill colour of the lift rectangle 

GUI_FLOOR_HEIGHT: int = 40                           # height of each floor

WAITING_INDICATOR_X_OFFSET: int = 60                 # x offset (in pixels) of the leftmost waiting indicator
# this is necessary, as otherwise the waiting indicators overlap with the floor numbers
WAITING_INDICATOR_RADIUS: int = 5                    # radius of waiting indicator circles

SPEED_SLIDER_LABEL: str = "Simulation speed"         # label for speed slider element

GUI_LIFT_TEXT_COLOUR: str = "white"                  # text colour for onboard counter in lift rectangle
GUI_LIFT_TEXT_FONT: str = GUI_DEFAULT_FONT           # text font for onboard counter in lift rectangle
GUI_LIFT_TEXT_FONT_SIZE: int = 13                    # text font size for onboard counter in lift rectangle

GUI_STATUS_TEXT_TITLE: str = "Lift Status"           # title for the status text
GUI_STATUS_TEXT_FONT: str = GUI_DEFAULT_FONT         # text font for status text (set to default, Arial)
GUI_STATUS_TEXT_FONT_SIZE: int = 14                  # text font size for status text

GUI_SIMULATION_FINISHED_TEXT: str = "Simulation finished!\n<3"


class LiftSimulatorGUI:
    def __init__(self, master, config_file):
        self.master = master
        self.master.title(GUI_WINDOW_TITLE)
        
        self.config = parse_config(config_file)
        self.total_floors: int = self.config["total_floors"]
        self.capacity: int = self.config["capacity"]
        self.num_requests: int = self.config["num_requests"]

        self.speed_multiplier = tk.DoubleVar(value=LIFT_DEFAULT_SPEED_FACTOR)

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
        
        # Initialize lift_rect before drawing elements
        self.lift_rect = None
        
        # create and render all the visual elements
        self._draw_all_elements()


    def _draw_status_label(self) -> None:
        self.status_label = tk.Label(self.info_frame, text=GUI_STATUS_TEXT_TITLE, font=(GUI_STATUS_TEXT_FONT, GUI_STATUS_TEXT_FONT_SIZE))
        self.status_label.pack(pady=10)


    def _draw_start_button(self) -> None:
        self.start_button = tk.Button(self.info_frame, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack(pady=10)


    def _draw_add_requests_button(self) -> None:
        self.add_requests_button = tk.Button(self.info_frame, text="Add new requests", command=lambda: self._add_requests(5))
        self.add_requests_button.pack(pady=10)
        self.add_requests_button.config(state="disabled")  # should not be able to add new requests before simulation has started


    def _draw_building(self):
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


    def _draw_all_elements(self) -> None:
        self._draw_status_label()
        self._draw_start_button()
        self._draw_add_requests_button()
        self._create_speed_slider()
        self._draw_building()
        self._draw_lift()
        self._update_status("Simulation not started yet.")

    
    def _create_speed_slider(self) -> None:
        self.speed_slider = tk.Scale(
            self.info_frame,
            from_=LIFT_MIN_SPEED_FACTOR, 
            to=LIFT_MAX_SPEED_FACTOR,
            resolution=0.25,
            orient="horizontal",
            label=SPEED_SLIDER_LABEL,
            variable=self.speed_multiplier,
            command=self._update_speed_multiplier 
        )
        self.speed_slider.pack(pady=10)
        self.speed_slider.config(state="disabled") # not active before start of simulation
        self.speed_slider.pack(pady=10)

    
    def _update_lift_position(self) -> None:
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


    def _get_waiting_counters(self) -> dict[int, int]:
        """
        Returns a dictionary of type [int, int], which represents the number of people (requests) waiting on each floor.
        Example: {1: 3, 2: 7, 3: 0}
        """
        waiting_counts = {}
        for req in self.lift.request_queue.get_requests():
            waiting_counts[req.origin_floor] = waiting_counts.get(req.origin_floor, 0) + 1
        return waiting_counts
    

    def _draw_waiting_indicators(self, waiting_counts: dict[int, int]) -> None:
        for floor, count in waiting_counts.items():
            canvas_height = int(self.canvas["height"])
            y = canvas_height - (floor - 0.5) * self.floor_height
            start_x = WAITING_INDICATOR_X_OFFSET  
            radius = WAITING_INDICATOR_RADIUS
            for i in range(count):
                circle_x = start_x + i * (2 * radius + 2)
                self.canvas.create_oval(circle_x-radius, y-radius, circle_x+radius, y+radius, fill="red", tags="waiting")
    

    def _update_waiting_indicators(self) -> None:
        """
        Draws little circles on each floor representing the number of waiting people,
        positioned so that they do not overlap the floor numbers.
        """
        self.canvas.delete("waiting") # reset waiting indicators
        waiting_counts: dict[int, int] = self._get_waiting_counters() # get waiting counts
        self._draw_waiting_indicators(waiting_counts) # draw waiting indicators


    def _gui_display_lift_direction(self, lift_direction) -> str:
        """Helper function for printing lift direction."""
        direction_display: dict = {Direction.UP: "up  ", Direction.DOWN : "down", Direction.NONE : "none"}
        return direction_display[lift_direction]
    

    def _add_requests(self, n: int) -> None:
        """This function adds n new requests for the lift."""
        new_requests = simulate_requests(n_requests=n, max_floor=self.total_floors)
        for req in new_requests:
            self.requests.append(req)
            self.lift.request_queue.add_request(req)

    
    def _update_speed_multiplier(self, val: float) -> None:
        self.speed_multiplier = tk.DoubleVar(value=val)


    def _get_step_delay_ms(self) -> int:
        """Returns delay before next step in ms"""
        delay: float = (STEP_DELAY_MS + LIFT_STOP_DELAY_MS * self.lift.current_floor_stop) * (1.0/self.speed_multiplier.get())
        return int(delay) # number of ms (as an int)
    

    def _get_status_text(self) -> str:
        """Returns the text to be displayed on top right for current lift status."""
        status_text = (
            f"----------- Status -----------\n\n"
            f"Current Floor: {self.lift.current_floor}\n"
            f"Direction: {self._gui_display_lift_direction(self.lift.direction)}\n"
            f"Waiting: {len(self.lift.request_queue.get_requests())}\n"
            f"Onboard: {len(self.lift.onboard_requests)}\n"
            f"Stopping: {"Yes" if self.lift.current_floor_stop else "No"}\n"
            f"People getting on: {"Yes" if self.lift.currently_onboarding else "No"}\n"
            f"People getting off: {"Yes" if self.lift.currently_offboarding else "No"}\n"
            f"\n-------------------------------\n"
        )
        return status_text


    def _update_status(self, text: str) -> None:
        """Updates the status label text."""
        self.status_label.config(text=text)


    def _draw_lift(self) -> None:
        """Initialise the lift component."""
        self._update_lift_position()


    def _destroy_buttons_and_sliders(self) -> None:
        """Destroys the different buttons and the speed slider at end of simulation."""
        self.start_button.destroy()
        self.add_requests_button.destroy()
        self.speed_slider.destroy()


    def simulation_step(self) -> None:
        """Performs a simulation step and schedules the next one."""
        # the following if statement checks whether there is, either at least 1 request still remaining,
        # or at least 1 person still on the lift; if so, we go through the logic
        if self.lift.request_queue.get_requests() or self.lift.onboard_requests:
            self.lift.move() # simulation goes forward by 1 move
            self._update_lift_position() # update the position of the lift
            self._update_waiting_indicators() # update the little circles of people waiting on each floor
            
            # update status label (on the right) with current info
            status_text = self._get_status_text()
            self.status_label.config(text=status_text)
            
            delay_ms = self._get_step_delay_ms()
            self.master.after(delay_ms, self.simulation_step)
        else:
            self.status_label.config(text=GUI_SIMULATION_FINISHED_TEXT)
            self._destroy_buttons_and_sliders()


    def start_simulation(self) -> None:
        self.start_button.config(state="disabled") # should not be able to press start button once the simulation has been started
        self.add_requests_button.config(state="normal") # can now add new requests
        self.speed_slider.config(state="normal") # can now change speed
        self.simulation_step()
