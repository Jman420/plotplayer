"""
PlotPlayer specific Render Axes Parameters Class

Public Classes :
  * RenderAxesParams - Class containing pointers to animation and slider axes
"""

class RenderAxesParams(object):
    """
    Pointers to Animation and Slider Axes for Rendering

    Public Attributes :
      * animation_axes - Instance of Matplotlib Axes to use for Animation
      * animation_x_limits - An array representing the minimum and maximum animation x-axis limits
      * animation_y_limits - An array representing the minimum and maximum animation y-axis limits
      * slider_axes - Instance of Matplotlib Axes to use for the Scrubber Slider
    """

    animation_axes = None
    animation_x_limits = None
    animation_y_limits = None
    slider_axes = None

    def __init__(self, animation_axes=None, slider_axes=None, animation_x_limits=None,
                 animation_y_limits=None):
        """
        Constructor

        Parameters :
          * animation_axes - Instance of Matplotlib Axes to use for Animation
          * animation_x_limits - An array representing the minimum and maximum animation x-axis limits
          * animation_y_limits - An array representing the minimum and maximum animation y-axis limits
          * slider_axes - Instance of Matplotlib Axes to use for the Scrubber Slider
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
        """
        Returns the Animation X-Axis Limits
        """
        return self.get_animation_x_limits

    def get_animation_y_limits(self):
        """
        Returns the Animation Y-Axis Limits
        """
        return self.get_animation_y_limits

    def get_slider_axes(self):
        """
        Returns the Slider Axes
        """
        return self.slider_axes
