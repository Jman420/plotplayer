"""
PlotPlayer specific Animation Parameters and Default Values

Public Class :
  * AnimationParams - Parameters related to Animation Playback
"""

_DEFAULT_ANIMATION_NAME = 'PlotPlayer'
_DEFAULT_FRAME_RATE = 30

class AnimationParams(object):
    """
    Parameters related to Animation Playback for PlotPlayer

    Public Attributes :
      * min_frame_number - Beginning frame number
      * max_frame_number - Ending frame number
      * frame_rate - Frame rate for playback
      * animation_name - Name of the animation
    """

    min_frame_number = None
    max_frame_number = None
    frame_rate = None
    animation_name = None

    def __init__(self, max_frame_number, min_frame_number=0, frame_rate=_DEFAULT_FRAME_RATE,
                 animation_name=_DEFAULT_ANIMATION_NAME):
        """
        Constructor

        Public Parameters :
          * min_frame_number - Beginning frame number
          * max_frame_number - Ending frame number
          * frame_rate - Frame rate for playback
          * animation_name - Name of the animation
        """
        self.min_frame_number = min_frame_number
        self.max_frame_number = max_frame_number
        self.frame_rate = frame_rate
        self.animation_name = animation_name

    def get_min_frame_num(self):
        """
        Return the Beginning Frame Number
        """
        return self.min_frame_number

    def get_max_frame_num(self):
        """
        Return the Ending Frame Number
        """
        return self.max_frame_number

    def get_frame_rate(self):
        """
        Return the Frame Rate
        """
        return self.frame_rate

    def get_animation_name(self):
        """
        Return the Animation Name
        """
        return self.animation_name
