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

def handle_save_key_combo(plotplayer, key):
    if key == SAVE_VIDEO_BUTTON:
        plotplayer.save_video()
    elif key == SAVE_HTML_BUTTON:
        plotplayer.save_html()
    elif key == SAVE_JAVASCRIPT_BUTTON:
        plotplayer.save_javascript()


class InputHandler(object):
    """User Input Handler for PlotPlayer Windows"""

    plotplayer = None
    handler_enabled = False
    key_press_handler = None
    save_button_pressed = False
    skip_size = jump_size = None

    def __init__(self, plotplayer, key_press_handler=None, skip_size=SKIP_SIZE,
                 jump_size=JUMP_SIZE, enabled=False):
        self.plotplayer = plotplayer
        self.key_press_handler = key_press_handler
        self.skip_size = skip_size
        self.jump_size = jump_size
        self.save_button_pressed = False
        self.set_enabled(enabled)

        figure = self.plotplayer.get_figure()
        figure.canvas.mpl_connect('button_press_event', self.handle_mouse_button_down)
        figure.canvas.mpl_connect('key_press_event', self.handle_key_press)
        figure.canvas.mpl_connect('key_release_event', self.handle_key_release)

    def handle_key_press(self, event_data):
        if not self.handler_enabled or ():
            return

        if self.key_press_handler is not None and self.key_press_handler(event_data):
            return

        plotplayer = self.plotplayer
        key = event_data.key
        if self.save_button_pressed:
            handle_save_key_combo(plotplayer, key)

        if key in KEYS_TRIGGER_STOP:
            plotplayer.stop()

        current_frame = plotplayer.get_current_frame_number()
        if key == SKIP_BACK_BUTTON:
            plotplayer.render(current_frame - self.skip_size)
        elif key == SKIP_AHEAD_BUTTON:
            plotplayer.render(current_frame + self.skip_size)
        elif key == JUMP_BACK_BUTTON:
            plotplayer.render(current_frame - self.jump_size)
        elif key == JUMP_AHEAD_BUTTON:
            plotplayer.render(current_frame + self.jump_size)
        elif key == GOTO_BEGINNING_BUTTON:
            plotplayer.render(0)
        elif key == GOTO_END_BUTTON:
            plotplayer.render(plotplayer.get_total_frames())
        elif key == TOGGLE_SLIDER_BUTTON:
            plotplayer.toggle_slider()
        elif key in TOGGLE_PLAY_BUTTON:
            plotplayer.toggle_playback()
        elif key == TOGGLE_TOOLBAR_BUTTON:
            plotplayer.toggle_toolbar()
        elif key == SAVE_BUTTON:
            self.save_button_pressed = True

    def handle_key_release(self, event_data):
        if not self.handler_enabled:
            return

        key = event_data.key

        if key == SAVE_BUTTON:
            self.save_button_pressed = False

    def handle_mouse_button_down(self, event_data):
        if not self.handler_enabled:
            return

        plotplayer = self.plotplayer
        if event_data.inaxes == plotplayer.render_processor.slider_axes:
            plotplayer.stop()

    def set_enabled(self, enabled):
        self.handler_enabled = enabled
