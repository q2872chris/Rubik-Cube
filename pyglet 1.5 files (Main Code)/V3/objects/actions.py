from utilities.general_utilities import Timer


class action:
    def __init__(self, ID="", add_to_stack=True):
        self.ID = ID
        self.print_flag = False
        self.print_message = ""
        self.add_to_stack = add_to_stack
        self.sent = False

    def start(self):
        pass

    def end(self):
        pass


# Need to control printing, eg with double new lines.
# Also need to control sequences that are too long, maybe return strings.
class main_action(action):
    def __init__(self, ID="", start_message="", end_message="",
                 add_to_stack=True):
        super().__init__(ID=ID, add_to_stack=add_to_stack)
        self.start_message = "\n" + start_message
        self.end_message = end_message
        self.timer = Timer()

    def start(self):
        print(self.start_message)
        self.timer.start()

    def end(self):
        print(self.end_message)
        self.timer.end()        # Get timer to return text too
        print()


class in_line_action(action):
    def __init__(self, ID="", print_message="", add_to_stack=True):
        super().__init__(ID=ID, add_to_stack=add_to_stack)
        self.print_message = f" ({print_message})"
        self.print_flag = True


class func_action(action):
    def __init__(self, function, *args, **kwargs):
        super().__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def start(self):
        self.function(*self.args, **self.kwargs)

