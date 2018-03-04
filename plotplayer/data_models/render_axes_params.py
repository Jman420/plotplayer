"""
PlotPlayer specific Render Axes Parameters Class

Public Classes :
  * RenderAxesParams - Class containing pointers to animation and slider axes
"""

_DEFAULT_X_LIMITS = [0, 1280]
_DEFAULT_Y_LIMITS = [0, 720]

class RenderAxesParams(object):
    """
    Pointers to Animation and Slider Axes for Rendering

    Public Attributes :
      * animation_axes - Pointer to the Animation Axes
      * slider_axes - Pointer to the Slider Axes
    """

    animation_axes = None
    animation_x_limits = None
    animation_y_limits = None
    slider_axes = None

    def __init__(self, animation_axes=None, slider_axes=None, animation_x_limits=_DEFAULT_X_LIMITS,
                 animation_y_limits=_DEFAULT_Y_LIMITS):
        """
        Constructor

        Parameters :
          * animation_axes - Pointer to the Animation Axes
          * slider_axes - Pointer to the Slider Axes
        """
        self.animation_axes = animation_axes
        self.animation_x_limits = animation_x_limits
        self.animation_y_limits = animation_y_limits
        self.slider_axes = slider_axes

    def get_animation_axes(self):
        """
        Returns the Animation Axes
        """
        return self.animation_axes

    def get_animation_x_limits(self):
        return self.get_animation_x_limits

    def get_animation_y_limits(self):
        return self.get_animation_y_limits

    def get_slider_axes(self):
        """
        Returns the Slider Axes
        """
        return self.slider_axes
