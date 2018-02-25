from matplotlib import pyplot
from matplotlib.animation import FuncAnimation

from .validators import type_validation
from .helpers import file_helper, ui_helper
from .ui import render_handler, input_handler

# Aspect ratio (ie. 4:3, 16:9, 21:9) in relation to DPI; default is half 16:9 (8:4.5)
DEFAULT_WINDOW_SIZE = (8, 4.5)
DEFAULT_ANIMATION_NAME = 'PlotPlayer'

VIDEO_EXTENSION = '.mp4'
HTML_EXTENSION = '.html'
JAVASCRIPT_EXTENSION = '.js.html'

SAVE_DIALOG_TITLE = 'Select video file to save'

VIDEO_FILE_TYPE = ['MP4 Video', '*{}'.format(VIDEO_EXTENSION)]
HTML_FILE_TYPE = ['HTML File', '*{}'.format(HTML_EXTENSION)]
JAVASCRIPT_FILE_TYPE = ['Javascript HTML File', '*{}'.format(JAVASCRIPT_EXTENSION)]

class PlotPlayer(object):
    """Function based animation player for Matplotlib"""
    figure = None
    render_processor = input_processor = None
    animation_name = animation = None
    frame_rate = None
    playing = False

    def __init__(self, window_title=None, figure=None, window_size=DEFAULT_WINDOW_SIZE,
                 slider_background_color=render_handler.SLIDER_BACKGROUND_COLOR,
                 toolbar_visible=False, slider_visible=True, key_press_handler=None,
                 skip_size=input_handler.SKIP_SIZE, jump_size=input_handler.JUMP_SIZE):
        if figure is None:
            figure = pyplot.figure(figsize=window_size)
        type_validation.assert_is_figure(figure, 'figure')
        self.figure = figure

        if window_title is None:
            window_title = DEFAULT_ANIMATION_NAME
        figure.canvas.set_window_title(window_title)

        animation_axes = None
        slider_axes = None
        if figure.axes:
            animation_axes = figure.axes[0]
        if len(figure.axes) > 1:
            slider_axes = figure.axes[1]
        self.render_processor = render_handler.RenderHandler(figure, animation_axes, slider_axes,
                                                             slider_background_color,
                                                             slider_visible, toolbar_visible)

        self.input_processor = input_handler.InputHandler(self, key_press_handler, skip_size,
                                                          jump_size)

    def initialize_animation(self, total_frames, draw_func, animation_name=DEFAULT_ANIMATION_NAME,
                             frame_rate=30):
        type_validation.assert_is_int(total_frames, 'total_frames')
        type_validation.assert_is_callable(draw_func, 'draw_func')
        type_validation.assert_is_int(frame_rate, 'frame_rate')

        self.stop()
        self.render_processor.initialize_rendering(total_frames, draw_func)
        self.input_processor.set_enabled(True)

        self.animation_name = animation_name
        self.frame_rate = frame_rate
        self.playing = False

    def render(self, frame_number):
        self.render_processor.render(frame_number)

        if frame_number == self.get_total_frames():
            self.stop()

    def play(self):
        if self.playing:
            return

        slider = self.render_processor.slider
        if slider.val == slider.valmax:
            self.render(0)

        frames_to_play = range(int(slider.val), slider.valmax + 1)
        animation = FuncAnimation(self.figure, self.render, frames_to_play,
                                  interval=1000 // self.frame_rate, repeat=False)
        self.figure.canvas.draw()

        self.playing = True
        self.animation = animation

    def stop(self):
        if not self.playing:
            return

        self.animation.event_source.stop()
        self.playing = False

    def toggle_playback(self):
        if self.playing:
            self.stop()
        else:
            self.play()

    def get_figure(self):
        return self.figure

    def get_animation_axes(self):
        return self.render_processor.animation_axes

    def get_current_frame_number(self):
        return int(self.render_processor.slider.val)

    def get_total_frames(self):
        return int(self.render_processor.slider.valmax)

    def toggle_toolbar(self):
        self.render_processor.toggle_toolbar()

    def toggle_slider(self):
        self.render_processor.toggle_slider()

    def get_html(self):
        html = self.animation.to_html5_video()
        return html

    def get_javascript(self):
        javascript = self.animation.to_jshtml()
        return javascript

    def save_video(self, file_name=None, writer=None):
        self.stop()

        if file_name is None:
            file_types = [VIDEO_FILE_TYPE, ui_helper.ALL_FILES_TYPE]
            file_name = ui_helper.get_save_dialog_result(SAVE_DIALOG_TITLE,
                                                         self.animation_name + VIDEO_EXTENSION,
                                                         file_types, VIDEO_EXTENSION)
        self.animation.save(file_name, writer)

    def save_html(self, file_name=None):
        self.stop()

        if file_name is None:
            file_types = [HTML_FILE_TYPE, ui_helper.ALL_FILES_TYPE]
            file_name = ui_helper.get_save_dialog_result(SAVE_DIALOG_TITLE,
                                                         self.animation_name + HTML_EXTENSION,
                                                         file_types, HTML_EXTENSION)
        video_html = self.get_html()
        file_helper.save_file(file_name, video_html)

    def save_javascript(self, file_name=None):
        self.stop()

        if file_name is None:
            file_types = [JAVASCRIPT_FILE_TYPE, ui_helper.ALL_FILES_TYPE]
            file_name = ui_helper.get_save_dialog_result(SAVE_DIALOG_TITLE,
                                                         self.animation_name + JAVASCRIPT_EXTENSION,
                                                         file_types, JAVASCRIPT_EXTENSION)
        video_javascript = self.get_javascript()
        file_helper.save_file(file_name, video_javascript)

    @staticmethod
    def show_players(blocking=True):
        ui_helper.show_players(blocking)
