"""
PlotPlayer specific Slider Parameters Class and Default Values

Public Constants :
  * DEFAULT_SLIDER_BACKGROUND_COLOR - Default background color for Slider Axes

Public Classes :
  * SliderParams - Class containing parameters related to rendering a Slider
"""

DEFAULT_SLIDER_BACKGROUND_COLOR = 'lightgoldenrodyellow'

class SliderParams(object):
    """
    Parameters related to rendering Sliders

    Public Attributes :
      * slider_background_color - String representing the background color for the Slider
      * slider_visible - Boolean indicated whether the Slider is visible
    """

    slider_background_color = None
    slider_visible = True

    def __init__(self, slider_background_color=DEFAULT_SLIDER_BACKGROUND_COLOR,
                 slider_visible=True):
        """
        Constructor

        Parameters :
          * slider_background_color - String representing the background color for the Slider
          * slider_visible - Boolean indicated whether the Slider is visible
        """
        self.slider_background_color = slider_background_color
        self.slider_visible = slider_visible

    def get_slider_background_color(self):
        """
        Return the Slider Background Color
        """
        return self.slider_background_color

    def get_slider_visible(self):
        """
        Return the Slider Visibility State
        """
        return self.slider_visible
