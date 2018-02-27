from matplotlib.widgets import Slider

IMAGE_AXES_RECT = [0, 0.03, 1, 0.97]  # [ x, y, width, height ] in percentage of window size
SLIDER_AXES_RECT = [0, 0, 1, 0.03]  # [ x, y, width, height ] in percentage of window size
SLIDER_BACKGROUND_COLOR = 'lightgoldenrodyellow'

class RenderManager(object):
    """Render Handler for PlotPlayer Viewer"""

    _figure = None
    _animation_axes = None
    _render_func = None
    _slider_axes = None
    _slider = None
    _slider_visible = False

    #pylint: disable=too-many-arguments
    def __init__(self, figure, animation_axes=None, slider_axes=None,
                 slider_background_color=SLIDER_BACKGROUND_COLOR, slider_visible=True):
        self._figure = figure

        if animation_axes is None:
            animation_axes = self._figure.add_axes(IMAGE_AXES_RECT)
            animation_axes.set_axis_off()
        self._animation_axes = animation_axes

        if slider_axes is None:
            slider_axes = self._figure.add_axes(SLIDER_AXES_RECT, facecolor=slider_background_color)
        self._slider_axes = slider_axes

        self.set_slider_visible(slider_visible)

    def initialize_render(self, render_func):
        self._render_func = render_func

    def initialize_slider(self, total_frames, slider_changed_handler):
        self._slider = Slider(self._slider_axes, str(), 0, total_frames - 1, valinit=0.0)
        self._slider.on_changed(slider_changed_handler)

    def render(self, frame_num):
        self.render_slider(frame_num)
        self.render_frame(frame_num)

    def render_frame(self, frame_num):
        self._figure.sca(self._animation_axes)
        self._render_func(frame_num, self._animation_axes)
        self._figure.canvas.draw_idle()

    def render_slider(self, new_slider_val):
        current_frame_num = int(self._slider.val)
        if current_frame_num != new_slider_val:
            self._slider.set_val(new_slider_val)

    def set_slider_visible(self, visible):
        self._slider_axes.set_visible(visible)
        self._figure.canvas.draw()
        self._slider_visible = visible

    def toggle_slider(self):
        self.set_slider_visible(not self._slider_visible)

    def get_animation_axes(self):
        return self._animation_axes

    def get_slider_axes(self):
        return self._slider_axes
