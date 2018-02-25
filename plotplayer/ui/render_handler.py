from tkinter.constants import BOTTOM, X
from matplotlib.widgets import Slider

IMAGE_AXES_RECT = [0, 0.03, 1, 0.97]  # [ x, y, width, height ] in percentage of window size
SLIDER_AXES_RECT = [0, 0, 1, 0.03]  # [ x, y, width, height ] in percentage of window size
SLIDER_BACKGROUND_COLOR = 'lightgoldenrodyellow'

DEFAULT_FRAME_RATE = 30

class RenderHandler(object):
    """Render Handler for PlotPlayer Viewer"""

    player_figure = None
    animation_axes = render_func = None
    slider_axes = slider = None
    slider_visible = toolbar_visible = False

    def __init__(self, player_figure, animation_axes=None, slider_axes=None,
                 slider_background_color=SLIDER_BACKGROUND_COLOR, slider_visible=True,
                 toolbar_visible=False):
        self.player_figure = player_figure

        if animation_axes is None:
            animation_axes = self.player_figure.add_axes(IMAGE_AXES_RECT)
            animation_axes.set_axis_off()
        self.animation_axes = animation_axes

        if slider_axes is None:
            slider_axes = self.player_figure.add_axes(SLIDER_AXES_RECT,
                                                      facecolor=slider_background_color)
        self.slider_axes = slider_axes

        self.set_slider_visible(slider_visible)
        self.set_toolbar_visible(toolbar_visible)

    def initialize_rendering(self, total_frames, render_func):
        self.slider = Slider(self.slider_axes, str(), 0, total_frames - 1, valinit=0.0)
        self.slider.on_changed(self.handle_slider_changed)

        self.render_func = render_func

    def render(self, frame_num):
        frame_num = min(max(0, int(frame_num)), self.slider.valmax)

        self.render_slider(frame_num)
        self.render_frame(frame_num)

    def render_frame(self, frame_num):
        self.player_figure.sca(self.animation_axes)
        self.render_func(frame_num, self.animation_axes)
        self.player_figure.canvas.draw_idle()

    def render_slider(self, new_slider_val):
        current_frame_num = int(self.slider.val)
        if current_frame_num != new_slider_val:
            self.slider.set_val(new_slider_val)

    def handle_slider_changed(self, slider_val):
        self.render(slider_val)

    def set_slider_visible(self, visible):
        self.slider_axes.set_visible(visible)
        self.player_figure.canvas.draw()
        self.slider_visible = visible

    def toggle_slider(self):
        self.set_slider_visible(not self.slider_visible)

    def set_toolbar_visible(self, visible):
        if visible:
            self.player_figure.canvas.toolbar.pack(side=BOTTOM, fill=X)
        else:
            self.player_figure.canvas.toolbar.pack_forget()

        self.toolbar_visible = visible

    def toggle_toolbar(self):
        self.set_toolbar_visible(not self.toolbar_visible)
