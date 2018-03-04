"""
PlotPlayer - A functional based animation viewer using Matplotlib

Public Classes:
  * PlotPlayer - Displays an animation in a Matplotlib Figure Window
"""
import numpy

from .helpers import ui_helper
from .data_models.animation_params import AnimationParams
from .managers import window_manager, render_manager, animation_manager, input_manager

class PlotPlayer(object):
    """
    Function based animation player for Matplotlib

    Static Methods:
      * show_players - Shows all instantiated Pyplot Figures (even ones not created by PlotPlayer)

    Public Methods:
      * initialize - Initialize the PlotPlayer instance for animation playback
      * play - Begin playback
      * stop - Stop playback
      * get_window_manager - Returns the WindowManager for the PlotPlayer Instance
      * get_render_manager - Returns the RenderManager for the PlotPlayer Instance
      * get_animation_manager - Returns the AnimationManager for the PlotPlayer Instance
      * get_input_manager - Returns the InputManager for the PlotPlayer Instance
    """
    _resolution_params = None
    _window_handler = None
    _render_handler = None
    _animation_handler = None
    _input_handler = None

    def __init__(self, window_handler=None, render_handler=None, animation_handler=None,
                 input_handler=None):
        """
        Constructor

        Parameters:
          * window_handler (optional) - Pre-setup WindowManager instance
          * render_handler (optional) - Pre-setup RenderManager instance
          * animation_handler (optional) - Pre-setup AnimationManager instance
          * input_handler (optional) - Pre-setup InputManager instance
        """
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

        self.initialize(1, self._render_logo)
        self.play()

    def initialize(self, total_frames, draw_func, animation_name=None):
        """
        Initialize the PlotPlayer instance for animation playback

        Parameters:
          * total_frames - The total frame count in the animation
          * draw_func - The external render method to call for reach frame rendering
          * animation_name (optional) - The name for the current animation
        """
        self.stop()

        self._render_handler.initialize(draw_func)

        animation_params = AnimationParams(total_frames, animation_name=animation_name)
        self._animation_handler.initialize(animation_params)
        self._input_handler.set_enabled(True)

    def play(self):
        """
        Method to begin playback
        """
        self._animation_handler.play()

    def stop(self):
        """
        Method to stop playback
        """
        self._animation_handler.stop()

    def get_window_manager(self):
        """
        Returns the WindowManager for the PlotPlayer
        """
        return self._window_handler

    def get_render_manager(self):
        """
        Returns the RenderManager for the PlotPlayer
        """
        return self._render_handler

    def get_animation_manager(self):
        """
        Returns the AnimationManager for the PlotPlayer
        """
        return self._animation_handler

    def get_input_manager(self):
        """
        Returns the InputManager for the PlotPlayer
        """
        return self._input_handler

    def _render_logo(self, frame_num, axes):
        pass

    @staticmethod
    def show_players(blocking=True):
        """
        Show all Pyplot Figures (even those not created by PlotPlayer)
        """
        ui_helper.show_players(blocking)
