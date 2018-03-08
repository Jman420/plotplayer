"""
PlotPlayer specific Render Manager Methods and Classes

Public Classes:
  * RenderManager - Manages the Scrubber Slider and Animation Axes used as canvases; manages the
      external render function that renders the animation frames
"""

from matplotlib.widgets import Slider

from ..data_models.render_axes_params import RenderAxesParams
from ..data_models.slider_params import SliderParams

IMAGE_AXES_RECT = [0, 0.03, 1, 0.97]  # [ x, y, width, height ] in percentage of window size
SLIDER_AXES_RECT = [0, 0, 1, 0.03]  # [ x, y, width, height ] in percentage of window size

class RenderManager(object):
    """
    Render Manager for PlotPlayer Windows

    Public Methods:
      * initialize - Initializes the Render Manager for rendering
      * render - Render a specific frame from the external render function
      * set_slider_visible - Method to hide/show the Scrubber Slider
      * toggle_slider - Method to toggle the Scribber Slider between shown and hidden
      * get_animation_axes - Returns the Animation Axes
      * get_slider_axes - Returns the Slider Axes
      * get_slider - Returns the Scrubber Slider
    """

    _figure = None
    _render_axes_params = None
    _render_func = None
    _slider = None
    _slider_visible = False

    def __init__(self, figure, render_axes_params=None, scrubber_slider_params=None):
        """
        Constructor

        Parameters:
          * figure - Instance of Pyplot figure associated with the draw canvas
          * render_axes_params (optional) - Instance of RenderAxesParams
          * scrubber_slider_params (optional) - Instance of SliderParams
        """
        self._figure = figure

        if render_axes_params is None:
            render_axes_params = RenderAxesParams(None, None)

        if scrubber_slider_params is None:
            scrubber_slider_params = SliderParams()

        if render_axes_params.animation_axes is None:
            render_axes_params.animation_axes = self._figure.add_axes(IMAGE_AXES_RECT)

        if render_axes_params.slider_axes is None:
            slider_background_color = scrubber_slider_params.slider_background_color
            slider_axes = self._figure.add_axes(SLIDER_AXES_RECT,
                                                facecolor=slider_background_color)
            render_axes_params.slider_axes = slider_axes

        self._render_axes_params = render_axes_params
        self._scrubber_slider_params = scrubber_slider_params
        self._slider = Slider(render_axes_params.slider_axes, str(), 0, 1, valinit=0.0)

        self.set_slider_visible(scrubber_slider_params.slider_visible)
        self.initialize(None, True)

    def initialize(self, render_func, clear_animation=False):
        """
        Initialize the Render Manager for rendering

        Parameters:
          * render_func - The function to perform the render
        """
        if clear_animation:
            animation_axes = self.get_animation_axes()
            animation_axes.clear()
            animation_axes.set_axis_off()
            self._enforce_limits()

        self._render_func = render_func

    def set_limits(self, animation_x_limits=None, animation_y_limits=None):
        """
        Set the Animation Axes X/Y Limits
        """
        self._render_axes_params.animation_x_limits = animation_x_limits
        self._render_axes_params.animation_y_limits = animation_y_limits

        self._enforce_limits()

    def render(self, frame_num, total_frames):
        """
        Render a specific frame from a total set of frames

        Parameters:
          * frame_num - The frame number to render
          * total_frames - The total number of frames that could be rendered
        """
        if frame_num < 0 or frame_num > total_frames:
            return

        slider_val = frame_num / total_frames
        self._render_frame(frame_num)
        self._render_slider(slider_val)
        self._figure.canvas.draw_idle()

    def set_slider_visible(self, visible):
        """
        Hide/Show the Scrubber Slider

        Parameters:
          * visible - Boolean specifying whether the Slider is visible
        """
        self._render_axes_params.slider_axes.set_visible(visible)
        self._figure.canvas.draw()
        self._slider_visible = visible

    def toggle_slider(self):
        """
        Toggle the Slider Visibility between Shown and Hidden
        """
        self.set_slider_visible(not self._slider_visible)

    def get_animation_axes(self):
        """
        Returns the Animation Axes
        """
        return self._render_axes_params.animation_axes

    def get_slider_axes(self):
        """
        Returns the Slider Axes
        """
        return self._render_axes_params.slider_axes

    def get_slider(self):
        """
        Returns the Scrubber Slider
        """
        return self._slider

    def _render_frame(self, frame_num):
        """
        Render a frame from the external render function

        Parameters:
          * frame_num - The frame number to render
        """
        animation_axes = self.get_animation_axes()

        self._figure.sca(animation_axes)
        self._render_func(frame_num, animation_axes)

    def _render_slider(self, new_slider_val):
        """
        Render the Scrubber Slider

        Parameters:
          * new_sider_val - New value to render the Scrubber Slider with
        """
        if self._slider.val != new_slider_val:
            self._slider.set_val(new_slider_val)

    def _enforce_limits(self):
        animation_axes = self.get_animation_axes()
        animation_x_limits = self._render_axes_params.animation_x_limits
        animation_y_limits = self._render_axes_params.animation_y_limits

        if (animation_x_limits is None or animation_y_limits is None):
            animation_axes.autoscale(True)
        else:
            animation_axes.autoscale(False)
            animation_axes.set_xlim(animation_x_limits)
            animation_axes.set_ylim(animation_y_limits)
