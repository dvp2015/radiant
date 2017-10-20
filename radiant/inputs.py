from collections import defaultdict


# window managers should update these values
mouse_wheel_delta = [0., 0.]
mouse_position = (0., 0.)
input_string = ""

key_down = defaultdict(lambda: False)  # True if it was pressed in the current event loop iteration
key_held = defaultdict(lambda: False)  # True while a key is held down
key_up = defaultdict(lambda: False)  # True if it was released in the current event loop iteration

mouse_button_down = defaultdict(lambda: False)  # True if it was pressed in the current event loop iteration
mouse_button_held = defaultdict(lambda: False)  # True while a button is held down
mouse_button_up = defaultdict(lambda: False)  # True if it was released in the current event loop iteration


def tick():
    """Resets the per-frame values."""
    global mouse_wheel_delta, mouse_position, input_string
    mouse_wheel_delta[0] = 0.
    mouse_wheel_delta[1] = 0.
    mouse_position = (0., 0.)
    input_string = ""

    global key_down, key_up
    key_down.clear()
    key_up.clear()

    global mouse_button_down, mouse_button_up
    mouse_button_down.clear()
    mouse_button_up.clear()
