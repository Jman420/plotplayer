from matplotlib.animation import FuncAnimation

from ..helpers import ui_helper, file_helper

DEFAULT_ANIMATION_NAME = "PlotPlayer"
DEFAULT_FRAME_RATE = 30

VIDEO_EXTENSION = '.mp4'
HTML_EXTENSION = '.html'
JAVASCRIPT_EXTENSION = '.js.html'

SAVE_DIALOG_TITLE = 'Select video file to save'

VIDEO_FILE_TYPE = ['MP4 Video', '*{}'.format(VIDEO_EXTENSION)]
HTML_FILE_TYPE = ['HTML File', '*{}'.format(HTML_EXTENSION)]
JAVASCRIPT_FILE_TYPE = ['Javascript HTML File', '*{}'.format(JAVASCRIPT_EXTENSION)]

#pylint: disable=too-many-instance-attributes
class AnimationManager(object):
    """description of class"""

    _figure = None
    _render_processor = None
    _frame_num = None
    _max_frames = None
    _frame_rate = None
    _animation = None
    _animation_name = None
    _playing = False

    def __init__(self, figure, render_processor):
        self._figure = figure
        self._render_processor = render_processor

    def initialize(self, max_frames, frame_rate=DEFAULT_FRAME_RATE,
                   animation_name=DEFAULT_ANIMATION_NAME):
        self._frame_rate = frame_rate
        self._max_frames = max_frames
        self._animation_name = animation_name

        self._frame_num = 0
        self._playing = False

    def render(self, frame_num):
        if frame_num >= self._max_frames:
            frame_num = self._max_frames - 1

        self._frame_num = frame_num
        self._render_processor.render(frame_num)

        if self._frame_num >= self._max_frames:
            self._playing = False

    def play(self):
        if self._playing:
            return

        if self._frame_num == self._max_frames:
            self._frame_num = 0

        frames_to_play = range(self._frame_num, self._max_frames + 1)
        animation = FuncAnimation(self._figure, self.render, frames_to_play,
                                  interval=1000 // self._frame_rate, repeat=False)
        self._figure.canvas.draw()

        self._playing = True
        self._animation = animation

    def stop(self):
        if not self._playing:
            return

        self._animation.event_source.stop()
        self._playing = False

    def toggle_playback(self):
        if self._playing:
            self.stop()
        else:
            self.play()

    def get_frame_number(self):
        return self._frame_num

    def get_total_frames(self):
        return self._max_frames

    def get_html(self):
        html = self._animation.to_html5_video()
        return html

    def get_javascript(self):
        javascript = self._animation.to_jshtml()
        return javascript

    def save_video(self, file_name=None, writer=None):
        self.stop()

        if file_name is None:
            file_types = [VIDEO_FILE_TYPE, ui_helper.ALL_FILES_TYPE]
            file_name = ui_helper.get_save_dialog_result(SAVE_DIALOG_TITLE,
                                                         self._animation_name + VIDEO_EXTENSION,
                                                         file_types, VIDEO_EXTENSION)
        self._animation.save(file_name, writer)

    def save_html(self, file_name=None):
        self.stop()

        if file_name is None:
            file_types = [HTML_FILE_TYPE, ui_helper.ALL_FILES_TYPE]
            file_name = ui_helper.get_save_dialog_result(SAVE_DIALOG_TITLE,
                                                         self._animation_name + HTML_EXTENSION,
                                                         file_types, HTML_EXTENSION)
        video_html = self.get_html()
        file_helper.save_file(file_name, video_html)

    def save_javascript(self, file_name=None):
        self.stop()

        if file_name is None:
            default_file_name = self._animation_name + JAVASCRIPT_EXTENSION
            file_types = [JAVASCRIPT_FILE_TYPE, ui_helper.ALL_FILES_TYPE]
            file_name = ui_helper.get_save_dialog_result(SAVE_DIALOG_TITLE, default_file_name,
                                                         file_types, JAVASCRIPT_EXTENSION)
        video_javascript = self.get_javascript()
        file_helper.save_file(file_name, video_javascript)
