from pyglet.window import key
from windows.renderer import renderer
from windows.cube_controller import cube_controller
from objects.objects3d import rubik_cube_generator
from objects.engine import engine
from objects.visuals import rubik_cube_moves, move_template
from objects.actions import action, func_action
from utilities.cube_utilities import scramble_generator, rubik_cube_diagonal
from utilities.general_utilities import extend, get_quadrant

END = action("END SEQUENCE")


class main_controller(renderer, cube_controller):
    def __init__(self, *args, dim: int, cube_width: float, gap: float,
                 start_speed: int, start_position: (tuple | None) = None, **kwargs):
        # Attributes to initialise and pass up the inheritance chain via super:
        if start_position is None:
            corner_position = rubik_cube_diagonal(dim, cube_width, gap)
            start_position = corner_position * 1.7
        cube_moves = rubik_cube_moves(dim)
        cube_moves.update_quadrant(get_quadrant(start_position))
        scrambler = scramble_generator(dim)
        super().__init__(*args, start_position=start_position, cube_moves=cube_moves,
                         scrambler=scrambler, **kwargs)
        cubes = rubik_cube_generator(self.batch_3D, dim, cube_width, gap)
        self.engine = engine(cubes)
        self.update_speed_func(speed=start_speed, print_info=False)

    def check_quadrant(self):
        if (quadrant := self.camera.check_quadrant()) is not None:
            self.send_action(func_action(self.cube_moves.update_quadrant, quadrant))

    def toggle_move_timer(self):
        self.send_action(func_action(self.engine.toggle_move_timer))

    def update_speed_func(self, speed=6, inc=False, dec=False, print_info=True):
        self.engine.update_speed(speed, inc, dec, print_info)
        self.cube_moves.update_speed(self.engine.frame_speed)

    def update_speed(self, inc=False, dec=False):
        self.send_action(func_action(self.update_speed_func, inc=inc, dec=dec))

    @extend
    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case key.T:
                self.toggle_move_timer()
            case key.EQUAL:
                self.update_speed(inc=True)
            case key.MINUS:
                self.update_speed(dec=True)
            case key.G:
                pass    # Grid
            case key.BRACKETRIGHT:
                pass
            case key.BRACKETLEFT:
                pass

    @extend
    def update(self, dt: float):
        self.update_move_buffer()
        self.engine.run()
        self.check_quadrant()

    # Rework the buffer system!!!!!!
    # (main/cube_controller/engine)
    def update_move_buffer(self):
        if self.new_move is not None:
            self.engine.update_move_buffer(self.new_move)
            self.new_move = None
        if self.move_buffer and self.engine.move is None:
            if not self.move_flag.sent:
                self.send_action(self.move_flag)
                self.move_flag.sent = True
            move = self.move_buffer.pop(0)
            self.send_action(move)
            if self.move_flag.add_to_stack:
                self.add_to_stack(move)
            if not self.move_buffer:
                self.send_action(END)
        elif isinstance(self.move_flag, func_action):
            self.send_action(self.move_flag)
            self.move_flag = None

    def send_action(self, new_action: (action | move_template)):
        self.engine.update_move_buffer(new_action, override=True)





