"""
PlotPlayer specific Render Manager Methods and Classes

Public Classes:
  * RenderManager - Manages the Scrubber Slider and Animation Axes used as canvases; manages the
      external render function that renders the animation frames
"""

from matplotlib.widgets import Slider

IMAGE_AXES_RECT = [0, 0.03, 1, 0.97]  # [ x, y, width, height ] in percentage of window size
SLIDER_AXES_RECT = [0, 0, 1, 0.03]  # [ x, y, width, height ] in percentage of window size
SLIDER_BACKGROUND_COLOR = 'lightgoldenrodyellow'

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
    _animation_axes = None
    _render_func = None
    _slider_axes = None
    _slider = None
    _slider_visible = False

    #pylint: disable=too-many-arguments
    def __init__(self, figure, animation_axes=None, slider_axes=None,
                 slider_background_color=SLIDER_BACKGROUND_COLOR, slider_visible=True):
        """
        Constructor

        Parameters:
          * figure - Instance of Pyplot figure associated with the draw canvas
          * animation_axes (optional) - a pre-setup axes to be used for the animation canvas
          * slider_axes (optional) - a pre-setup axes to be used for the slider canvas
          * slider_background_color (optional) - specifies the background color for the slider
          * slider_visible (optional) - boolean indicated whether the slider is visible
        """
        self._figure = figure

        if animation_axes is None:
            animation_axes = self._figure.add_axes(IMAGE_AXES_RECT)
            animation_axes.set_axis_off()
        self._animation_axes = animation_axes

        if slider_axes is None:
            slider_axes = self._figure.add_axes(SLIDER_AXES_RECT, facecolor=slider_background_color)
        self._slider_axes = slider_axes
        self._slider = Slider(self._slider_axes, str(), 0, 1, valinit=0.0)

        self.set_slider_visible(slider_visible)

    def initialize(self, render_func):
        """
        Initialize the Render Manager for rendering

        Parameters:
          * render_func - The function to perform the render
        """
        self._render_func = render_func

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
        self._render_slider(slider_val)
        self._render_frame(frame_num)

    def set_slider_visible(self, visible):
        """
        Hide/Show the Scrubber Slider

        Parameters:
          * visible - Boolean specifying whether the Slider is visible
        """
        self._slider_axes.set_visible(visible)
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
        return self._animation_axes

    def get_slider_axes(self):
        """
        Returns the Slider Axes
        """
        return self._slider_axes

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
        self._figure.sca(self._animation_axes)
        self._render_func(frame_num, self._animation_axes)
        self._figure.canvas.draw_idle()

    def _render_slider(self, new_slider_val):
        """
        Render the Scrubber Slider

        Parameters:
          * new_sider_val - New value to render the Scrubber Slider with
        """
        if self._slider.val != new_slider_val:
            self._slider.set_val(new_slider_val)
