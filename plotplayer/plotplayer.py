from .helpers import ui_helper
from .managers import window_manager, render_manager, animation_manager, input_manager

class PlotPlayer(object):
    """Function based animation player for Matplotlib"""
    _window_handler = None
    _render_handler = None
    _animation_handler = None
    _input_handler = None

    def __init__(self, window_handler=None, render_handler=None, animation_handler=None,
                 input_handler=None):
        if window_handler is None:
            window_handler = window_manager.WindowManager()
        self._window_handler = window_handler
        figure = self._window_handler.get_figure()

        if render_handler is None:
            render_handler = render_manager.RenderManager(figure)
        self._render_handler = render_handler

        if animation_handler is None:
            animation_handler = animation_manager.AnimationManager(figure, self._render_handler)
        self._animation_handler = animation_handler

        if input_handler is None:
            input_handler = input_manager.InputManager(self._window_handler, self._render_handler,
                                                       self._animation_handler)
        self._input_handler = input_handler

    def initialize(self, total_frames, draw_func,
                   animation_name=animation_manager.DEFAULT_ANIMATION_NAME):
        self.stop()

        self._render_handler.initialize_render(draw_func)
        self._render_handler.initialize_slider(total_frames,
                                               self._input_handler.handle_slider_changed)
        self._animation_handler.initialize(total_frames, animation_name=animation_name)
        self._input_handler.set_enabled(True)

    def play(self):
        self._animation_handler.play()

    def stop(self):
        self._animation_handler.stop()

    def toggle_playback(self):
        if self._animation_handler.is_playing():
            self.stop()
        else:
            self.play()

    def get_window_manager(self):
        return self._window_handler

    def get_render_manager(self):
        return self._render_handler

    def get_animation_manager(self):
        return self._animation_handler

    def get_input_manager(self):
        return self._input_handler

    @staticmethod
    def show_players(blocking=True):
        ui_helper.show_players(blocking)
