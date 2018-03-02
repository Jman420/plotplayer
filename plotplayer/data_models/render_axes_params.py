"""
PlotPlayer specific Render Axes Parameters Class

Public Classes :
  * RenderAxesParams - Class containing pointers to animation and slider axes
"""

class RenderAxesParams(object):
    """
    Pointers to Animation and Slider Axes for Rendering

    Public Attributes :
      * animation_axes - Pointer to the Animation Axes
      * slider_axes - Pointer to the Slider Axes
    """

    animation_axes = None
    slider_axes = None

    def __init__(self, animation_axes, slider_axes):
        """
        Constructor

        Parameters :
          * animation_axes - Pointer to the Animation Axes
          * slider_axes - Pointer to the Slider Axes
        """
        self.animation_axes = animation_axes
        self.slider_axes = slider_axes

    def get_animation_axes(self):
        """
        Returns the Animation Axes
        """
        return self.animation_axes

    def get_slider_axes(self):
        """
        Returns the Slider Axes
        """
        return self.slider_axes
