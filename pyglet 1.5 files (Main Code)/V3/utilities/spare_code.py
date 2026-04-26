def _1(kwargs):
    """Remove final redundant keys from kwargs for window class."""
    kwarg_keys = {"width", "height", "caption", "resizable", "style", "fullscreen", "visible",
                  "vsync", "display", "screen", "config", "context", "mode"}
    # Need to first remove leftover keys from mro so the final subclass doesn't
    # need a specific inheritance order for its superclasses, an issue of
    # diamond inheritance.
    for item in (kwargs.keys() - kwarg_keys):
        kwargs.pop(item)
    # Now we can call super safely
    # Must pass dim via the mro to the other superclass of main
    # To ensure the inheritance is invariant to permutation,
    # a workaround has been used in the window class