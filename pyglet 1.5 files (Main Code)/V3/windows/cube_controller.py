import logging
from pyglet.window import key
from windows.window import window
from objects.visuals import rubik_cube_moves, move_template
from objects.parser import double_moves_to_moves, double_move_to_move, prime
from objects.actions import action, main_action, in_line_action, func_action
from utilities.cube_utilities import wide, scramble_generator
from utilities.general_utilities import extend

logger = logging.getLogger(__name__)


class cube_controller(window):
    def __init__(self, *args, cube_moves: rubik_cube_moves,
                 scrambler: scramble_generator, **kwargs):
        super().__init__(*args, **kwargs)
        self.scrambler = scrambler
        self.cube_moves = cube_moves
        self.move_ids = {getattr(key, i): i for i in self.cube_moves.base_moves}
        self.new_move: (move_template | None) = None
        self.move_buffer: list[move_template] = []
        self.number = 0
        self.move_flag = action()
        self.scrambles = 0
        self.solves = 0
        self.stack: list[move_template] = []

    @extend
    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case key.BACKSPACE:
                self.reverse_last_move()
            case key.O:
                self.stack_solve()
            case key.I:
                self.test_move_sequence("R U R' U' " * 6)
            case key.P:
                self.full_scramble()
            case key.J:
                self.single_random_move()
            case _:
                self.number_check(symbol)
                self.cube_move(symbol, modifiers & key.MOD_SHIFT)

    def on_key_release(self, symbol: int, modifiers: int):
        self.number_check(symbol, press=False)

    def single_random_move(self):
        move_flag = in_line_action("RANDOM MOVE", "Random move")
        move = next(iter(self.scrambler))
        self.force_moves_str(move_flag, double_move_to_move(move))

    def full_scramble(self):
        self.scrambles += 1
        moves = list(iter(self.scrambler))
        text = f"Scramble {self.scrambles}: {' '.join(moves)}"
        move_flag = main_action("SCRAMBLE", "Scrambling...", text)
        self.force_moves_str(move_flag, *double_moves_to_moves(moves))

    def test_move_sequence(self, sequence: str):
        moves = sequence.strip().split(" ")
        text = f"Moves: {sequence}"
        move_flag = main_action("USER SEQUENCE", "Sequence...", text)
        self.force_moves_str(move_flag, *double_moves_to_moves(moves))

    def reverse_last_move(self):
        # Rework this
        if self.stack and not self.move_buffer:
            move_flag = in_line_action("REVERSE MOVE", "Move reversed", False)
            move = self.stack.pop(-1).get_reverse_move()
            self.force_moves(move_flag, move)
        else:
            # Rework this
            def temp():
                print("No moves to reverse")
            move_flag = func_action(temp)
            self.force_moves_str(move_flag)

    def stack_solve(self):
        # Rework this
        if self.stack:
            self.solves += 1
            moves = [move.get_reverse_move() for move in self.stack[::-1]]
            text = f"Solution {self.solves}: {' '.join(move.name for move in moves)}"
            move_flag = main_action("STACK SOLVE", "Solving (via a stack)...", text, False)
            self.force_moves(move_flag, *moves)
            self.stack.clear()
        else:
            # Rework this
            def temp():
                print("No moves to reverse")
            move_flag = func_action(temp)
            self.force_moves_str(move_flag)

    def force_moves(self, move_flag: action, *moves: move_template):
        # Rework this
        if not self.move_buffer:
            self.move_flag = move_flag
            self.move_buffer = list(moves)
            logger.debug(self.move_flag.ID)

    def force_moves_str(self, move_flag: action, *moves: str):
        # Rework this
        if not self.move_buffer:
            self.move_flag = move_flag
            self.move_buffer = [self.cube_moves[move] for move in moves]
            logger.debug(self.move_flag.ID)

    def number_check(self, symbol: int, press=True):
        if 1 < (number := symbol - 48) < 10:
            if press:
                self.number = number
            elif self.number == number:
                self.number = 0

    # Some of the more advanced key combinations have issue
    # For example 6Uw, 4Rw, 5Rw
    # After testing this is most likely due to key rollover/key jamming
    # Pressing 4-5-6-D also doesn't work for example
    # Pressing 6Uw then releasing 6 or w does work however
    def cube_move(self, symbol: int, shift: (int | bool)):
        if symbol in self.move_ids:
            wide_flag = self.keys[key.W]
            str_move = self.move_ids[symbol]
            str_move = wide(str_move, wide_flag, self.number)
            str_move += "'" if shift else ""    # Prime move
            if str_move in self.cube_moves:
                self.new_move = self.cube_moves[str_move]
                self.add_to_stack(self.new_move)
                logger.debug(repr(self.new_move))

    def add_to_stack(self, move: move_template):
        true_move = move.get_true_move()
        str_prime_move = prime(true_move.name)
        prime_move = self.cube_moves[str_prime_move]
        self.stack.append(prime_move)



if __name__ == "__main__":
    import pyglet as py
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s [%(levelname)s] %(message)s")
    dim = 7
    cube_controller(width=240, height=160, caption="cube_controller test",
                    cube_moves=rubik_cube_moves(dim),
                    scrambler=scramble_generator(dim),
                    exclusive_mouse=False, x=0.95, y=0.99)
    py.app.run()







