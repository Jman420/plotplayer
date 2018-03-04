"""
PlotPlayer specific Window Manager Methods and Classes

Public Classes:
  * WindowManager - Manages a Matplotlib figure as a Window
"""

from tkinter.constants import BOTTOM, X
from matplotlib import pyplot

from ..validators import type_validation

# Aspect ratio (ie. 4:3, 16:9, 21:9) in relation to DPI; default is half 16:9 (8:4.5)
_DEFAULT_WINDOW_SIZE = (8, 4.5)
_DEFAULT_ANIMATION_NAME = 'PlotPlayer'

class WindowManager(object):
    """
    Window Manager for PlotPlayer Windows

    Public Methods:
      * get_toolbar_visible - Returns boolean indicating whether the Matplotlib Navigation
          Toolbar is visible
      * set_toolbar_visible - Method to hide/show the Matplotlib Navigation Toolbar
      * toggle_toolbar - Method to toggle the visibility of the Matplotlib Navigation Toolbar
      * get_figure - Returns the figure associated with the WindowManager
    """

    _figure = None
    _toolbar_visible = False

    def __init__(self, window_size=_DEFAULT_WINDOW_SIZE, window_title=_DEFAULT_ANIMATION_NAME,
                 figure=None, toolbar_visible=True):
        """
        Constructor

        Parameters:
          * window_size (optional) - Specifies the initial window size as an aspect ratio
              (4:3, 16:9, 21:9)
          * window_title (optional) - Title for the window associated with the WindowManager
          * figure (optional) - A custom pre-built figure for a window
          * toolbar_visible (optional) - Boolean indicating whether the Matplotlib Navigation
              Toolbar is visible
        """
        if figure is None:
            figure = pyplot.figure(figsize=window_size)
        type_validation.assert_is_figure(figure, 'figure')
        self._figure = figure

        self.set_window_title(window_title)
        self.set_toolbar_visible(toolbar_visible)

    def set_window_title(self, window_title):
        if window_title is None:
            window_title = _DEFAULT_ANIMATION_NAME
        self.get_figure().canvas.set_window_title(window_title)

    def get_toolbar_visible(self):
        """
        Returns a boolean indicating whether the Matplotlib Navigation Toolbar is visible
        """
        return self._toolbar_visible

    def set_toolbar_visible(self, visible):
        """
        Method to hide/show the Matplotlib Navigation Toolbar
        """
        if visible:
            self._figure.canvas.toolbar.pack(side=BOTTOM, fill=X)
        else:
            self._figure.canvas.toolbar.pack_forget()

        self._toolbar_visible = visible

    def toggle_toolbar(self):
        """
        Method to toggle the visibility of the Matplotlib Navigation Toolbar
        """
        self.set_toolbar_visible(not self._toolbar_visible)

    def get_figure(self):
        """
        Returns the figure used for the Window
        """
        return self._figure
