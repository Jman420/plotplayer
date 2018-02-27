"""PlotPlayer specific input handler"""

SKIP_BACK_BUTTON = 'left'
SKIP_AHEAD_BUTTON = 'right'
JUMP_BACK_BUTTON = 'down'
JUMP_AHEAD_BUTTON = 'up'
TOGGLE_PLAY_BUTTON = [' ', 'enter']
GOTO_BEGINNING_BUTTON = 'home'
GOTO_END_BUTTON = 'end'
TOGGLE_SLIDER_BUTTON = 't'
TOGGLE_TOOLBAR_BUTTON = 'm'
SAVE_BUTTON = 'd'
SAVE_VIDEO_BUTTON = 'v'
SAVE_HTML_BUTTON = 'h'
SAVE_JAVASCRIPT_BUTTON = 'j'

KEYS_TRIGGER_STOP = [SKIP_BACK_BUTTON, SKIP_AHEAD_BUTTON, JUMP_BACK_BUTTON, JUMP_AHEAD_BUTTON,
                     GOTO_BEGINNING_BUTTON, GOTO_END_BUTTON]

SKIP_SIZE = 1
JUMP_SIZE = 10

def handle_save_key_combo(animation_handler, key):
    handled = True

    if key == SAVE_VIDEO_BUTTON:
        animation_handler.save_video()
    elif key == SAVE_HTML_BUTTON:
        animation_handler.save_html()
    elif key == SAVE_JAVASCRIPT_BUTTON:
        animation_handler.save_javascript()
    else:
        handled = False

    return handled

def handle_navigation_keys(key, animation_handler, skip_size, jump_size):
    handled = True

    if key in KEYS_TRIGGER_STOP:
        animation_handler.stop()

    current_frame_num = animation_handler.get_frame_number()
    if key == SKIP_BACK_BUTTON:
        animation_handler.render(current_frame_num - skip_size)
    elif key == SKIP_AHEAD_BUTTON:
        animation_handler.render(current_frame_num + skip_size)
    elif key == JUMP_BACK_BUTTON:
        animation_handler.render(current_frame_num - jump_size)
    elif key == JUMP_AHEAD_BUTTON:
        animation_handler.render(current_frame_num + jump_size)
    elif key == GOTO_BEGINNING_BUTTON:
        animation_handler.render(0)
    elif key == GOTO_END_BUTTON:
        animation_handler.render(animation_handler.get_total_frames())
    elif key in TOGGLE_PLAY_BUTTON:
        animation_handler.toggle_playback()
    else:
        handled = False

    return handled

def handle_visibility_keys(key, window_handler, render_handler):
    handled = True

    if key == TOGGLE_SLIDER_BUTTON:
        render_handler.toggle_slider()
    elif key == TOGGLE_TOOLBAR_BUTTON:
        window_handler.toggle_toolbar()
    else:
        handled = False

    return handled


#pylint: disable=too-many-instance-attributes
class InputManager(object):
    """User Input Handler for PlotPlayer Windows"""

    _window_handler = None
    _render_handler = None
    _animation_handler = None
    _handler_enabled = False
    _key_press_handler = None
    _save_button_pressed = False
    _skip_size = None
    _jump_size = None

    #pylint: disable=too-many-arguments
    def __init__(self, window_handler, render_handler, animation_handler, key_press_handler=None,
                 skip_size=SKIP_SIZE, jump_size=JUMP_SIZE, enabled=False):
        self._window_handler = window_handler
        self._render_handler = render_handler
        self._animation_handler = animation_handler
        self._key_press_handler = key_press_handler
        self._skip_size = skip_size
        self._jump_size = jump_size
        self._save_button_pressed = False

        self.set_enabled(enabled)

        figure = self._window_handler.get_figure()
        figure.canvas.mpl_connect('button_press_event', self.handle_mouse_button_down)
        figure.canvas.mpl_connect('key_press_event', self.handle_key_press)
        figure.canvas.mpl_connect('key_release_event', self.handle_key_release)

    def handle_key_press(self, event_data):
        if not self._handler_enabled:
            return

        if self._key_press_handler is not None and self._key_press_handler(event_data):
            return

        key = event_data.key
        if self._save_button_pressed and handle_save_key_combo(self._animation_handler, key):
            return

        if handle_navigation_keys(key, self._animation_handler, self._skip_size, self._jump_size):
            return

        if handle_visibility_keys(key, self._window_handler, self._render_handler):
            return

        if key == SAVE_BUTTON:
            self._save_button_pressed = True

    def handle_key_release(self, event_data):
        if not self._handler_enabled:
            return

        key = event_data.key

        if key == SAVE_BUTTON:
            self._save_button_pressed = False

    def handle_mouse_button_down(self, event_data):
        if not self._handler_enabled:
            return

        if event_data.inaxes == self._render_handler.get_slider_axes():
            self._animation_handler.stop()

    def handle_slider_changed(self, slider_val):
        frame_num = min(max(0, int(slider_val)), self._animation_handler.get_total_frames())

        self._animation_handler.render(frame_num)

    def set_enabled(self, enabled):
        self._handler_enabled = enabled
