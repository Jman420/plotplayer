"""
PlotPlayer specific Input Manager Methods and Classes

Public Classes:
  * InputManager - Attaches to appropriate input events and handles their events.

Private Methods:
  * _handle_save_key_combo - Handles Save key combo mappings
  * _handle_navigation_keys - Handles Navigation key mappings
  * _handle_visibility_keys - Handles Visibility key mappings
"""

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

def _handle_save_key_combo(key, animation_handler):
    """
    Handle save key inputs

    Parmeters:
      * key - A string representation of the pressed key
      * animation_handler - An instance of AnimationManager class to be called based on the key
          inputs

    Returns a boolean indicating whether they key press is handled
    """
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

def _handle_navigation_keys(key, animation_handler, skip_size, jump_size):
    """
    Handle navigation key inputs

    Parameters:
      * key - A string representation of the pressed key
      * animation_handler - An instance of AnimationManager class to be called based on the key
          inputs
      * skip_size - Number of frames to skip ahead when skip keys are pressed
      * jump_size - Number of frames to jump ahead when jump keys are pressed

    Returns a boolean indicating whether they key press is handled
    """
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
        animation_handler.render(animation_handler.get_min_frame_num())
    elif key == GOTO_END_BUTTON:
        animation_handler.render(animation_handler.get_max_frame_number())
    elif key in TOGGLE_PLAY_BUTTON:
        animation_handler.toggle_playback()
    else:
        handled = False

    return handled

def _handle_visibility_keys(key, window_handler, render_handler):
    """
    Handle visibility toggle key inputs

    Parameters:
      * window_handler - An instance of WindowManager class to be called based on key inputs
      * render_handler - An instance of RenderManager class to be called based on key inputs

    Returns a boolean indicating whether they key press is handled
    """
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
    """
    User Input Handler for PlotPlayer Windows

    See PlotPlayer Readme for default keymappings

    Public Methods:
      * handle_slider_changed - Method to handle scrubber slider changed events; needs to be
          attached to appropriate slider on_changed event
      * set_enabled - Method to enable/disable an InputManager instance

    Private Methods:
      * _handle_key_press - Method to handle key presses; attached to Matplotlib key_press_event.
      * _handle_key_release - Method to handle key releases; attached to Matplotlib
          key_release_event.
      * _handle_mouse_button_down - Method to handle mouse button down events; attached to
          Matplotlib button_press_event.

    Overriding Default Keymappings:
      * Provide a method as key_press_handler parameter in constructor; this method will be called
          on the Matplotlib key_press_event
      * Provided method should return True in order to prevent processing default keymappings
    """

    _window_handler = None
    _render_handler = None
    _animation_handler = None
    
    _key_press_handler = None
    
    _skip_size = None
    _jump_size = None

    _handler_enabled = False
    _save_button_pressed = False

    #pylint: disable=too-many-arguments
    def __init__(self, window_handler, render_handler, animation_handler, key_press_handler=None,
                 skip_size=SKIP_SIZE, jump_size=JUMP_SIZE, enabled=False):
        """
        Constructor

        Parameters:
          * window_handler - An instance of WindowManager class associated with the InputManager
              instance
          * render_handler - An instance of RenderManager class associated with the InputManager
              instance
          * animation_handler - An instance of AnimationManager class associated with the
              InputManager instance
          * key_press_handler (optional) - A method allowing for custom keymappings and input
              handling
          * skip_size (optional) - A number representing the number of frames difference for Skip
              key mappings
          * jump_size (optional) - A number representing the number of frames difference for Jump
              key mappings
          * enabled (optional) - Boolean indicating whether the InputManager is enabled
        """
        self._window_handler = window_handler
        self._render_handler = render_handler
        self._animation_handler = animation_handler
        self._key_press_handler = key_press_handler
        self._skip_size = skip_size
        self._jump_size = jump_size
        self._save_button_pressed = False

        self.set_enabled(enabled)

        figure = self._window_handler.get_figure()
        figure.canvas.mpl_connect('button_press_event', self._handle_mouse_button_down)
        figure.canvas.mpl_connect('key_press_event', self._handle_key_press)
        figure.canvas.mpl_connect('key_release_event', self._handle_key_release)

        slider = self._render_handler.get_slider()
        slider.on_changed(self.handle_slider_changed)

    def _handle_key_press(self, event_data):
        """
        Handle Matplotlib key_press_event for a WindowManager instance

        Parameters:
          * event_data - An object representing the key press event data
        """
        if not self._handler_enabled:
            return

        if self._key_press_handler is not None and self._key_press_handler(event_data):
            return

        key = event_data.key
        if self._save_button_pressed and _handle_save_key_combo(key, self._animation_handler):
            return

        if _handle_navigation_keys(key, self._animation_handler, self._skip_size, self._jump_size):
            return

        if _handle_visibility_keys(key, self._window_handler, self._render_handler):
            return

        if key == SAVE_BUTTON:
            self._save_button_pressed = True

    def _handle_key_release(self, event_data):
        """
        Handle Matplotlib key_release_event for WindowManager Instance

        Parameters:
          * event_data - An object representing the key press event data
        """
        if not self._handler_enabled:
            return

        key = event_data.key

        if key == SAVE_BUTTON:
            self._save_button_pressed = False

    def _handle_mouse_button_down(self, event_data):
        """
        Handle Matplotlib button_press_event for WindowManager Instance

        Parameters:
          * event_data - An object representing the key press event data
        """
        if not self._handler_enabled:
            return

        if event_data.inaxes == self._render_handler.get_slider_axes():
            self._animation_handler.stop()

    def handle_slider_changed(self, slider_val):
        """
        Handle Scrubber slider changed event

        Parameters:
          * slider_val - A number representing the new slider value
        """
        if not self._handler_enabled:
            return

        min_frame_num = self._animation_handler.get_min_frame_num()
        total_frame_count = self._animation_handler.get_max_frame_number() - min_frame_num
        frame_num = slider_val * total_frame_count + min_frame_num

        self._animation_handler.render(frame_num)

    def set_enabled(self, enabled):
        """
        Enable/Disable the input functionality for an InputManager instance

        Parameters:
          * enabled - Boolean indicating whether the InputManager instance is enabled
        """
        self._handler_enabled = enabled
