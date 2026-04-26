import numpy as np
from objects.visuals import move_template
from objects.actions import action, func_action
from utilities.cube_utilities import speed_bound, frame_speed
from utilities.general_utilities import Timer


class engine:
    def __init__(self, cubes: np.ndarray, print_move_info=True):
        self.cubes = cubes
        self.move: (move_template | None) = None
        self.move_buffer = []
        self.move_buffer_limit = 3
        self.frame = 0
        self.speed = 6    # Will be updated in main
        self.frame_speed = frame_speed(self.speed)
        self.move_count = 0
        self.print_move_info = print_move_info
        self.move_flag: (action | None) = None
        self.move_timer = Timer()
        self.move_timer_flag = False

    def run(self):
        if self.move is None and self.move_buffer:
            self.new_move()
        if self.move is not None:
            self.move.initialise_rotation(self.cubes)
            self.active_move()

    def new_move(self):
        # Rework this
        new_action = self.move_buffer.pop(0)
        if isinstance(new_action, action):
            if new_action.ID == "END SEQUENCE":
                self.move_flag.end()
                self.move_flag = None
            elif isinstance(new_action, func_action):
                new_action.start()
            else:
                new_action.start()
                self.move_flag = new_action
        else:
            self.move = new_action
            self.move_timer.start()

    def active_move(self):
        self.frame += self.frame_speed
        self.move.rotate_vertices()
        if self.frame == 90:
            self.cubes = self.move.rotate_array(self.cubes)
            self.print_info()  # Must be run before self.move is set to None
            self.frame = 0
            self.move = None

    # Needs more string formatting!!
    def print_info(self):
        if self.move_flag is None or self.move_flag.print_flag:
            self.move_count += 1
            if self.print_move_info:
                message = str(self.move_count)
                if self.move_flag is not None:
                    message += self.move_flag.print_message
                message += ": " + self.move.name
                message = f"Move {message : <25}"
                message += f"[current quadrant: {str(self.move.quadrant) : >8}]"
                print(message, end="\t\t")
                if self.move_timer_flag:    # Rework this
                    self.move_timer.end()      # Should return a string
                else:
                    print()

    def update_move_buffer(self, move: (action | move_template), override=False):
        if len(self.move_buffer) < self.move_buffer_limit or override:
            self.move_buffer.append(move)

    # Combine with add_new_line
    def toggle_move_timer(self):
        flag = self.move_timer_flag = not self.move_timer_flag
        print(f"Move timer {'' if flag else 'de'}activated")

    # Combine with add_new_line
    # Rework this
    def update_speed(self, new_speed=6, inc=False, dec=False, print_info=True):
        old_speed = self.speed
        if inc:
            self.speed = speed_bound(self.speed + 1)
        elif dec:
            self.speed = speed_bound(self.speed - 1)
        else:
            self.speed = speed_bound(new_speed)
        self.frame_speed = frame_speed(self.speed)
        if print_info:
            if old_speed != self.speed:
                print(f"New speed: {self.speed}/12")
            elif inc:
                print(f"Max speed already reached")
            elif dec:
                print(f"Min speed already reached")
            else:
                print(f"Speed unchanged")

    # To fill in
    def add_new_line(self):
        pass

    # To fill in
    # Need to deal with extra spaces from scramble text!
    def print_text(self, text: str):
        pass







