"""
PlotPlayer specific Animation Manager Methods and Classes

Public Classes:
  * AnimationManager - Manages Matplotlib FuncAnimation and RenderManager integration to
      produce animation
"""

from matplotlib.animation import FuncAnimation

from ..helpers import ui_helper, file_helper

VIDEO_EXTENSION = '.mp4'
HTML_EXTENSION = '.html'
JAVASCRIPT_EXTENSION = '.js.html'

SAVE_DIALOG_TITLE = 'Select video file to save'

VIDEO_FILE_TYPE = ['MP4 Video', '*{}'.format(VIDEO_EXTENSION)]
HTML_FILE_TYPE = ['HTML File', '*{}'.format(HTML_EXTENSION)]
JAVASCRIPT_FILE_TYPE = ['Javascript HTML File', '*{}'.format(JAVASCRIPT_EXTENSION)]

class AnimationManager(object):
    """
    Animation Manager for PlotPlayer Windows

    Public Methods:
      * initialize - Initialize the Animation Manager for playback
      * render - Render a specific frame of the associated animation
      * play - Begin playback from the current position; restarts from beginning if current
          position is the last frame
      * stop - Stop playback at its current position
      * toggle_playback - Toggle between play and stop states
      * get_frame_number - Returns the current frame number
      * get_total_frames - Returns the total number of frames in the current animation
      * get_html - Returns the current animation in HTML5 Video
      * get_javascript - Returns the current animation in Javascript Video
      * save_video - Saves the current animation to file as Video
      * save_html - Saves the current animation to file as HTML5 Video
      * save javascript - Saves the current animation to file as Javascript Video
    """

    _figure = None
    _render_handler = None
    _frame_num = None
    _animation_params = None
    _animation = None
    _playing = False

    def __init__(self, figure, render_handler):
        """
        Constructor

        Parameters:
          * figure - Instance of Pyplot figure associated with the draw canvas
          * render_handler - Instance of RenderManager associated with the current animation
        """
        self._figure = figure
        self._render_handler = render_handler

    def initialize(self, animation_params):
        """
        Initialize the Animation Manager for Playback

        Parameters:
          * animation_params - Instance of AnimationParams
        """
        self.stop()

        self._animation_params = animation_params

        self._frame_num = -1
        self._playing = False

    def render(self, frame_num):
        """
        Render a specific frame of the animation

        Parameters:
          * frame_num - The frame number to render
        """
        if frame_num < self._animation_params.min_frame_number:
            frame_num = self._animation_params.min_frame_number
        elif frame_num > self._animation_params.max_frame_number:
            frame_num = self._animation_params.max_frame_number

        total_frames = (self._animation_params.max_frame_number -
                        self._animation_params.min_frame_number)
        self._frame_num = int(frame_num)
        self._render_handler.render(self._frame_num, total_frames)

        if self._frame_num == self._animation_params.max_frame_number:
            self._playing = False

    def play(self):
        """
        Begin playback from the current frame; restart playback from beginning if at the end
        """
        if self._playing:
            return

        if self._frame_num == self._animation_params.max_frame_number:
            self._frame_num = -1

        frames_to_play = range(self._frame_num, self._animation_params.max_frame_number + 1)
        animation = FuncAnimation(self._figure, self.render, frames_to_play,
                                  interval=1000 // self._animation_params.frame_rate, repeat=False)
        
        self._playing = True
        self._animation = animation
        self._figure.canvas.draw()

    def stop(self):
        """
        Stop playback at the current position
        """
        if not self._playing:
            return

        self._animation.event_source.stop()
        self._playing = False

    def toggle_playback(self):
        """
        Toggle between play and stop states
        """
        if self._playing:
            self.stop()
        else:
            self.play()

    def get_frame_number(self):
        """
        Returns the current frame number
        """
        return self._frame_num

    def get_min_frame_num(self):
        """
        Returns the minimum frame number in the current animation
        """
        return self._animation_params.min_frame_number

    def get_max_frame_number(self):
        """
        Returns the maximum frame number in the current animation
        """
        return self._animation_params.max_frame_number

    def get_html(self):
        """
        Returns the current animation in HTML5 Video format
        """
        html = self._animation.to_html5_video()
        return html

    def get_javascript(self):
        """
        Returns the current animation in Javascript Video format
        """
        javascript = self._animation.to_jshtml()
        return javascript

    def save_video(self, file_name=None, writer=None):
        """
        Saves the current animation to file as Video

        Parameters:
          * file_name (optional) - Indicates the file name to write the video to; will prompt
              if omitted
          * writer (optional) - Specifies the video writer for Matplotlib to use to write the video
        """
        self.stop()

        if file_name is None:
            file_types = [VIDEO_FILE_TYPE, ui_helper.ALL_FILES_TYPE]
            animation_name = self._animation_params.animation_name
            file_name = ui_helper.get_save_dialog_result(SAVE_DIALOG_TITLE,
                                                         animation_name + VIDEO_EXTENSION,
                                                         file_types, VIDEO_EXTENSION)
        self._animation.save(file_name, writer)

    def save_html(self, file_name=None):
        """
        Saves the current animation to file as HTML5 Video

        Parameters:
          * file_name (optional) - Indicates the file name to write the video to; will prompt
              if omitted
        """
        self.stop()

        if file_name is None:
            file_types = [HTML_FILE_TYPE, ui_helper.ALL_FILES_TYPE]
            animation_name = self._animation_params.animation_name
            file_name = ui_helper.get_save_dialog_result(SAVE_DIALOG_TITLE,
                                                         animation_name + HTML_EXTENSION,
                                                         file_types, HTML_EXTENSION)
        video_html = self.get_html()
        file_helper.save_file(file_name, video_html)

    def save_javascript(self, file_name=None):
        """
        Saves the current animation to file as Javascript Video

        Parameters:
          * file_name (optional) - Indicates the file name to write the video to; will prompt
              if omitted
        """
        self.stop()

        if file_name is None:
            default_file_name = self._animation_params.animation_name + JAVASCRIPT_EXTENSION
            file_types = [JAVASCRIPT_FILE_TYPE, ui_helper.ALL_FILES_TYPE]
            file_name = ui_helper.get_save_dialog_result(SAVE_DIALOG_TITLE, default_file_name,
                                                         file_types, JAVASCRIPT_EXTENSION)
        video_javascript = self.get_javascript()
        file_helper.save_file(file_name, video_javascript)
